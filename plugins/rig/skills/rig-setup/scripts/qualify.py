"""Independent single-use qualification; never imports author test claims."""
import concurrent.futures, hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
import tomllib


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def credit_lines(row):
    """Resolve declared exact statement anchors; ambiguity never gets credit."""
    source=Path(row['source']).read_text().splitlines();resolved=[]
    for value in row['credit_lines']:
        if type(value) is int and 1<=value<=len(source):resolved.append(value)
        elif isinstance(value,str):
            matches=[n for n,line in enumerate(source,1) if line==value]
            if len(matches)!=1:raise RuntimeError('Finding attribution anchor missing or ambiguous')
            resolved.append(matches[0])
        else:raise RuntimeError('Invalid finding attribution')
    if not resolved:raise RuntimeError('Finding attribution missing')
    return resolved
def context(root, manifest, baseline):
    # Reusing a sealed result is safe only for the same source/tools/grader/pack.
    # Changed source needs a newly generated independent cohort, not a cached pass.
    names=subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=root).decode().split('\0')
    sources={p:sha(root/p) for p in names if p and not p.startswith('.rig/') and (root/p).is_file()}
    return {'sources':sources,'baseline':baseline,'baseline_sha256':sha(root/baseline['opengrep_rules']),
            'frozen_files':manifest['frozen_files'],'rig':sha(manifest['rig']),'engine':sha(manifest['engine'])}
def retain(result, directory):
    """Keep the real Rig engine artifacts before isolated case roots disappear."""
    evidence=result.get('receipt',{}).get('evidence',{})
    retained={}
    for kind in ('raw','sarif'):
        path=evidence.get(kind+'_path');digest=evidence.get(kind+'_digest')
        if not path or not digest:raise RuntimeError('Native scan evidence missing')
        source=Path(path)
        if sha(source)!=digest:raise RuntimeError('Native scan evidence integrity mismatch')
        directory.mkdir(parents=True,exist_ok=True)
        target=directory/source.name;shutil.copy2(source,target)
        if sha(target)!=digest:raise RuntimeError('Retained native artifact integrity mismatch')
        retained[kind]={'path':str(target),'sha256':digest,'original_path':path}
    result['retained_evidence']=retained
def native(rig, engine, rules, source, row, work):
    target=row['target']
    app=work/row['id'];app.mkdir(parents=True)
    dest=app/target;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(row['source'],dest)
    # Full real caller file is scanned; execute through ordinary Rig project checks.
    (app/'.rig').mkdir();shutil.copy2(rules,app/'.rig/rules.yaml')
    definition={'schema_version':1,'checks':[{'id':'qualification','source':'.rig/rules.yaml','statement':'Independent full caller qualification',
        'argv':[engine,'scan','--config','.rig/rules.yaml','--error','--strict','--json','--disable-version-check','--verbose',target],
        'authority':'candidate','mode':'advisory','owner':'independent coordinator','read_only':True,'execution_path':'/opt/homebrew/bin:/usr/bin:/bin',
        'env':{},'timeout_ms':20000,'output_limit_bytes':1048576,'paths':[target],'inputs':['**'],'opengrep_rules':'.rig/rules.yaml'}]}
    # Use serde-compatible TOML via the already installed dependency in controller.
    c=definition['checks'][0]
    text='schema_version = 1\n[[checks]]\n'+''.join(k+' = '+(str(v).lower() if isinstance(v,bool) else json.dumps(v))+'\n' for k,v in c.items())
    (app/'.rig/checks.toml').write_text(text)
    subprocess.run(['git','init','-q',str(app)],check=True,capture_output=True)
    env=dict(os.environ,RIG_HOME=str(app.parent/(row['id']+'-state')),PYTHONDONTWRITEBYTECODE='1',
             SEMGREP_ENABLE_VERSION_CHECK='0',SEMGREP_SEND_METRICS='off')
    registration=subprocess.run([rig,'scanner','register',engine,'--name','independent-native','--rules',str(rules),'--application-model','off'],env=env,capture_output=True,text=True,timeout=20)
    if registration.returncode:raise RuntimeError('Native scanner registration failed: '+registration.stderr)
    p=subprocess.run([rig,'checks','run','--id','qualification'],cwd=app,env=env,capture_output=True,text=True,timeout=35)
    try:
        receipt=json.loads(p.stdout)
        findings=receipt.get('findings',[])
        complete=bool(p.returncode in [0,1] and receipt.get('executed') is True and receipt.get('freshness')=='current' and receipt.get('execution_status')=='completed' and receipt.get('logs_truncated') is False and receipt.get('scanned_files',0)>0 and receipt.get('state') in ['satisfied','violation'] and not receipt.get('diagnostics') and receipt.get('engine_version'))
        hit=any(f['path'].endswith(target) and f['line'] in credit_lines(row) for f in findings)
    except (ValueError,KeyError,TypeError):receipt={};findings=[];complete=False;hit=False
    return {'complete':complete,'hit':hit,'findings':findings,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'receipt':receipt}

