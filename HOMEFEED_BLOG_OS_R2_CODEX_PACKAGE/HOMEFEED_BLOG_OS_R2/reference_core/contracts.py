"""Executable deterministic reference checks. No network, DB or LLM calls.
A passing result does NOT establish factual accuracy, naturalness, licenses or virality.
Reports passed to assess_handoff must be loaded by an authenticated server from its
review store, never accepted as client/writer assertions. DB enforcement is separate.
"""
from __future__ import annotations
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
from urllib.parse import urlsplit
from dataclasses import dataclass
from typing import Any
import json,ipaddress,math,re,unicodedata
import jsonschema
from .canonical import content_hash
ROOT=Path(__file__).resolve().parents[1]
DEFS=json.loads((ROOT/'schemas/domain.schema.json').read_text())['$defs']

class Violation(ValueError):
    def __init__(self,code:str,detail:str=''):
        self.code=code;super().__init__(code+(': '+detail if detail else ''))

def require(ok:bool,code:str,detail:str='')->None:
    if not ok:raise Violation(code,detail)

def instant(value:str)->datetime:
    try:
        d=datetime.fromisoformat(value.replace('Z','+00:00'))
        require(d.tzinfo is not None,'TIMEZONE_REQUIRED')
        return d.astimezone(timezone.utc)
    except (TypeError,ValueError) as e:
        if isinstance(e,Violation):raise
        raise Violation('INVALID_TIME') from e

def web_url(url:str)->str:
    require(isinstance(url,str) and not any(ord(c)<33 for c in url),'URL_CONTROL')
    try:
        p=urlsplit(url);port=p.port
        require(p.scheme in ('https','http') and bool(p.hostname),'URL_SCHEME')
        require(p.username is None and p.password is None,'URL_CREDENTIALS')
        h=p.hostname.encode('idna').decode('ascii').lower().rstrip('.')
    except (UnicodeError,ValueError) as e:raise Violation('URL_INVALID') from e
    require('\\' not in url,'URL_BACKSLASH')
    require(h not in ('localhost',) and not h.endswith(('.local','.localhost')),'URL_LOCAL_HOST')
    try:ip=ipaddress.ip_address(h)
    except ValueError:pass
    else:require(ip.is_global and not ip.is_multicast,'URL_NONPUBLIC_IP')
    return h

def fetch_guard(url:str,allowed_hosts:list[str],resolved_addresses:list[str])->None:
    """Call on every redirect and after DNS; egress/proxy enforcement still required."""
    host=web_url(url)
    normalized=[h.encode('idna').decode('ascii').lower().rstrip('.') for h in allowed_hosts]
    require(host in normalized,'HOST_NOT_ALLOWED')
    require(bool(resolved_addresses),'DNS_UNRESOLVED')
    for addr in resolved_addresses:
        try:ip=ipaddress.ip_address(addr)
        except ValueError as e:raise Violation('DNS_INVALID') from e
        require(ip.is_global and not ip.is_multicast,'DNS_NONPUBLIC')

def safe_path(value:str)->str:
    require(isinstance(value,str) and value!='','FILE_PATH_EMPTY')
    require(not any(ord(c)<32 or ord(c)==127 for c in value),'FILE_PATH_CONTROL')
    require('\\' not in value and ':' not in value and not value.startswith('/'),'FILE_PATH_UNSAFE')
    require(not any(c in value for c in '"<>|?*%#'),'FILE_PATH_RESERVED_CHAR')
    require(all(p not in ('','.','..') for p in value.split('/')),'FILE_PATH_TRAVERSAL')
    for part in value.split('/'):
        require(not part.endswith((' ','.')),'FILE_PATH_WINDOWS_ALIAS')
        stem=part.split('.')[0].upper()
        require(stem not in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))},'FILE_PATH_WINDOWS_RESERVED')
    return unicodedata.normalize('NFC',value).casefold()

def unique(values:list[Any],code:str)->None:require(len(values)==len(set(values)),code)

