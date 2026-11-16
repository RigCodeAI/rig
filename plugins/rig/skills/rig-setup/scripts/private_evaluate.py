"""Local fresh-context construction/grading runner; no public comparison stdout.

The CLI owns request reservation and final qualification policy. Hidden artifacts and
process output stay out of ordinary check receipts. Same-user files are readable.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

from evaluate import prepare
from qualify import run, sha
from evaluation_feedback import EvaluationError, checkpoint, failure
from worker import WorkerError, run as run_worker


def validate_candidate(job, source, engine, request):
    """Check authored syntax on public source, outside the fresh context's inputs."""
    rules = job / 'validation-rule.json'
    rules.write_text(request['candidate'])
    checkpoint(job, 'rule_validation')
    env = dict(os.environ, SEMGREP_ENABLE_VERSION_CHECK='0', SEMGREP_SEND_METRICS='off')
    try:
        result = run_worker([str(engine), 'scan', '--config', str(rules), '--strict',
                             '--json', '--disable-version-check', request['paths'][0]],
                            source, env, job / 'rule-validation', 30)
        try:
            raw = json.loads((job / 'rule-validation/stdout').read_text())
        except (OSError, ValueError):
            raw = {}
        kinds = {row.get('type') for row in raw.get('errors', []) if isinstance(row.get('type'), str)}
        if kinds & {'Rule parse error', 'Pattern parse error', 'Invalid rule schema'}:
            ids = {row.get('rule_id') for row in raw.get('errors', []) if isinstance(row.get('rule_id'), str)}
            matches = [(len(rule['id']), n, 'pattern' if 'pattern' in rule else 'rule')
                       for n, rule in enumerate(json.loads(request['candidate']).get('rules', []))
                       if any(ident == rule['id'] or ident.endswith('.' + rule['id']) for ident in ids)]
            matched = max(matches, default=None)
            location = {'rule_index': matched[1], 'field': matched[2]} if matched else None
            raise EvaluationError('invalid_rule', location)
        if result['status'] != 'completed' or result['exit_code'] != 0:
            raise WorkerError(result)
        if not raw:
            raise EvaluationError('scanner_error')
        if raw.get('errors'):
            raise EvaluationError('target_parse_error')
    finally:
        rules.unlink(missing_ok=True)


def evaluate(job, vault, engine, seconds, author_root):
    checkpoint(job, 'preparation')
    request = json.loads((job / 'request.json').read_text())
    source = job / 'source'
    source.mkdir()
    for path, text in request['sources'].items():
        target = source / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    for path, encoded in request.get('binary_sources', {}).items():
        target = source / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(bytes.fromhex(encoded))
    baseline = job / 'baseline.yaml'
    baseline.write_text(request['baseline'])
    validate_candidate(job, source, engine, request)
    # Only source and baseline are supplied to the fresh context. Same-user reads
    # are not isolated. The separate oracle denies candidate/history paths.
    frozen = prepare(source, job / 'construction', baseline, seconds,
                     denied_paths=[vault, author_root, Path.home()/'.claude', Path.home()/'.agents'], targets=request['paths'],
                     focus={'statement': request.get('statement') or request.get('gap') or 'Verify the declared caller operation',
                            'gap': request.get('gap', ''), 'paths': request['paths'],
                            'limitations': request.get('limitations', '')},
                     progress=lambda stage: checkpoint(job, stage))
    checkpoint(job, 'case_validation')
    location = Path(frozen['evaluation'])
    targets = {row['target'] for row in json.loads((location / 'private/cohort.json').read_text())['cases']}
    if targets != set(request['paths']):
        raise EvaluationError('case_construction_invalid')
    for path, digest in frozen['bindings'].items():
        if sha(location / path) != digest:
            raise EvaluationError('case_construction_invalid')
    for path, digest in frozen['source_inputs'].items():
        if sha(source / path) != digest:
            raise EvaluationError('stale_source')
    # Materialize candidate only after construction exits and cases are frozen.
    (source / '.rig').mkdir()
    rules = source / '.rig/candidate.json'
    rules.write_text(request['candidate'])
    (source / '.rig/baseline.yaml').write_text(request['baseline'])
    check = {'id': 'opengrep-default', 'opengrep_rules': '.rig/baseline.yaml',
             'paths': ['**']}
    (source / '.rig/checks.toml').write_text('schema_version = 1\n[[checks]]\n' +
        ''.join(key + ' = ' + json.dumps(value) + '\n' for key, value in check.items()))
    subprocess.run(['git', 'init', '-q', str(source)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    bindings = {str(location / path): digest for path, digest in frozen['bindings'].items()}
    bindings.update({str(Path(frozen['source_root']) / path): digest
                     for path, digest in frozen['source_inputs'].items()})
    manifest = {'purpose': 'qualification', 'rig': os.environ['RIG_EXECUTABLE'],
                'engine': str(engine), 'private': str(job / 'grading'),
                'cohort': str(location / 'private/cohort.json'),
                'rules_path': '.rig/candidate.json', 'generated_id': 'candidate',
                'baseline_id': 'opengrep-default', 'frozen_files': bindings,
                'application_inputs': frozen['source_inputs'], 'diagnostic_job': str(job)}
    path = job / 'manifest.json'
    path.write_text(json.dumps(manifest))
    os.chdir(source)
    checkpoint(job, 'native_scan')
    proof = run(path)
    if proof.get('complete') is True:
        checkpoint(job, 'proof_validation')
    if any(sha(Path(p)) != digest for p, digest in bindings.items()):
        raise EvaluationError('case_construction_invalid')
    if sha(os.environ['RIG_EXECUTABLE']) != request['runtime_sha256'] or sha(engine) != request['engine_sha256']:
        raise EvaluationError('tool_changed')
    (job / 'proof.json').write_text(json.dumps(proof))


if __name__ == '__main__':
    try:
        evaluate(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4]), Path(sys.argv[5]))
    except BaseException as error:
        failure(Path(sys.argv[1]), error)
        sys.exit(2)  # Only validated checkpoint codes may enter the public response.