def authorize_and_run(invoke,ident):
    """Normal public CLI JSON is the default; approval grants execution only."""
    review=invoke(['checks','review','--id',ident])
    if not review.get('execution_approved'):
        invoke(['checks','approve','--id',ident,'--digest',review['approval_digest']])
    return invoke(['checks','run','--id',ident])
def adopt_qualified(invoke,ident):
    """Consume current qualification and normal advisory policy under setup auth."""
    q=invoke(['setup','--qualification',ident]) # Failed qualification stops before any policy action.
    try:
        invoke(['setup','--qualification',ident,'--apply','--digest',q['proposal_digest']])
    except RuntimeError:
        pass # An already sealed check can still need policy adoption; failed gates refuse below.
    p=invoke(['checks','policy-review','--id',ident,'--mode','advisory'])
    return invoke(['checks','activate','--id',ident,'--mode','advisory','--owner','Rig setup authorization','--digest',p['policy_digest']])

def existing(m):
    """Test unchanged existing protection before writing any application rule."""
    root=Path.cwd();out=Path(m['private']);out.mkdir(exist_ok=True)
    config=tomllib.loads((root/'.rig/checks.toml').read_text())
    baseline=next(c for c in config['checks'] if c['id']==m['baseline_id'])
    if baseline.get('application_model'):raise RuntimeError('Existing models require their compatible verifier, never omission')
    rules=root/baseline['opengrep_rules']
    for path,digest in m['frozen_files'].items():
        if sha(path)!=digest:raise RuntimeError('Frozen existing-rule evidence changed')
    for path,digest in m.get('application_inputs',{}).items():
        if sha(root/path)!=digest:raise RuntimeError('Application changed before existing-rule qualification')
    bound=context(root,m,baseline);spent=out/'existing-spent.json';final=out/'existing-proof.json'
    if spent.exists():
        if json.loads(spent.read_text())!=bound or not final.exists():raise RuntimeError('Existing collection changed/incomplete; no retry')
        return json.loads(final.read_text())
    spent.write_text(json.dumps(bound))
    cohort=json.loads(Path(m['cohort']).read_text());cases=[];raw=[]
    with tempfile.TemporaryDirectory(prefix='rig-existing-native-') as name:
        for row in cohort['cases']:
            if sha(row['source'])!=row['sha256']:raise RuntimeError('Existing case changed')
            credit_lines(row)
            if not any(__import__('fnmatch').fnmatchcase(row['target'],p) or p=='**' for p in baseline['paths']):raise RuntimeError('Existing scanner scope does not cover this target')
            base=native(m['rig'],m['engine'],rules,root,row,Path(name))
            if base['complete']:retain(base,out/'native-evidence'/row['id'])
            cases.append({'id':row['id'],'expected':row['expected'],'error':not base['complete'],
                          'caught':base['hit'] if row['expected']=='vulnerable' else None,
                          'attributed':base['hit'] if row['expected']=='vulnerable' else None,
                          'alarm':base['hit'] if row['expected']=='safe' else None})
            raw.append({'case':row,'baseline':base});(out/'raw-existing.json').write_text(json.dumps(raw,indent=2))
    value={'schema_version':1,'kind':'app_existing_qualification','complete':len(cases)==len(cohort['cases']) and not any(c['error'] for c in cases),
           'native_rig':True,'independent':True,'rules_sha256':sha(rules),'cases':cases,
           'targets':sorted({c['target'] for c in cohort['cases']}),'cohort_sha256':sha(m['cohort']),
           'independence':'Separate source-only runtime cases; finite tested operation scope, not category coverage'}
    final.write_text(json.dumps(value,indent=2));return value