def validate(name:str,obj:dict[str,Any])->None:
    try:jsonschema.Draft202012Validator({'$defs':DEFS,'$ref':'#/$defs/'+name},format_checker=jsonschema.FormatChecker()).validate(obj)
    except jsonschema.ValidationError as e:raise Violation('SCHEMA_'+name,str(e.message)[:180]) from e
    if name=='EvidenceItem':require(instant(obj['valid_until'])>instant(obj['verified_at']),'EVIDENCE_INTERVAL')
    if name=='Claim':
        if obj['verified_at'] and obj['valid_until']:require(instant(obj['valid_until'])>instant(obj['verified_at']),'CLAIM_INTERVAL')
    if name=='Observation':
        v=obj['value_interval']
        if v:
            require(math.isfinite(v['lower']) and math.isfinite(v['upper']) and v['lower']<=v['upper'],'OBS_INTERVAL')
            if obj['metric_value'] is not None:require(v['lower']<=obj['metric_value']<=v['upper'],'OBS_VALUE_OUTSIDE_INTERVAL')
        if obj['display_precision']=='rounded':require(v is not None,'ROUNDED_NEEDS_INTERVAL')
    if name=='MetricRow':
        require(instant(obj['period_end'])>instant(obj['period_start']),'METRIC_INTERVAL')
        if obj['status'] in ['OBSERVED','USER_ENTERED']:require(obj['value'] is not None,'OBSERVED_NEEDS_VALUE')
        if obj['value'] is not None:require(math.isfinite(obj['value']),'METRIC_NONFINITE')
    if name=='ContentBrief':
        unique([s['section_id'] for s in obj['sections']],'SECTION_DUPLICATE')
        require(not(obj['visual_required'] and obj['text_only_allowed']),'VISUAL_TEXT_CONTRADICTION')
        if obj['visual_required']:require(bool(obj['required_asset_ids']),'REQUIRED_ASSET_LIST_EMPTY')
        for s in obj['sections']:require(set(s['claim_ids'])<=set(obj['claim_ids']),'SECTION_ORPHAN_CLAIM')
    if name=='PublicCitation':web_url(obj['url'])
    if name=='CardPlan':
        ids=[x['option_id'] for x in obj['options']];unique(ids,'CARD_ID_DUPLICATE');require(obj['recommended_option_id'] in ids,'CARD_RECOMMENDATION_MISSING')
    if name=='GateReport':require(instant(obj['valid_until'])>instant(obj['checked_at']),'GATE_INTERVAL')
    if name=='ArticleIR':
        unique([b['block_id'] for b in obj['blocks']],'BLOCK_DUPLICATE')
        unique([c['id'] for c in obj['public_citations']],'CITATION_DUPLICATE')
        cites={c['id'] for c in obj['public_citations']}
        for c in obj['public_citations']:validate('PublicCitation',c)
        for b in obj['blocks']:
            require(set(b['citation_ids'])<=cites,'CITATION_ORPHAN')
            if b['type']=='table':require(all(len(row)==len(b['headers']) for row in b['rows']),'TABLE_WIDTH')
        # An escaped HTML fragment is text, not permission to render it as markup.
        public=json.dumps({'title':obj['title'],'blocks':obj['blocks']},ensure_ascii=False)
        require(not re.search(r'\[TODO\]|\{\{[^}]+\}\}|BEGIN PRIVATE|여기에.{0,20}삽입||sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}',public),'PUBLIC_INTERNAL_TEXT')
    if name=='ExportManifest':
        require(instant(obj['valid_until'])>instant(obj['generated_at']),'EXPORT_INTERVAL')
        unique([safe_path(f['path']) for f in obj['files']],'FILE_PATH_DUPLICATE')

def bundle_hash(bundle:dict)->str:
    """Bind source scope/permissions, claims, assets and profile; not only article text."""
    return content_hash({'algorithm':'HFBO-NFC-INT-1','article_hash':content_hash(bundle['article']),
      'profile':bundle['profile'],'brief':bundle['brief'],
      'opportunity':{k:bundle['opportunity'][k] for k in ['id','tenant_id','blog_id','reader_question','proposed_answer','review_at']},
      'claims':sorted(bundle['claims'],key=lambda x:x['id']),
      'evidence':sorted(bundle['evidence'],key=lambda x:x['id']),
      'snapshots':sorted(bundle['snapshots'],key=lambda x:x['id']),
      'sources':sorted(bundle['sources'],key=lambda x:x['id']),
      'assets':sorted(bundle['assets'],key=lambda x:x['id']),
      'experience_records':sorted(bundle.get('experience_records',[]),key=lambda x:x['id']),
      'policy_version':bundle['policy_version']})

@dataclass(frozen=True)
class HandoffDecision:
    allowed:bool
    mode:str
    valid_until:str|None
    code:str

