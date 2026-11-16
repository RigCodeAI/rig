"""Closed controller checkpoints; raw exceptions never become author feedback."""
import json
from pathlib import Path
import subprocess
import time

from worker import WorkerError


class EvaluationError(RuntimeError):
    def __init__(self, reason, candidate_location=None):
        self.reason = reason
        self.candidate_location = candidate_location
        super().__init__(reason)


def checkpoint(job, stage, reason='internal_error', cleanup_error=False, candidate_location=None):
    if job is not None:
        path = Path(job) / 'diagnostic.json'
        pending = path.with_suffix('.pending')
        value = {'schema_version': 1, 'stage': stage, 'reason': reason, 'cleanup_error': cleanup_error}
        if candidate_location is not None:
            value['candidate_location'] = candidate_location
        pending.write_text(json.dumps(value))
        pending.replace(path)
        with (Path(job) / 'stages.jsonl').open('a') as stream:
            stream.write(json.dumps({'stage': stage, 'reason': reason,
                                     'cleanup_error': cleanup_error,
                                     'monotonic_seconds': time.monotonic()}) + '\n')


def failure(job, error):
    path = Path(job) / 'diagnostic.json'
    stage = json.loads(path.read_text())['stage'] if path.exists() else 'preparation'
    reason, cleanup, location = 'internal_error', False, None
    if isinstance(error, WorkerError):
        # Only fixed transport statuses survive; never error text or OS paths.
        status = error.outcome.get('status')
        reason = status if status in {
            'permission_required', 'timeout', 'output_limit', 'cancelled',
            'cleanup_failed', 'worker_failed', 'auth_route_rejected',
            'overage_rejected', 'quota_rejected'} else 'runtime_unavailable'
        cleanup = error.outcome.get('cleanup_error') is True
    elif isinstance(error, EvaluationError):
        reason = error.reason
        location = error.candidate_location
    elif isinstance(error, PermissionError):
        reason = 'permission_required'
    elif isinstance(error, subprocess.TimeoutExpired):
        reason = 'timeout'
    elif stage == 'case_validation':
        reason = 'case_construction_invalid'
    elif stage == 'preflight':
        reason = 'preflight_failed'
    checkpoint(job, stage, reason, cleanup, location)
