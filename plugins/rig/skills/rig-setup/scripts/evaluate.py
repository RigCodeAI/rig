"""Prepare independent behavior-checked data in a fresh native agent session.

Opt-in setup step, never imported by Cargo/CI. No repository-specific fixtures
or verifier program are inputs. The worker cannot read author rules/history.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib

from native_host import auth_copy, bounded, environment, preflight
from qualify import sha, credit_lines


TASK = '''Act as the independent security evaluator for an authorized Rig setup.
You have repository SOURCE and the existing protective rule pack only. No rule
author conversation, candidate rules, or prior evaluations are available.
Inspect the application, its actual helpers/callers/configuration and inventory
OWASP Top 10 2025 concerns: A01 Broken Access Control, A02 Security
Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures,
A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or
Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling
of Exceptional Conditions. Use these IDs/edition; do not substitute 2021.
Choose ONE useful application-specific gap in the existing
rules whose security semantics you can verify with available local tools. Choose
primary application code rather than auxiliary evaluation/build tooling. Do not
infer security from API names or invent business policy. Unknowns stay unknown.
Prefer a concrete dangerous operation/transfer with observable runtime evidence.
If an obligation depends on recognizing arbitrary possible validation logic that
cannot be established, mark that limitation rather than inventing a general
missing-guard policy. Mocks may record calls or inject boundary failures; never
implement the vulnerability mechanism inside a mock to manufacture an effect.
Use the relevant real parser/interpreter/operation where the claim requires it;
otherwise keep that claim unknown and choose a soundly testable gap.

Write these artifacts in OUTPUT:
* inventory.json: all ten OWASP categories with observed evidence locations,
  applicability/unknowns; selected gap, helper semantics, scope and limitations.
* public/facts.json: observed helper semantics and selected gap for the author,
  without private cases or descriptions of their syntactic variations.
* public/cohort.json and private/cohort.json, each {"cases":[...]}. Each row has
  id (unique across BOTH sets, alphanumeric/hyphen), source (absolute regular file
  under that split's cases/ directory), target (actual relative source path in
  repository), expected (vulnerable or safe), credit_lines (nonempty 1-based line
  numbers OR unique exact whole source-line strings where alarms must be
  attributed), sha256 (file bytes). Each source is a FULL
  actual caller file variant, preserving real imports/helpers/context. Include
  at least 4 vulnerable and 4 safe cases PER split. Use distinct semantic forms,
  propagation, aliases, unused/overwritten data and legitimate alternatives.
  Safe controls must preserve useful ordinary behavior, not just disable it.
  Do not author scanner rules. Do not give private cases to the author.
* verify.py: executable independent stdlib/native-runtime behavior oracle, with
  no scanner, network, model or installation. Run it from OUTPUT. It must execute
  real repository helper behavior and the relevant operation in EVERY case,
  contrast malicious/ordinary inputs, and verify observable effects/outputs.
  Stub external services at the operation boundary only; do not replace the helper
  semantics being tested. Use temporary sentinels and controlled sinks, never real
  destructive operations or providers. Syntax/name matching is not a runtime
  oracle. Store runtime-results.json {"complete":true,"cases":[{"id":..., 
  "source_sha256":...,"observed":"vulnerable"|"safe", 
  "ordinary_behavior":true,"evidence":...}]}. Exit nonzero on any mismatch,
  missing execution or unknown. Verify all labels independently of scanner output.

Source is read-only at SOURCE; installed tools/rule pack are read-only at BASELINE.
Only OUTPUT and temporary files are writable. No package installation, external
service calls, credentials, other agents or history. You may create your own
temporary harnesses and fix invalid case construction BEFORE freezing. Run your
oracle and ensure every emitted row is behavior-checked. If no sound gap can be
tested, save inventory with unknowns and stop with failure; never fabricate proof.
The controller reruns your oracle after you exit and freezes the data. The rule
author will receive only public/ and source. No engineer will repair your output.
'''


INVENTORY_TASK = '''Inspect repository SOURCE and existing protection BASELINE for authorized multi-gap Rig setup.
This is discovery, not rule writing or qualification. Write the initial valid
worklist-plan.json IMMEDIATELY after inspecting top-level manifests: all ten
categories unknown with honest reasons, and an empty gaps array. Then update it
incrementally as each concrete obligation is identified. Do not defer all artifact
writing until the end. Reserve at least half the declared session budget for
writing, validating and finishing. Inspect primary application
features, real helpers/callers and existing protective rules. Account for OWASP
Top 10 2025 A01..A10. Write OUTPUT/worklist-plan.json with operation=plan,
inventory=[{category:A01..A10,applicability:applicable|unknown|not_applicable|outside_app_layer,reason:source-grounded explanation}],
gaps=[{id:stable-hyphen-ID,statement:concrete obligation,gap:existing shortfall or
existing coverage to independently check,categories:[Axx,...],paths:[actual relative
caller source files],applicability:same enum,reason:source evidence,limitations:unknowns}].
Identify ALL concrete applicable app-layer obligations you find, not just one or
one per category. Group overlapping obligations; one check can cover several
categories and a category can have multiple gaps. Do not invent business policy.
Inventory/tags/rule presence/zero findings are not verified coverage. Existing
rules are tested first by a separate runtime evaluator; identify likely reusable
protection without claiming it verified. Dependency CVEs are outside app-layer
scope. Unavailable runtimes or untestable behavior stay unknown/unsupported, not
not-applicable. No scanner rules, tests, cases or verifier program are needed in
this discovery step. No installs, network, providers, other agents or credentials.
Only OUTPUT and temporary files writable. Source only: no author conversations,
old test forms or grading results. Return a finite worklist; budgets are assigned
by the controller, not the inventory. Saved obligation metadata, if supplied,
contains no test/rule forms: preserve it with prior_check and the EXACT saved gap
text, rather than rerolling failed checks. Do not supply passing status labels.
'''

def validate_plan(output,project):
    value=json.loads((Path(output)/'worklist-plan.json').read_text())
    categories=value.get('inventory',[])
    if len(categories)!=10 or {c['category'] for c in categories}!={f'A{n:02}' for n in range(1,11)}:raise RuntimeError('Account for all ten categories')
    ids=set()
    for gap in value.get('gaps',[]):
        if gap['id'] in ids:raise RuntimeError('Duplicate obligation')
        ids.add(gap['id'])
        for path in gap['paths']:
            p=Path(path)
            if p.is_absolute() or '..' in p.parts or not (Path(project)/p).is_file():raise RuntimeError('Gap must cite actual source files')
    if len(ids)>128:raise RuntimeError('Worklist inventory bound exceeded')
    return value


def validate(output, project):
    """Validate data and join every label to a separate runtime observation."""
    output, project = Path(output).resolve(), Path(project).resolve()
    inventory = json.loads((output / 'inventory.json').read_text())
    if not inventory.get('selected_gap'):
        raise RuntimeError('Evaluator did not establish a useful gap')
    runtime = json.loads((output / 'runtime-results.json').read_text())
    if runtime.get('complete') is not True:
        raise RuntimeError('Independent runtime observations incomplete')
    observations = runtime.get('cases', [])
    ids = [row['id'] for row in observations]
    if len(ids) != len(set(ids)):
        raise RuntimeError('Duplicate runtime observation')
    observed = {row['id']: row for row in observations}
    seen = set()
    for split in ('public', 'private'):
        rows = json.loads((output / split / 'cohort.json').read_text())['cases']
        for label in ('vulnerable', 'safe'):
            if sum(r['expected'] == label for r in rows) < 4:
                raise RuntimeError('Both independently tested classes require at least four cases')
        for row in rows:
            ident = row['id']
            if not ident or not all(c.isalnum() or c == '-' for c in ident) or ident in seen:
                raise RuntimeError('Invalid/duplicate case identity')
            seen.add(ident)
            source = Path(row['source'])
            target = Path(row['target'])
            if source.is_symlink() or not source.resolve().is_relative_to(output / split / 'cases'):
                raise RuntimeError('Case source escaped its split')
            if target.is_absolute() or '..' in target.parts or not (project / target).is_file():
                raise RuntimeError('Case target is not actual repository source')
            if sha(source) != row['sha256']:
                raise RuntimeError('Case source identity mismatch')
            credit_lines(row)
            proof = observed.get(ident, {})
            if (proof.get('source_sha256') != row['sha256'] or
                proof.get('observed') != row['expected'] or
                proof.get('ordinary_behavior') is not True or not proof.get('evidence')):
                raise RuntimeError('Case lacks matching runtime security/ordinary-behavior evidence')
    if seen != set(observed):
        raise RuntimeError('Runtime/case denominator mismatch')
    return {'complete': True, 'cases': len(seen), 'inventory': inventory,
            'bindings': {str(p.relative_to(output)): sha(p) for p in output.rglob('*')
                         if p.is_file() and p.name not in ('freeze.json',)}}


def prepare(project, output, baseline, seconds=900, focus=None, inventory=False, saved_obligations=None):
    if sys.platform != 'darwin':
        raise RuntimeError('Independent native evaluator currently requires macOS sandbox-exec')
    project, archive, baseline = map(lambda p: Path(p).resolve(), (project, output, baseline))
    if archive.exists():
        raise RuntimeError('Preserve evaluation generations; output must be new')
    archive.mkdir(parents=True)
    # The native worker sees a source-only copy, never .rig or earlier agent data.
    state = Path(tempfile.mkdtemp(prefix='rig-setup-evaluator-')).resolve()
    output = state / 'evaluation'; output.mkdir()
    (archive/'location.json').write_text(json.dumps({'evaluation': str(output)}))
    source = state / 'source'
    shutil.copytree(project, source, symlinks=True, ignore=shutil.ignore_patterns(
        '.git', '.rig', '.agents', '.claude', '.codex', '__pycache__',
        '.venv', 'node_modules', 'target', 'task-artifacts',
        'AGENTS.md', 'CLAUDE.md', 'GEMINI.md'))
    if any(p.is_symlink() for p in source.rglob('*')):
        raise RuntimeError('Source symlinks are unsupported; evaluator will not follow external inputs')
    source_inputs = {str(p.relative_to(source)): sha(p) for p in source.rglob('*') if p.is_file()}
    tools = state / 'baseline.yaml'; shutil.copy2(baseline, tools)
    obligation = None
    if focus:
        prior = json.loads(Path(focus).read_text())
        obligation = {k: prior[k] for k in ('statement', 'gap', 'paths', 'limitations') if k in prior}
        if not obligation.get('statement') or not obligation.get('paths'):
            raise RuntimeError('Revalidation focus needs the saved obligation and scope, never authored rules/cases')
    profile = state / 'profile'; profile.mkdir()
    for name in ('tmp', 'home'): (state / name).mkdir()
    default_home = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex')))
    auth_copy(default_home / 'auth.json', profile / 'auth.json')
    configured = tomllib.loads((default_home / 'config.toml').read_text())
    config = 'forced_login_method="chatgpt"\ncli_auth_credentials_store="file"\nmodel_provider="openai"\napproval_policy="on-request"\nsandbox_mode="workspace-write"\n'
    for key in ('model', 'model_reasoning_effort'):
        if key in configured: config += key + '=' + json.dumps(configured[key]) + '\n'
    config += '[features]\nmulti_agent=false\nmemories=false\nremote_plugin=false\n'
    (profile / 'config.toml').write_text(config)
    host = Path(shutil.which('codex')).resolve()
    env = environment(profile, state / 'rig-home')
    env.update(HOME=str(state / 'home'), TMPDIR=str(state / 'tmp'))
    q = lambda p: json.dumps(str(Path(p).resolve()))
    # Source-copy parent instructions/history cannot leak across the role boundary.
    policy = state / 'worker.sb'
    policy.write_text('(version 1)\n(allow default)\n(deny file-read* (subpath '+q(project)+') (subpath '+q(default_home)+'))\n(deny file-write*)\n'+
        ''.join('(allow file-write* (subpath '+q(p)+'))\n' for p in (output, profile, state/'tmp', state/'home'))+
        '(allow file-write* (literal "/dev/null") (literal "/dev/tty"))\n')
    prompt = (INVENTORY_TASK if inventory else TASK).replace('OUTPUT', str(output)).replace('SOURCE', str(source)).replace('BASELINE', str(tools))
    protocol = state / 'protocol'; protocol.mkdir()
    for script in ('evaluate.py', 'native_host.py', 'qualify.py'):
        shutil.copy2(Path(__file__).parent/script, protocol/script)
    if inventory and saved_obligations:
        prompt += '\nSaved obligation metadata (no rules or test forms): '+json.dumps(saved_obligations)
    prompt += '\nTotal session budget: '+str(seconds)+' seconds. Write valid artifacts early; do not exhaust the budget on reading.\n'
    prompt += '\nBefore finishing, run the existing protocol validator and fix any invalid construction yourself: '+str(sys.executable)+' -B '+str(protocol/'evaluate.py')+(' --validate-plan' if inventory else ' --validate')+' --project '+str(source)+' --output '+str(output)+'\nThis validates data only and starts no model or scanner.\n'
    if obligation:
        prompt += '\nRevalidate this saved obligation on CURRENT source (not a new unrelated gap). Treat its assumptions as untrusted; establish semantics again. Include regressions even if current source is safe. No previous rule or cases are supplied:\n'+json.dumps(obligation)
    cell = archive / 'session'; cell.mkdir()
    controls = archive / 'controls'; controls.mkdir()
    for script in ('evaluate.py', 'native_host.py', 'qualify.py'):
        shutil.copy2(Path(__file__).parent/script, controls/script)
    try:
        status = preflight(host, env, configured.get('model'))
        (cell / 'preflight.json').write_text(json.dumps(status, indent=2))
        args = ['/usr/bin/sandbox-exec', '-f', str(policy), str(host), 'exec',
                '--ephemeral', '--skip-git-repo-check', '--approve-for-me', '--json',
                '--add-dir', str(state/'tmp'), '-C', str(output), prompt]
        (cell/'request.json').write_text(json.dumps({'argv': args, 'fresh': True, 'author_context': False}))
        result = bounded(args, source, env, cell, cap=seconds)
        (cell/'result.json').write_text(json.dumps(result))
        if not inventory and (result['status'] != 'completed' or result['exit_code'] != 0):
            raise RuntimeError('Independent evaluator session did not complete')
        if inventory:
            plan=validate_plan(output,project)
            finished=result['status']=='completed' and result['exit_code']==0
            plan['discovery']={'complete':finished,'status':result['status'],'seconds':result['seconds'],'scope':'Bounded source discovery; uninspected obligations remain unknown. Inventory is not verified coverage.'}
            if any(sha(project/p)!=h for p,h in source_inputs.items()):raise RuntimeError('Source changed during discovery')
            shutil.copytree(output,archive/'artifacts')
            return {'complete':True,'cases':0,'evaluation':str(output),'plan':plan}
        # Rerun separately; no scanner output or author assertion supplies labels.
        oracle_policy = state / 'oracle.sb'
        oracle_policy.write_text(policy.read_text()+'\n(deny network*)\n')
        p = subprocess.run(['/usr/bin/sandbox-exec', '-f', str(oracle_policy),
                            sys.executable, '-B', str(output/'verify.py')],
                           cwd=output, env=env, capture_output=True, text=True, timeout=120)
        (output/'runtime-verification.log').write_text(p.stdout+'\n'+p.stderr)
        if p.returncode: raise RuntimeError('Independent behavior oracle failed after session exit')
        frozen = validate(output, project)
        if any(not (project/p).is_file() or sha(project/p) != h for p,h in source_inputs.items()):
            raise RuntimeError('Application changed during independent evaluation construction')
        frozen.update(source_inputs=source_inputs, source_root=str(source))
        (output/'freeze.json').write_text(json.dumps(frozen, indent=2))
        shutil.copytree(output, archive/'artifacts')
        frozen['evaluation'] = str(output)
        return frozen
    finally:
        (profile/'auth.json').unlink(missing_ok=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--baseline', type=Path)
    p.add_argument('--validate', action='store_true')
    p.add_argument('--validate-plan', action='store_true')
    p.add_argument('--inventory', action='store_true')
    p.add_argument('--saved-obligations',type=Path)
    p.add_argument('--seconds', type=int, default=900)
    p.add_argument('--focus', type=Path)
    a = p.parse_args()
    if a.validate_plan:
        validate_plan(a.output,a.project);print(json.dumps({'complete':True}));sys.exit(0)
    if a.validate:
        checked = validate(a.output, a.project)
        print(json.dumps({'complete': checked['complete'], 'cases': checked['cases']}))
        sys.exit(0)
    if a.baseline is None:p.error('--baseline required for independent preparation')
    result = prepare(a.project, a.output, a.baseline, a.seconds, a.focus,a.inventory,json.loads(a.saved_obligations.read_text()) if a.saved_obligations else None)
    # The invoking rule author must not receive private inventory/variation data.
    # Generic manifest construction can load hash fields programmatically without
    # displaying the oracle, private source or runtime observations to the model.
    location = Path(result['evaluation'])
    if a.inventory:
        print(json.dumps({'complete': result['complete'], 'plan': str(location/'worklist-plan.json')}))
        sys.exit(0)
    print(json.dumps({'complete': result['complete'], 'cases': result['cases'],
                      'public': str(location/'public'),
                      'evaluation_metadata': str(location/'freeze.json'),
                      'private_cohort': str(location/'private/cohort.json')}))
