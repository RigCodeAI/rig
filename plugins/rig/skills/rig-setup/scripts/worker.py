"""Rig-owned bounded workers. A closed stdin lease cancels owned work.

No process enumeration, permission elevation, authentication fallback or retry.
Only fixed diagnostics leave this transport; captured worker bytes stay private.
"""
from contextlib import contextmanager
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import tempfile
import time

CAPTURE_LIMIT_BYTES = 16_777_216

PERMISSION = ('Execution permission denied. Explain the required worker execution '
              'in the calling conversation. Retry only after caller approval using '
              'supported permissions; declining stops this work.')


class WorkerError(RuntimeError):
    def __init__(self, outcome):
        self.outcome = outcome
        super().__init__(outcome['status'] + ': ' + outcome['diagnostic'] +
                         (' Cleanup also failed.' if outcome.get('cleanup_error') else ''))


def failed(status, cleanup=False):
    return {'status': status, 'exit_code': None, 'cleanup_error': cleanup,
            'diagnostic': PERMISSION if status == 'permission_required' else
            'Worker did not complete; no qualification. If execution permission is required, explain it in the calling conversation before any caller-approved retry.'}


def remaining(deadline):
    seconds = deadline - time.monotonic()
    if seconds <= 0:
        raise WorkerError(failed('timeout'))
    return seconds


@contextmanager
def native_slot(deadline, observe=None):
    """One native evaluator lane per POSIX user, across isolated homes and jobs."""
    if os.name != 'posix':
        raise WorkerError(failed('startup_failed'))
    import fcntl
    # A persistent directory inode avoids unlink/recreate races. It contains no
    # project data. TMPDIR and HOME can both be private to a single evaluation.
    uid = os.geteuid()
    path = Path('/tmp') / f'rig-native-qualification-{uid}'
    path.mkdir(mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        info = os.fstat(fd)
        if info.st_uid != uid or stat.S_IMODE(info.st_mode) != 0o700:
            raise PermissionError('Native scheduler directory unavailable')
        started = time.monotonic()
        while True:
            remaining(deadline)
            reason = observe() if observe else None
            if reason:
                raise WorkerError(failed(reason))
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                time.sleep(min(.05, remaining(deadline)))
        yield fd, time.monotonic() - started
    finally:
        # The supervisor inherits a reference. If the coordinator dies, its
        # lease closes and the slot remains held until owned work is cleaned.
        os.close(fd)


class Worker:
    def __init__(self, argv, cwd, env, directory, seconds, forward_stdin=False, rig=None, slot=None):
        self.directory = Path(directory)
        if not 0 < seconds <= 14_400:
            raise WorkerError(failed('invalid_limits'))
        try:
            self.directory.mkdir(parents=True, exist_ok=False, mode=0o700)
            self.directory.chmod(0o700)
        except PermissionError:
            raise WorkerError(failed('permission_required')) from None
        except OSError:
            raise WorkerError(failed('startup_failed')) from None
        self.p = None
        self.started = time.monotonic()
        self.outcome = None
        executable = rig or os.environ.get('RIG_EXECUTABLE') or shutil.which('rig')
        if not executable:
            raise WorkerError(failed('startup_failed'))
        request = self.directory / 'request.json'
        request.write_text(json.dumps({'argv': [str(a) for a in argv],
            'cwd': str(Path(cwd).resolve()), 'directory': str(self.directory.resolve()),
            'timeout_ms': max(1, int(seconds * 1000)), 'output_limit_bytes': CAPTURE_LIMIT_BYTES,
            'forward_stdin': forward_stdin}))
        request.chmod(0o600)
        try:
            self.p = subprocess.Popen([str(executable), '__eval_worker', str(request)],
                env=env, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, start_new_session=True,
                pass_fds=() if slot is None else (slot,))
        except PermissionError:
            raise WorkerError(failed('permission_required')) from None
        except OSError:
            raise WorkerError(failed('startup_failed')) from None

    def poll(self):
        if self.outcome is not None:
            return self.outcome
        if self.p.poll() is None:
            return None
        try:
            path = self.directory / 'result.json'
            if path.stat().st_size > 4096:
                raise ValueError()
            self.outcome = json.loads(path.read_text())
        except (OSError, ValueError):
            self.outcome = failed('supervisor_failed', cleanup=True)
        return self.outcome

    def send(self, value):
        try:
            self.p.stdin.write((json.dumps(value) + '\n').encode())
            self.p.stdin.flush()
        except (OSError, ValueError):
            raise WorkerError(self.poll() or failed('worker_failed')) from None

    def close(self):
        if self.p is None:
            return self.outcome
        # Never wait without a bound. EOF reaches the native lease watcher even
        # if a child is blocked writing/reading. SIGTERM is a supported backup.
        try:
            self.p.stdin.close()
        except (OSError, ValueError):
            pass
        try:
            self.p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                self.p.send_signal(signal.SIGTERM)
            except OSError:
                self.outcome = failed('cleanup_failed', cleanup=True)
                return self.outcome
            try:
                self.p.wait(timeout=3)
            except subprocess.TimeoutExpired:
                # Do not kill the supervisor and abandon its owned group.
                self.outcome = failed('cleanup_failed', cleanup=True)
        return self.poll() or self.outcome


def run(argv, cwd, env, directory, seconds, cancel=None, rig=None, observe=None, slot=None):
    worker = Worker(argv, cwd, env, directory, seconds, rig=rig, slot=slot)
    primary = None
    try:
        while worker.poll() is None:
            rejected = observe() if observe else None
            if rejected:
                primary = failed(rejected)
                break
            if cancel is not None and cancel.is_set():
                primary = failed('cancelled')
                break
            time.sleep(.02)
    except BaseException:
        # Preserve interruption, attaching only a fixed cleanup note if needed.
        outcome = worker.close()
        if outcome and outcome.get('cleanup_error'):
            import sys
            sys.exception().add_note('Owned worker cleanup also failed.')
        raise
    finally:
        outcome = worker.close()
    if primary is None and observe:
        rejected = observe()
        if rejected:
            primary = failed(rejected)
    result = primary or outcome
    if primary and outcome and outcome.get('cleanup_error'):
        result['cleanup_error'] = True
    result['seconds'] = round(time.monotonic() - worker.started, 3)
    return result