def assess_handoff(bundle:dict,now:datetime,*,mode:str)->HandoffDecision:
    """Deterministic reference gate; trusted review-store loading is a caller duty."""
    try:
        require(mode in ['REPLAY','LIVE'],'MODE_INVALID');require(now.tzinfo is not None,'TIMEZONE_REQUIRED')
        a=bundle['article'];b=bundle['brief'];p=bundle['profile'];g=bundle['gate'];op=bundle['opportunity']
        for n,x in [('ArticleIR',a),('ContentBrief',b),('BlogProfile',p),('GateReport',g),('Opportunity',op)]:validate(n,x)
        tenant=a['tenant_id'];blog=a['blog_id']
        require(p['tenant_id']==tenant and p['id']==blog,'PROFILE_SCOPE')
        require(p['version']==a['profile_version'],'PROFILE_VERSION')
        require(a['article_type'] in p['allowed_formats'],'FORMAT_NOT_ALLOWED')
        require(a['brief_id']==b['id'] and (b['tenant_id'],b['blog_id'])==(tenant,blog),'BRIEF_SCOPE')
        require(op['id']==b['opportunity_id'] and (op['tenant_id'],op['blog_id'])==(tenant,blog),'OPPORTUNITY_SCOPE')
        require(a['article_type']==b['article_type'],'ARTICLE_FORMAT_MISMATCH')
        require((g['tenant_id'],g['blog_id'],g['revision_id'])==(tenant,blog,a['revision_id']),'GATE_SCOPE')
        require(g['target_content_hash']==content_hash(a),'CONTENT_CHANGED')
        require(g['policy_version']==bundle['policy_version'],'POLICY_CHANGED')
        require(g['verdict']=='PASS','GATE_NOT_PASS')
        require(g['evidence_bundle_hash']==bundle_hash(bundle),'REVIEW_CONTEXT_CHANGED')
        require(instant(g['checked_at'])<=now,'REVIEW_IN_FUTURE')
        require(mode!='LIVE' or (not a['is_reference_example'] and not p['is_demo'] and bundle['provenance']=='LIVE'),'REPLAY_CANNOT_BECOME_LIVE')
        require(p['status']=='ACTIVE','BLOG_NOT_ACTIVE')
        deadlines=[instant(b['review_at']),instant(op['review_at']),instant(g['valid_until'])]
        indexes={}
        for group,typename in [('claims','Claim'),('evidence','EvidenceItem'),('snapshots','SourceSnapshot'),('sources','SourceRegistration'),('assets','Asset')]:
            unique([x['id'] for x in bundle[group]],group.upper()+'_DUPLICATE')
            indexes[group]={x['id']:x for x in bundle[group]}
            for x in bundle[group]:validate(typename,x);require(x['tenant_id']==tenant,'RESOURCE_TENANT')
        claims=indexes['claims'];evidence=indexes['evidence'];snapshots=indexes['snapshots'];sources=indexes['sources'];assets=indexes['assets']
        usedclaims=set(b['claim_ids'])|{x for block in a['blocks'] for x in block['claim_ids']}
        require(usedclaims<=set(claims),'CLAIM_ORPHAN')
        usedev=set(b['new_contribution']['evidence_ids'])
        for cid in usedclaims:
            c=claims[cid];require(c['blog_id']==blog,'CLAIM_BLOG')
            require(c['support_status'] not in ['UNVERIFIED','CONFLICTING'],'CLAIM_UNSUPPORTED')
            usedev.update(c['evidence_ids'])
            if c['valid_until']:deadlines.append(instant(c['valid_until']))
            if c['verified_at']:require(instant(c['verified_at'])<=now,'CLAIM_FUTURE')
            if c['kind']=='author_experience':
                records={x['id']:x for x in bundle.get('experience_records',[])}
                require(c['author_record_id'] in records and c['author_record_id'] in p['actual_author_record_ids'],'EXPERIENCE_MISSING')
                er=records[c['author_record_id']];require((er['tenant_id'],er['blog_id'])==(tenant,blog),'EXPERIENCE_SCOPE')
                require(er.get('revoked_at') is None,'EXPERIENCE_REVOKED')
        require(usedev<=set(evidence),'EVIDENCE_ORPHAN')
        for eid in usedev:
            e=evidence[eid];require(blog in e['allowed_blog_ids'],'EVIDENCE_SCOPE')
            require(instant(e['verified_at'])<=now,'EVIDENCE_FUTURE');deadlines.append(instant(e['valid_until']))
            require(e['snapshot_id'] in snapshots,'SNAPSHOT_MISSING');s=snapshots[e['snapshot_id']]
            require(blog in s['allowed_blog_ids'],'SNAPSHOT_SCOPE');require(s['source_id'] in sources,'SOURCE_MISSING')
            require(instant(s['observed_at'])<=now,'SNAPSHOT_FUTURE')
            require(s['read_scope'] not in ['metadata','incomplete'],'EVIDENCE_READ_SCOPE_INSUFFICIENT')
            require(mode!='LIVE' or s['execution_mode']!='REPLAY','REPLAY_SNAPSHOT_IN_LIVE')
            source=sources[s['source_id']];require(blog in source['allowed_blog_ids'],'SOURCE_SCOPE')
            require(source['status']=='AVAILABLE','SOURCE_UNAVAILABLE')
            require(source['permissions']['send_to_model'],'MODEL_TRANSFER_NOT_ALLOWED')
            if source['permissions']['expires_at']:deadlines.append(instant(source['permissions']['expires_at']))
        usedassets=set(b['required_asset_ids'])|{x['asset_id'] for x in a['blocks'] if x['type']=='image'}
        require(usedassets<=set(assets),'ASSET_MISSING')
        if b['visual_required']:require(bool(usedassets) and any(x['type']=='image' for x in a['blocks']),'VISUAL_MISSING')
        for aid in usedassets:
            asset=assets[aid];require(asset['blog_id']==blog,'ASSET_SCOPE');require(asset['status']=='READY','ASSET_NOT_READY')
            require(p['platform'] in asset['allowed_platforms'],'ASSET_PLATFORM')
            if asset['expires_at']:deadlines.append(instant(asset['expires_at']))
        limit=min(deadlines);require(now<limit,'STALE_AT_HANDOFF')
        return HandoffDecision(True,mode,limit.isoformat(),'REFERENCE_GATE_PASS' if mode=='REPLAY' else 'DETERMINISTIC_GATE_PASS')
    except (Violation,KeyError,TypeError,ValueError) as e:
        return HandoffDecision(False,mode,None,e.code if isinstance(e,Violation) else 'INVALID_BUNDLE')

