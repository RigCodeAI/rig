"""Native subscription worker controls reused from experiments/ponytail_controls
and experiments/loop_benchmark: preflight, auth copy, bounded capture and cleanup.
No model calls occur on import or in normal CI.
"""
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import threading


def environment(home,state):
    env={k:v for k,v in os.environ.items() if not any(s in k.upper() for s in ('API_KEY','BASE_URL','AUTH_TOKEN','ACCESS_TOKEN','SECRET')) and not k.startswith(('ANTHROPIC_','AWS_','AZURE_','GOOGLE_','VERTEX_','OPENAI_','CODEX_','CLAUDE_'))}
    env.update(CODEX_HOME=str(home),RIG_HOME=str(state),PYTHONDONTWRITEBYTECODE='1',PATH='/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin')
    return env


class Rpc:
    def __init__(self,host,env):
        self.p=subprocess.Popen([str(host),'app-server','--stdio'],env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,start_new_session=True)
        self.rows=queue.Queue();self.next_id=0
        def reader():
            for line in self.p.stdout:
                try:self.rows.put(json.loads(line))
                except ValueError:pass
        threading.Thread(target=reader,daemon=True).start()
        try:
            self.request('initialize',{'clientInfo':{'name':'rig_benchmark','version':'1.0'},'capabilities':{'experimentalApi':True}})
            self.send({'method':'initialized','params':{}})
        except Exception:
            self.close();raise

    def send(self,value):self.p.stdin.write(json.dumps(value)+'\n');self.p.stdin.flush()

    def request(self,method,params=None):
        self.next_id+=1;ident=self.next_id
        self.send({'id':ident,'method':method,**({'params':params} if params is not None else {})})
        while True:
            row=self.rows.get(timeout=30)
            if row.get('id')==ident:
                if 'error' in row:raise RuntimeError(str(row['error']))
                return row['result']

    def close(self):
        try:os.killpg(self.p.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        self.p.wait(timeout=5)
        for stream in (self.p.stdin,self.p.stdout):stream.close()


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

import time
def auth_copy(source,dest):
    data=json.loads(Path(source).read_text())
    if data.get('auth_mode')!='chatgpt' or not data.get('tokens') or data.get('OPENAI_API_KEY'):raise RuntimeError('Subscription auth file required; no API key route')
    __import__("shutil").copyfile(source,dest);Path(dest).chmod(0o600)

def processes():
    lines=subprocess.check_output(['ps','-axo','pid=,ppid=,pgid='],text=True).splitlines()
    return [tuple(map(int,line.split())) for line in lines if len(line.split())==3]

def cleanup(child,owned):
    current={pid:pgid for pid,_,pgid in processes()}
    groups={child.pid} if child.poll() is None else set()
    groups.update(pgid for pid,pgid in owned.items() if current.get(pid)==pgid)
    for group in groups:
        if group==os.getpgrp():continue
        try:os.killpg(group,signal.SIGKILL)
        except ProcessLookupError:pass
    child.wait()

def bounded(argv,cwd,env,cell,cap=600):
    owned={};start=time.monotonic();status='completed';offset=0;pending='';events=[]
    with (cell/'transcript.jsonl').open('w') as out,(cell/'stderr.log').open('w') as err:
        p=subprocess.Popen(argv,cwd=cwd,env=env,stdout=out,stderr=err,start_new_session=True)
        try:
            while p.poll() is None:
                parents={p.pid}|set(owned)
                rows=processes();again=True
                while again:
                    again=False
                    for pid,ppid,pgid in rows:
                        if ppid in parents and pid not in parents:
                            parents.add(pid);owned[pid]=pgid;again=True
                with (cell/'transcript.jsonl').open() as stream:
                    stream.seek(offset);pending+=stream.read();offset=stream.tell()
                while '\n' in pending:
                    line,pending=pending.split('\n',1)
                    try:e=json.loads(line)
                    except ValueError:continue
                    events.append(e)
                    if e.get('subtype')=='init' and e.get('apiKeySource')!='none':status='auth_route_rejected'
                    info=e.get('rate_limit_info',{})
                    if info.get('isUsingOverage'):status='overage_rejected'
                    if info.get('status')=='rejected':status='quota_rejected'
                if status!='completed':break
                if time.monotonic()-start>=cap:status='timeout';break
                time.sleep(min(.25,max(0,cap-(time.monotonic()-start))))
        finally:cleanup(p,owned)
    return {'exit_code':p.returncode,'status':status,'seconds':round(time.monotonic()-start,3)}