def run(manifest):
    m=json.loads(manifest.read_text())
    if m.get('purpose')=='existing':return existing(m)
    root=Path.cwd();out=Path(m['private']);out.mkdir(exist_ok=True)
    rules=root/m.get('rules_path',f".rig/corrections/{m['generated_id']}/rule.json")
    candidate_sha=sha(rules)
    purpose=m.get('purpose','qualification')
    if purpose not in ['qualification','development']:raise RuntimeError('Unknown suite purpose')
    semantic=hashlib.sha256(json.dumps(json.loads(rules.read_text()),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    base_out=out
    if purpose=='development':
        limit=m.get('max_development_runs')
        if limit is not None and len(list(out.glob('run-*')))>=limit:raise RuntimeError('Development attempt budget exhausted; freeze or leave inactive and continue')
        import time
        out=out/('run-'+str(time.time_ns()));out.mkdir()
    else:
        prerequisite=m.get('development_report')
        if prerequisite:
            dev=json.loads(Path(prerequisite).read_text())
            passed=dev.get('complete') is True and dev.get('rules_semantic_sha256')==semantic and all(
                c.get('error') is False and ((c['expected']=='vulnerable' and c.get('caught') is True and c.get('attributed') is True) or (c['expected']=='safe' and c.get('alarm') is False)) for c in dev.get('cases',[]))
            if not passed:raise RuntimeError('Public development suite must pass completely before opening independent cases')
    config=tomllib.loads((root/'.rig/checks.toml').read_text());baseline=next(c for c in config['checks'] if c['id']==m.get('baseline_id','opengrep-default'))
    if baseline.get('application_model'):
        raise RuntimeError('This local-rule fixture runner cannot omit an application model; use the existing compatible model verification path')
    baseline_file=root/baseline['opengrep_rules']
    review=rules.with_name('review.json')
    if purpose=='qualification' and review.exists():
        metadata=json.loads(review.read_text())
        if metadata.get('setup_generation') is True and metadata['behavior_evidence']['baseline_rules_sha256']!=sha(baseline_file):
            raise RuntimeError('Candidate behavior baseline differs from evaluator baseline; collection remains unopened. Anchor the baseline_check reported by public development before generating a candidate.')
    for path,h in m['frozen_files'].items():
        if sha(path)!=h:raise RuntimeError('Frozen verifier/case/runtime changed: '+path)
    for path,h in m.get('application_inputs',{}).items():
        if sha(root/path)!=h:raise RuntimeError('Application changed since evaluation construction; automatically prepare a new generation')
    current_context=context(root,m,baseline)
    spent=out/'qualification-spent.json'
    if purpose=='qualification' and spent.exists():
        previous=json.loads(spent.read_text())
        if previous['rules_sha256']!=candidate_sha:raise RuntimeError('Cohort spent; revised candidate cannot reuse independent cases')
        if previous.get('context')!=current_context:raise RuntimeError('Qualification context stale; automatically prepare a new evaluation generation')
        final=out/'qualification-proof.json'
        if not final.exists():raise RuntimeError('Incomplete spent collection; no retry')
        return json.loads(final.read_text())
    cohort=json.loads(Path(m['cohort']).read_text())
    for row in cohort['cases']:
        if sha(row['source'])!=row['sha256']:raise RuntimeError('Frozen case source changed')
        credit_lines(row)
    if purpose=='qualification':
        with spent.open('x') as f:json.dump({'rules_sha256':candidate_sha,'cohort_sha256':sha(m['cohort']),'context':current_context,'started':True},f)
    shutil.copy2(rules,out/'frozen-candidate.json')
    combined=out/'combined.json'
    candidate=json.loads(rules.read_text())
    baseline_text=baseline_file.read_text()
    try:
        original=json.loads("\n".join(line for line in baseline_text.splitlines() if not line.lstrip().startswith("#")))
        original_ids=[r['id'] for r in original['rules']]
        combined.write_text(json.dumps({'rules':original['rules']+candidate['rules']}))
    except ValueError:
        import re
        assert baseline_text.startswith('rules:'),'Independent checker requires a local rules-only pack'
        original_ids=re.findall(r'^\s*-?\s*id:\s*(\S+)',baseline_text,re.M)
        combined.write_text(baseline_text.rstrip()+'\n'+'\n'.join('- '+json.dumps(r) for r in candidate['rules'])+'\n')
    ids=original_ids+[r['id'] for r in candidate['rules']]
    if len(ids)!=len(set(ids)):raise RuntimeError('Candidate duplicates an existing protective rule')
    cases=[];raws=[]
    with tempfile.TemporaryDirectory(prefix='rig-independent-native-') as name:
        work=Path(name)
        def one(row):
            base=native(m['rig'],m['engine'],baseline_file,root,row,work/'baseline')
            revised=native(m['rig'],m['engine'],combined,root,row,work/'candidate')
            if base['complete']:retain(base,out/'native-evidence'/row['id']/'baseline')
            if revised['complete']:retain(revised,out/'native-evidence'/row['id']/'candidate')
            return row,base,revised
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for row,base,revised in pool.map(one,cohort['cases']):
                error=not(base['complete'] and revised['complete'])
                # Safe controls reject ANY new candidate finding on the real caller,
                # including mistaken attribution elsewhere; baseline extras retained.
                own=[f for f in revised['findings'] if any(f['rule_id']==r['id'] or f['rule_id'].endswith('.'+r['id']) for r in candidate['rules'])]
                cases.append({'id':row['id'],'expected':row['expected'],'error':error,'caught':revised['hit'] if row['expected']=='vulnerable' else None,
                    'attributed':revised['hit'] if row['expected']=='vulnerable' else None,'alarm':bool(own) if row['expected']=='safe' else None,
                    'baseline_missed':row['expected']=='vulnerable' and not base['hit'] and base['complete']})
                raws.append({'case':row,'baseline':base,'candidate':revised})
                (out/'raw-results.json').write_text(json.dumps(raws,indent=2))
    value={'schema_version':1,'kind':'app_rule_qualification','complete':len(cases)==len(cohort['cases']) and not any(c['error'] for c in cases),
        'native_rig':True,'independent':purpose=='qualification','rules_semantic_sha256':semantic,'rules_sha256':candidate_sha,'baseline_check':baseline['id'],'baseline_rules_sha256':sha(baseline_file),
        'baseline_missed':sum(c['baseline_missed'] for c in cases),'cases':cases,'targets':sorted({c['target'] for c in cohort['cases']}),
        'cohort_sha256':sha(m['cohort']),'independence':'Separately prepared runtime-effect cases withheld from author; finite automated evidence, not semantic infallibility or hostile containment.'}
    (out/'qualification-proof.json').write_text(json.dumps(value,indent=2))
    if purpose=='development':(base_out/'latest.json').write_text(json.dumps(value,indent=2))
    return value
if __name__=='__main__':
    try:print(json.dumps(run(Path(sys.argv[1]))))
    except Exception as e:
        print(json.dumps({'schema_version':1,'kind':'app_rule_qualification','complete':False,'error':str(e)}));sys.exit(1)
