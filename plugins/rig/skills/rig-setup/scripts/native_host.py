"""Native subscription worker controls reused from experiments/ponytail_controls
and experiments/loop_benchmark: preflight, auth copy, bounded capture and cleanup.
No model calls occur on import or in normal CI.
"""
import json
import os
from pathlib import Path
import tempfile
import time

from worker import CAPTURE_LIMIT_BYTES, Worker, WorkerError, failed, run


def environment(home,state):
    env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ('API_KEY','BASE_URL','AUTH_TOKEN','ACCESS_TOKEN','SECRET')) and not k.startswith(('ANTHROPIC_','AWS_','AZURE_','GOOGLE_','VERTEX_','OPENAI_','CODEX_','CLAUDE_'))}
    env.update(CODEX_HOME=str(home),RIG_HOME=str(state),PYTHONDONTWRITEBYTECODE='1',PATH='/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin')
    return env


class Rpc:
    def __init__(self, host, env):
        self.temp = tempfile.TemporaryDirectory(prefix='rig-preflight-')
        self.worker = None
        self.next_id = 0
        self.offset = 0
        self.pending = b''
        try:
            self.worker = Worker([str(host), 'app-server', '--stdio'], Path.cwd(),
                env, Path(self.temp.name)/'worker', 120, forward_stdin=True)
            self.request('initialize', {'clientInfo': {'name': 'rig_setup', 'version': '1.0'},
                'capabilities': {'experimentalApi': True}})
            self.send({'method': 'initialized', 'params': {}})
        except BaseException:
            self.close()
            raise

    def send(self, value):
        self.worker.send(value)

    def request(self, method, params=None):
        self.next_id += 1
        ident = self.next_id
        self.send({'id': ident, 'method': method,
            **({'params': params} if params is not None else {})})
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            path = self.worker.directory / 'stdout'
            try:
                with path.open('rb') as stream:
                    stream.seek(self.offset)
                    data = stream.read(65_536)
                    self.offset = stream.tell()
            except FileNotFoundError:
                data = b''
            self.pending += data
            if len(self.pending) > 1_048_576:
                raise WorkerError(failed('output_limit'))
            while b'\n' in self.pending:
                line, self.pending = self.pending.split(b'\n', 1)
                try:
                    row = json.loads(line)
                except (ValueError, UnicodeError):
                    continue
                if not isinstance(row, dict):
                    continue
                if row.get('id') == ident:
                    if 'error' in row:
                        raise WorkerError(failed('rpc_failed'))
                    return row.get('result', {})
            outcome = self.worker.poll()
            if outcome is not None:
                raise WorkerError(outcome if outcome['status'] != 'completed' else failed('rpc_failed'))
            time.sleep(.01)
        raise WorkerError(failed('timeout'))

    def close(self):
        try:
            if self.worker is not None:
                outcome = self.worker.close()
                # Cancellation is the normal way to close a live RPC session.
                if outcome and outcome.get('cleanup_error'):
                    import sys
                    if sys.exception() is not None:
                        if isinstance(sys.exception(), WorkerError):
                            sys.exception().outcome['cleanup_error'] = True
                        sys.exception().add_note('Owned preflight cleanup also failed.')
                    else:
                        raise WorkerError(outcome)
        finally:
            self.temp.cleanup()


def quota_ok(limits):
    buckets=limits.get('rateLimitsByLimitId') or {'codex':limits.get('rateLimits')}
    windows=[]
    for bucket in buckets.values():
        if not isinstance(bucket,dict) or bucket.get('rateLimitReachedType') or bucket.get('spendControlReached'):return False
        for key in ('primary','secondary'):
            w=bucket.get(key)
            if w is not None:
                used=w.get('usedPercent')
                if not isinstance(used,(int,float)) or not 0<=used<85:return False
                windows.append(w)
    return bool(windows)


def preflight(host,env,model=None):
    rpc=Rpc(host,env)
    try:
        account=rpc.request('account/read',{'refreshToken':False}).get('account')
        if not account or account.get('type')!='chatgpt':raise RuntimeError('ChatGPT authentication required; no API route permitted')
        limits=rpc.request('account/rateLimits/read')
        if not quota_ok(limits):raise RuntimeError('Subscription windows unavailable or >=85% used; no paid credit fallback permitted')
        result={'auth_type':account['type'],'plan':account.get('planType'),'limits':limits,'model_calls':0}
        if model:
            models=rpc.request('model/list',{'includeHidden':False})['data']
            found=next((m for m in models if m.get('model')==model or m.get('id')==model),None)
            if found is None:raise RuntimeError('Configured model unavailable for this subscription: '+model)
            result['model']={k:found.get(k) for k in ('id','model','supportedReasoningEfforts','defaultReasoningEffort')}
        return result
    finally:rpc.close()

def auth_copy(source,dest):
    data=json.loads(Path(source).read_text())
    if data.get('auth_mode')!='chatgpt' or not data.get('tokens') or data.get('OPENAI_API_KEY'):raise RuntimeError('Subscription auth file required; no API key route')
    __import__("shutil").copyfile(source,dest);Path(dest).chmod(0o600)

def bounded(argv, cwd, env, cell, cap=600, cancel=None, rig=None):
    offset = 0
    pending = b''
    rejected = None

    def inspect(line):
        if not line.strip():
            return None
        try:
            event = json.loads(line)
        except (ValueError, UnicodeError, RecursionError):
            return 'rpc_failed'
        if not isinstance(event, dict):
            return 'rpc_failed'
        if event.get('subtype') == 'init' and event.get('apiKeySource') != 'none':
            return 'auth_route_rejected'
        info = event.get('rate_limit_info', {})
        if isinstance(info, dict):
            if info.get('isUsingOverage'):
                return 'overage_rejected'
            if info.get('status') == 'rejected':
                return 'quota_rejected'
        return None

    def observe():
        nonlocal offset, pending, rejected
        path = Path(cell) / 'worker' / 'stdout'
        try:
            with path.open('rb') as stream:
                stream.seek(offset)
                pending += stream.read(65_536)
                offset = stream.tell()
        except FileNotFoundError:
            return rejected
        # Session events include escaped command output; retain the native stream bound.
        if len(pending) > CAPTURE_LIMIT_BYTES:
            return 'output_limit'
        while b'\n' in pending:
            line, pending = pending.split(b'\n', 1)
            rejected = rejected or inspect(line)
        return rejected

    result = run(argv, cwd, env, Path(cell) / 'worker', cap,
                 cancel=cancel, rig=rig, observe=observe)
    # Drain bounded final events too; fast exits cannot bypass auth guards.
    path = Path(cell) / 'worker' / 'stdout'
    while path.exists() and offset < path.stat().st_size:
        reject = observe()
        if reject:
            if result['status'] == 'completed':
                result['status'] = reject
            break
    # A fast exit or missing final newline cannot hide an auth/overage event.
    # Invalid or truncated JSON never becomes successful evidence.
    if result['status'] == 'completed' and pending:
        reject = inspect(pending)
        if reject:
            result['status'] = reject
    return result
