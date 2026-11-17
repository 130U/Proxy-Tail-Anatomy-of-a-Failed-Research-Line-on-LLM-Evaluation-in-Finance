"""Collect independent ChatGPT-authenticated Codex sessions, without paid APIs.

Every prompt is passed on stdin unchanged. No resumed/forked session, no
correctness-dependent retry, no output repair. Tool use is disabled and audited.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import argparse
import json
import os
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parent
CODEX = Path('C:/Program Files/WindowsApps/OpenAI.Codex_26.1111.2228.0_x64__2p2nqsd0c76g0/app/resources/codex.exe')
DISABLED = ['shell_tool','apps','plugins','multi_agent','browser_use','browser_use_external',
            'computer_use','in_app_browser','image_generation','memories','shell_snapshot']


def utc():
    return datetime.now(timezone.utc).isoformat()


def artifact_paths(group, name):
    return {
        'raw': ROOT/'raw'/group/f'{name}.txt',
        'events': ROOT/'events'/group/f'{name}.jsonl',
        'stderr': ROOT/'events'/group/f'{name}.stderr',
        'call': ROOT/'calls'/group/f'{name}.json',
    }


def recovery_eligibility(record, paths):
    """A recovery is permitted only when no model answer was received."""
    if record.get('status') not in ('infrastructure_failure', 'infrastructure_timeout'):
        return False, 'not_a_terminal_infrastructure_failure'
    if not record.get('completed_utc'):
        return False, 'terminal_timestamp_missing'
    if record.get('tool_use_observed'):
        return False, 'tool_use_recorded'
    if not record.get('model') or not record.get('reasoning_effort'):
        return False, 'original_model_configuration_missing'
    if paths['raw'].exists() and paths['raw'].read_bytes().strip():
        return False, 'existing_response_bytes'
    recorded_types = set(record.get('event_item_types', []))
    if recorded_types - {'reasoning', 'error'}:
        return False, 'model_answer_or_tool_in_recorded_events'
    if record.get('usage'):
        return False, 'completed_turn_usage_present'
    if not paths['events'].exists():
        return False, 'event_log_missing_cannot_verify_no_answer'
    try:
        events = paths['events'].read_bytes().decode('utf8').splitlines()
        for line in events:
            if not line.strip():
                continue
            event = json.loads(line)
            if not isinstance(event, dict):
                return False, 'unrecognized_event_shape'
            kind = event.get('type')
            if kind == 'turn.completed':
                return False, 'completed_turn_in_event_log'
            if kind not in {'thread.started', 'turn.started', 'turn.failed', 'error', 'item.started', 'item.updated', 'item.completed'}:
                return False, 'unrecognized_event_type_cannot_verify_no_answer'
            item = event.get('item')
            if item is not None:
                if not isinstance(item, dict) or item.get('type') not in {'reasoning', 'error'}:
                    return False, 'model_answer_or_tool_in_event_log'
    except (UnicodeError, ValueError):
        return False, 'unparseable_event_log_cannot_verify_no_answer'
    return True, 'terminal_infrastructure_failure_with_no_model_answer'


def run_session(group, prompt, model, effort, timeout, recovery_record=None):
    name = prompt.stem
    paths = artifact_paths(group, name)
    raw, event, error, record_path = (paths[key] for key in ('raw', 'events', 'stderr', 'call'))
    for folder in [raw.parent,event.parent,record_path.parent]:
        folder.mkdir(parents=True,exist_ok=True)
    prompt_bytes = prompt.read_bytes()
    command = [str(CODEX),'exec','--ignore-user-config','--ephemeral','--skip-git-repo-check']
    for flag in DISABLED:
        command += ['--disable',flag]
    command += ['-c',f'model="{model}"','-c',f'model_reasoning_effort="{effort}"',
                '-c','service_tier="priority"',
                '-c','project_doc_max_bytes=0','-c','web_search="disabled"',
                '--sandbox','read-only','--cd',str(ROOT/'.runtime'),'--json',
                '-o',str(raw),'-']
    rec = {'group':group,'id':name,'model':model,'reasoning_effort':effort,
           'fresh_session':True,'auth':'existing ChatGPT login; no paid API',
           'prompt_file':prompt.relative_to(ROOT).as_posix(),'started_utc':utc(),
           'status':'started','command':command,'returncode':None,'attempt_number':1}
    if recovery_record:
        rec.update(recovery_record)
    record_path.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    start = time.monotonic()
    try:
        child_env = os.environ.copy()
        for credential in ('OPENAI_API_KEY', 'AZURE_OPENAI_API_KEY'):
            child_env.pop(credential, None)
        with event.open('wb') as out, error.open('wb') as err:
            proc = subprocess.run(command,input=prompt_bytes,stdout=out,stderr=err,
                                  timeout=timeout,creationflags=subprocess.CREATE_NO_WINDOW,
                                  env=child_env)
        rec['returncode'] = proc.returncode
        rec['status'] = 'completed' if proc.returncode == 0 and raw.exists() else 'infrastructure_failure'
    except subprocess.TimeoutExpired:
        rec['status'] = 'infrastructure_timeout'
    except Exception as exc:
        rec.update(status='infrastructure_failure',error=f'{type(exc).__name__}: {exc}')
    rec.update(completed_utc=utc(),elapsed_seconds=round(time.monotonic()-start,3))
    types = []
    for line in (event.read_text(encoding='utf8',errors='replace').splitlines() if event.exists() else []):
        try:
            item = json.loads(line)
        except ValueError:
            continue
        if item.get('type') == 'thread.started':
            rec['thread_id'] = item.get('thread_id')
        if item.get('type') == 'turn.completed':
            rec['usage'] = item.get('usage')
        if item.get('item',{}).get('type'):
            types.append(item['item']['type'])
        if item.get('type') in ['error','turn.failed']:
            rec.setdefault('errors',[]).append(item)
    rec['event_item_types'] = sorted(set(types))
    # Transport errors are runtime events, not model-invoked tools.
    rec['tool_use_observed'] = any(t not in ['agent_message','reasoning','error'] for t in types)
    if rec['tool_use_observed']:
        rec['status'] = 'protocol_violation_tool_use'
    record_path.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return {k:rec[k] for k in ['group','id','status','elapsed_seconds','tool_use_observed']}


def collect(group, prompt, model, effort, timeout, recover_infrastructure=False):
    name = prompt.stem
    paths = artifact_paths(group, name)
    if not paths['call'].exists():
        if recover_infrastructure:
            return {'group':group,'id':name,'status':'recovery_blocked','reason':'no_prior_failed_call'}
        if any(path.exists() for path in paths.values()):
            raise RuntimeError(f'Artifacts exist without a call record: {group}/{name}')
        return run_session(group, prompt, model, effort, timeout)
    if not recover_infrastructure:
        return {'group':group,'id':name,'status':'already_recorded'}
    record = json.loads(paths['call'].read_text(encoding='utf8'))
    allowed, reason = recovery_eligibility(record, paths)
    if not allowed:
        return {'group':group,'id':name,'status':'recovery_blocked','reason':reason}
    # The current collector and completed-answer records are never resumed or
    # altered. A per-item exclusive lock prevents duplicate recovery processes.
    lock = ROOT/'attempt_history'/group/name/'recovery.lock'
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        return {'group':group,'id':name,'status':'recovery_blocked','reason':'recovery_lock_exists'}
    try:
        with os.fdopen(lock_fd, 'wb') as stream:
            stream.write(json.dumps({'pid':os.getpid(),'started_utc':utc()}).encode('utf8'))
        record = json.loads(paths['call'].read_text(encoding='utf8'))
        allowed, reason = recovery_eligibility(record, paths)
        if not allowed:
            return {'group':group,'id':name,'status':'recovery_blocked','reason':reason}
        if record.get('prompt_file') != prompt.relative_to(ROOT).as_posix():
            return {'group':group,'id':name,'status':'recovery_blocked','reason':'original_prompt_path_mismatch'}
        # Keep the original model and effort even if CLI defaults name another
        # condition. This is transport recovery, not a new experimental arm.
        original_attempt = int(record.get('attempt_number', 1))
        archive = lock.parent/f'attempt_{original_attempt:03}'
        archive.mkdir(exist_ok=False)
        archived = {}
        filenames = {'call':'call.json','events':'events.jsonl','stderr':'stderr.txt','raw':'response.txt'}
        for key, path in paths.items():
            if path.exists():
                target = archive/filenames[key]
                shutil.copy2(path, target)
                archived[key] = target.relative_to(ROOT).as_posix()
            else:
                archived[key] = None
        # Check copied bytes before the new attempt writes canonical paths.
        for key, target in archived.items():
            if target is not None and paths[key].read_bytes() != (ROOT/target).read_bytes():
                raise RuntimeError('Failed-attempt preservation check failed')
        recovery_record = {
            'attempt_number':original_attempt+1,
            'infrastructure_recovery':True,
            'recovery_reason':reason,
            'previous_attempt_status':record['status'],
            'previous_attempt_artifacts':archived,
            'recovery_policy':'Fresh session, unchanged frozen prompt and original model/effort; previous attempt had no model answer. No quality/format-dependent retry.',
        }
        return run_session(group, prompt, record['model'], record['reasoning_effort'], timeout, recovery_record)
    finally:
        # Only the lock created by this invocation is removed; saved attempts
        # and all pre-existing inference artifacts are retained.
        lock.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--groups',default='')
    parser.add_argument('--reconcile-events',action='store_true')
    parser.add_argument('--recover-infrastructure',action='store_true',
                        help='Only retry terminal infrastructure failures with no received model answer; preserve every failed attempt.')
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--model',default='gpt-6-astra')
    parser.add_argument('--effort',default='ultra')
    parser.add_argument('--timeout',type=int,default=1200)
    parser.add_argument('--ids',default='')
    parser.add_argument('--c-half',action='store_true')
    args=parser.parse_args()
    if args.reconcile_events and args.recover_infrastructure:
        parser.error('Choose either event reconciliation or infrastructure recovery, not both')
    if args.reconcile_events:
        updated=[]
        for path in sorted((ROOT/'calls').glob('*/*.json')):
            rec=json.loads(path.read_text(encoding='utf8'))
            if rec.get('status') not in ('completed','protocol_violation_tool_use'):
                continue
            types=rec.get('event_item_types',[])
            tool_use=any(t not in ['agent_message','reasoning','error'] for t in types)
            if tool_use != rec.get('tool_use_observed'):
                rec['tool_use_observed']=tool_use
                if not tool_use and rec.get('returncode')==0 and rec.get('usage'):
                    rec['status']='completed'
                rec['event_classification_note']='Runtime error/transport-fallback events are not tool calls; original events and response unchanged.'
                path.write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
                updated.append(path.relative_to(ROOT).as_posix())
        print(json.dumps({'reclassified_transport_events':updated}))
        return
    if not args.groups:
        parser.error('--groups is required unless --reconcile-events is used')
    if not 1 <= args.workers <= 3:
        raise ValueError('At most three simultaneous inference sessions')
    ids=set(args.ids.split(',')) if args.ids else None
    half=set(json.loads((ROOT/'private/c_half_ids.json').read_text(encoding='utf8')))
    groups=args.groups.split(',')
    selected={g:[p for p in sorted((ROOT/'prompts'/g).glob('*.txt'))
                 if (ids is None or p.stem in ids) and (g!='C' or not args.c_half or p.stem in half)] for g in groups}
    if 'C' in selected:
        selected['C'].sort(key=lambda p:(p.stem not in half,p.stem))
    # Alternate conditions at each question index to reduce temporal confounding.
    tasks=[(g,selected[g][i]) for i in range(max(map(len,selected.values()),default=0))
           for g in groups if i<len(selected[g])]
    print(json.dumps({'jobs':len(tasks),'groups':{g:len(v) for g,v in selected.items()},
                      'model':args.model,'effort':args.effort,'workers':args.workers,
                      'recover_infrastructure':args.recover_infrastructure}),flush=True)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        future_map={pool.submit(collect,g,p,args.model,args.effort,args.timeout,args.recover_infrastructure):(g,p) for g,p in tasks}
        for future in as_completed(future_map):
            print(json.dumps(future.result(),ensure_ascii=False),flush=True)


if __name__=='__main__':
    main()