def velocity_interval(earlier:dict,later:dict)->dict:
    keys=['source_id','surface','external_id','filter_hash','observer_session','metric_name','unit']
    if any(earlier.get(k)!=later.get(k) for k in keys):return {'status':'INCOMPARABLE','lower':None,'upper':None}
    if any(x['metric_status']!='OBSERVED' for x in (earlier,later)):return {'status':'MISSING','lower':None,'upper':None}
    hours=(instant(later['observed_at'])-instant(earlier['observed_at'])).total_seconds()/3600
    if hours<=0:return {'status':'INCOMPARABLE','lower':None,'upper':None}
    def bounds(x):
        if x.get('value_interval'):return x['value_interval']['lower'],x['value_interval']['upper']
        if x['display_precision']=='exact' and x['metric_value'] is not None:return x['metric_value'],x['metric_value']
        raise Violation('UNKNOWN_PRECISION')
    try:lo1,hi1=bounds(earlier);lo2,hi2=bounds(later)
    except Violation:return {'status':'MISSING','lower':None,'upper':None}
    if lo1>hi1 or lo2>hi2:return {'status':'INVALID','lower':None,'upper':None}
    if hi2<lo1:return {'status':'COUNTER_RESET_OR_REVISION','lower':None,'upper':None}
    return {'status':'INTERVAL','lower':max(0,lo2-hi1)/hours,'upper':max(0,hi2-lo1)/hours}

def plan_action(*,signals_verified:bool,scheduled_event_verified:bool,brief_ready:bool,
                ready_count:int,queue_limit:int,budget_approved:bool,needs_paid_call:bool,
                user_can_post_before_expiry:bool,total_repairs:int,max_repairs:int=6)->str:
    """Reference editorial scheduling policy, NOT a viral prediction model."""
    if ready_count>=queue_limit:return 'QUEUE_FULL_REFRESH_ONLY'
    if total_repairs>=max_repairs:return 'HUMAN_REVIEW'
    if needs_paid_call and not budget_approved:return 'BUDGET_REQUIRED'
    if not signals_verified:return 'PREPARE_ONLY' if scheduled_event_verified else 'RESEARCH'
    if not user_can_post_before_expiry:return 'REFRAME_OR_DEFER'
    return 'WRITE' if brief_ready else 'RESEARCH'
