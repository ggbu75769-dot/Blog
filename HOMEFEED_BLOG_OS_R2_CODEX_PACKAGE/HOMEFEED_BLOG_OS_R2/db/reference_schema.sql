-- HOMEFEED BLOG OS 4.1.0-r1 / reference DDL, 2026-09-15
-- NOT APPLIED OR TESTED AGAINST POSTGRESQL IN THIS DOCUMENT PACKAGE.
-- Disposable DB migration/rollback/RLS/concurrency tests are required before adoption.
-- Existing DB: translate into versioned migrations, do not paste blindly.
-- IDs are assigned by the server. Application role must NOT own tables or BYPASSRLS.
-- Set app.tenant_id, app.blog_ids ('{uuid,...}'), app.allow_shared, app.actor_subject locally per tx after authentication.
-- These are server-derived context, NOT client-editable or a defense against arbitrary SQL execution.
-- Backend roles must not expose SQL, own tables, alter RLS or inherit BYPASSRLS.
-- Context is set in a short tx and cleared by transaction exit; test pooled-connection reuse.
-- R1 edits were structurally checked only: PostgreSQL execution was unavailable in the audit runtime.
BEGIN;
CREATE TABLE tenants (id uuid PRIMARY KEY, name text NOT NULL, created_at timestamptz NOT NULL DEFAULT now());

CREATE TABLE members (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  user_subject text NOT NULL, role text NOT NULL CHECK(role IN ('OWNER','EDITOR','READER','WORKER')), UNIQUE(tenant_id,user_subject),
  UNIQUE (tenant_id, id)
);

CREATE TABLE blogs (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  name text NOT NULL, platform text NOT NULL CHECK(platform IN ('naver','tistory','owned')), url text, status text NOT NULL DEFAULT 'DRAFT', is_primary boolean NOT NULL DEFAULT false, version integer NOT NULL DEFAULT 1 CHECK(version>0), public_posting_mode text NOT NULL DEFAULT 'manual' CHECK(public_posting_mode='manual'),
  UNIQUE (tenant_id, id)
);

CREATE UNIQUE INDEX one_primary_blog ON blogs(tenant_id) WHERE is_primary;
CREATE TABLE blog_grants (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  member_id uuid NOT NULL, can_read boolean NOT NULL DEFAULT false, can_edit boolean NOT NULL DEFAULT false, UNIQUE(tenant_id,blog_id,member_id),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, member_id) REFERENCES members(tenant_id, id)
);

CREATE TABLE profile_versions (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  version integer NOT NULL CHECK(version>0), profile jsonb NOT NULL, content_hash text NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'), UNIQUE(tenant_id,blog_id,version),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id)
);

CREATE TABLE author_records (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  kind text NOT NULL CHECK(kind IN ('fact','experience')), subject text NOT NULL, allowed_statements jsonb NOT NULL, scope_notes text NOT NULL, approved_at timestamptz NOT NULL, revoked_at timestamptz, record jsonb NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id)
);

CREATE TABLE sources (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  allowed_blog_ids uuid[] NOT NULL CHECK(cardinality(allowed_blog_ids)>0),
  allowed_hosts text[] NOT NULL DEFAULT '{}',
  kind text NOT NULL, name text NOT NULL, base_url text, permission_version text NOT NULL, permissions jsonb NOT NULL, credential_ref text, status text NOT NULL, checked_at timestamptz,
  UNIQUE (tenant_id, id)
);

CREATE TABLE source_snapshots (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  allowed_blog_ids uuid[] NOT NULL CHECK(cardinality(allowed_blog_ids)>0),
  source_id uuid NOT NULL, canonical_url text NOT NULL, content_hash text NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'), published_at timestamptz, date_precision text NOT NULL, execution_mode text NOT NULL CHECK(execution_mode IN ('LIVE','REPLAY','USER_IMPORT')), observed_at timestamptz NOT NULL, read_scope text NOT NULL, independence_group text NOT NULL, permission_version text NOT NULL, snapshot jsonb NOT NULL, UNIQUE(tenant_id,source_id,canonical_url,content_hash),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, source_id) REFERENCES sources(tenant_id, id)
);

CREATE TABLE observations (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  source_id uuid NOT NULL, external_id text NOT NULL, surface text NOT NULL, observer_session text NOT NULL DEFAULT '', observed_at timestamptz NOT NULL, filter_hash text NOT NULL, metric_value numeric, metric_status text NOT NULL, source_updated_at timestamptz, observation jsonb NOT NULL, UNIQUE(tenant_id,source_id,external_id,surface,observer_session,observed_at,filter_hash),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, source_id) REFERENCES sources(tenant_id, id)
);

CREATE TABLE events (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  canonical_key text NOT NULL, occurred_at timestamptz, first_observed_at timestamptz NOT NULL, independence_groups jsonb NOT NULL DEFAULT '[]', event jsonb NOT NULL, UNIQUE(tenant_id,canonical_key),
  UNIQUE (tenant_id, id)
);

CREATE TABLE opportunities (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  event_id uuid NOT NULL, reader_question text NOT NULL, proposed_answer text NOT NULL, rank numeric NOT NULL DEFAULT 0 CHECK(rank>=0 AND rank<=100), coverage numeric NOT NULL CHECK(coverage>=0 AND coverage<=1), status text NOT NULL, review_at timestamptz NOT NULL, opportunity jsonb NOT NULL,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, event_id) REFERENCES events(tenant_id, id)
);

CREATE TABLE evidence_items (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  snapshot_id uuid NOT NULL, allowed_blog_ids uuid[] NOT NULL, locator text NOT NULL, summary text NOT NULL, verified_at timestamptz NOT NULL, valid_until timestamptz NOT NULL, independence_group text NOT NULL, CHECK(valid_until>verified_at),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, snapshot_id) REFERENCES source_snapshots(tenant_id, id)
);

CREATE TABLE claims (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  statement text NOT NULL, kind text NOT NULL, support_status text NOT NULL, author_record_id uuid, scope_notes text NOT NULL, verified_at timestamptz, valid_until timestamptz, supersedes_claim_id uuid,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, author_record_id) REFERENCES author_records(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, supersedes_claim_id) REFERENCES claims(tenant_id, blog_id, id)
);

CREATE TABLE claim_evidence (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  claim_id uuid NOT NULL, evidence_id uuid NOT NULL, UNIQUE(tenant_id,blog_id,claim_id,evidence_id),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, claim_id) REFERENCES claims(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, evidence_id) REFERENCES evidence_items(tenant_id, id)
);

CREATE TABLE briefs (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  opportunity_id uuid NOT NULL, version integer NOT NULL CHECK(version>0), brief jsonb NOT NULL, content_hash text NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'), review_at timestamptz NOT NULL, UNIQUE(tenant_id,blog_id,opportunity_id,version),
  UNIQUE (tenant_id, blog_id, opportunity_id, id),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, opportunity_id) REFERENCES opportunities(tenant_id, blog_id, id)
);

CREATE TABLE topic_reservations (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  event_id uuid NOT NULL, question_fingerprint text NOT NULL, answer_fingerprint text NOT NULL, expires_at timestamptz NOT NULL, released_at timestamptz,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, event_id) REFERENCES events(tenant_id, id)
);

CREATE UNIQUE INDEX active_topic_reservation ON topic_reservations(tenant_id,event_id,question_fingerprint,answer_fingerprint) WHERE released_at IS NULL;
CREATE TABLE articles (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  opportunity_id uuid NOT NULL, brief_id uuid, state text NOT NULL CHECK(state IN ('DISCOVERED','ASSIGNED','RESEARCHING','BRIEF_READY','DRAFTED','EDITING','VERIFYING','ASSET_READY','RENDERING','HANDOFF_READY','NEEDS_SOURCE','NEEDS_ASSET','NEEDS_EXPERIENCE','NEEDS_REVIEW','REVALIDATION_REQUIRED','DEFERRED','REJECTED')), current_revision_id uuid, version integer NOT NULL DEFAULT 1 CHECK(version>0), updated_at timestamptz NOT NULL DEFAULT now(),
  CHECK(state NOT IN ('BRIEF_READY','DRAFTED','EDITING','VERIFYING','ASSET_READY','RENDERING','HANDOFF_READY') OR brief_id IS NOT NULL),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, opportunity_id) REFERENCES opportunities(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, opportunity_id, brief_id) REFERENCES briefs(tenant_id, blog_id, opportunity_id, id)
);

CREATE TABLE article_revisions (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  article_id uuid NOT NULL, brief_id uuid NOT NULL, profile_version_id uuid NOT NULL, parent_revision_id uuid, version integer NOT NULL CHECK(version>0), content_hash text NOT NULL CHECK (content_hash ~ '^[0-9a-f]{64}$'), article_ir jsonb NOT NULL, edit_reason text NOT NULL, UNIQUE(tenant_id,blog_id,article_id,version), UNIQUE(tenant_id,blog_id,article_id,id),
  CHECK(parent_revision_id IS NULL OR parent_revision_id <> id),
  UNIQUE (tenant_id, blog_id, id, content_hash),
  UNIQUE (tenant_id, blog_id, article_id, id, content_hash),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, article_id) REFERENCES articles(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, brief_id) REFERENCES briefs(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, profile_version_id) REFERENCES profile_versions(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, article_id, parent_revision_id) REFERENCES article_revisions(tenant_id, blog_id, article_id, id)
);

ALTER TABLE articles ADD CONSTRAINT article_current_revision_fk FOREIGN KEY(tenant_id,blog_id,id,current_revision_id) REFERENCES article_revisions(tenant_id,blog_id,article_id,id) DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE article_claims (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  revision_id uuid NOT NULL, claim_id uuid NOT NULL, block_id text NOT NULL, UNIQUE(tenant_id,blog_id,revision_id,block_id,claim_id),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, revision_id) REFERENCES article_revisions(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, claim_id) REFERENCES claims(tenant_id, blog_id, id)
);

CREATE TABLE assets (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  object_key text NOT NULL, sha256 text NOT NULL, mime text NOT NULL, size_bytes bigint NOT NULL CHECK(size_bytes>0), width integer NOT NULL CHECK(width>0), height integer NOT NULL CHECK(height>0), status text NOT NULL CHECK(status IN('QUARANTINED','READY','REJECTED')), rights_version integer NOT NULL CHECK(rights_version>0), rights jsonb NOT NULL, expires_at timestamptz, UNIQUE(tenant_id,object_key),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id)
);

CREATE TABLE article_assets (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  revision_id uuid NOT NULL, asset_id uuid NOT NULL, block_id text NOT NULL, UNIQUE(tenant_id,blog_id,revision_id,block_id),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, revision_id) REFERENCES article_revisions(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, asset_id) REFERENCES assets(tenant_id, blog_id, id)
);

CREATE TABLE review_reports (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  revision_id uuid NOT NULL, target_content_hash text NOT NULL, evidence_bundle_hash text NOT NULL, policy_version text NOT NULL, issuer text NOT NULL CHECK(issuer='review_service'), verdict text NOT NULL CHECK(verdict IN('PASS','FAIL','HOLD')), checked_at timestamptz NOT NULL, valid_until timestamptz NOT NULL, report jsonb NOT NULL, CHECK(valid_until>checked_at),
  UNIQUE (tenant_id, blog_id, revision_id, id, target_content_hash, evidence_bundle_hash),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, revision_id, target_content_hash) REFERENCES article_revisions(tenant_id, blog_id, id, content_hash)
);

CREATE TABLE exports (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  article_id uuid NOT NULL, revision_id uuid NOT NULL, review_report_id uuid NOT NULL, target_platform text NOT NULL CHECK(target_platform IN('naver_manual','tistory_manual','owned_manual')), status text NOT NULL CHECK(status IN('HANDOFF_READY','REVALIDATION_REQUIRED','REFERENCE_EXAMPLE')), content_hash text NOT NULL, review_bundle_hash text NOT NULL, valid_until timestamptz NOT NULL, manifest jsonb NOT NULL, public_posting_performed boolean NOT NULL DEFAULT false CHECK(public_posting_performed=false),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, article_id) REFERENCES articles(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id, article_id, revision_id, content_hash) REFERENCES article_revisions(tenant_id, blog_id, article_id, id, content_hash),
  FOREIGN KEY (tenant_id, blog_id, revision_id, review_report_id, content_hash, review_bundle_hash) REFERENCES review_reports(tenant_id, blog_id, revision_id, id, target_content_hash, evidence_bundle_hash)
);

CREATE TABLE export_files (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  export_id uuid NOT NULL, relative_path text NOT NULL CHECK(relative_path !~ '(^/|(^|/)\.\.(/|$))'), object_key text NOT NULL, sha256 text NOT NULL, size_bytes bigint NOT NULL CHECK(size_bytes>=0), visibility text NOT NULL CHECK(visibility IN('public','private','guide')), UNIQUE(tenant_id,blog_id,export_id,relative_path),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, export_id) REFERENCES exports(tenant_id, blog_id, id)
);

CREATE TABLE publication_receipts (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  article_revision_id uuid NOT NULL, url text NOT NULL, posted_at timestamptz NOT NULL, recorded_by uuid NOT NULL, status text NOT NULL CHECK(status IN('USER_RECORDED','USER_CORRECTED','RETRACTED')), final_content_hash text, user_note text NOT NULL DEFAULT '',
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, article_revision_id) REFERENCES article_revisions(tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, recorded_by) REFERENCES members(tenant_id, id)
);

CREATE TABLE jobs (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  kind text NOT NULL, status text NOT NULL CHECK(status IN('QUEUED','RUNNING','WAITING','COMPLETED','FAILED','CANCELLED')), stage text NOT NULL, idempotency_key text NOT NULL, input_hash text NOT NULL, payload jsonb NOT NULL, priority integer NOT NULL DEFAULT 0, not_before timestamptz NOT NULL DEFAULT now(), lease_until timestamptz, lease_owner text, fencing_token bigint NOT NULL DEFAULT 0 CHECK(fencing_token>=0), attempt integer NOT NULL DEFAULT 0 CHECK(attempt>=0), output_ref text, error_code text, updated_at timestamptz NOT NULL DEFAULT now(), UNIQUE(tenant_id,idempotency_key),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id)
);

CREATE TABLE job_events (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  job_id uuid NOT NULL, sequence bigint NOT NULL, stage text NOT NULL, event text NOT NULL, data jsonb NOT NULL, UNIQUE(tenant_id,job_id,sequence),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, job_id) REFERENCES jobs(tenant_id, id)
);

CREATE TABLE budget_accounts (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  currency text NOT NULL, period_start timestamptz NOT NULL, period_end timestamptz NOT NULL, limit_micro bigint CHECK(limit_micro>=0), spent_micro bigint NOT NULL DEFAULT 0 CHECK(spent_micro>=0), reserved_micro bigint NOT NULL DEFAULT 0 CHECK(reserved_micro>=0), UNIQUE(tenant_id,currency,period_start), CHECK(period_end>period_start), overrun_micro bigint GENERATED ALWAYS AS (CASE WHEN limit_micro IS NOT NULL THEN GREATEST(0::bigint,spent_micro+reserved_micro-limit_micro) ELSE 0::bigint END) STORED,
  UNIQUE (tenant_id, id)
);

CREATE TABLE call_intents (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  job_id uuid NOT NULL, provider text NOT NULL, stage_key text NOT NULL, input_hash text NOT NULL, provider_job_id text, status text NOT NULL CHECK(status IN('RESERVED','SUBMITTED','UNKNOWN','COMPLETED','FAILED','CANCELLED')), quoted_micro bigint NOT NULL CHECK(quoted_micro>=0), actual_micro bigint CHECK(actual_micro>=0), currency text NOT NULL, pricing_version text NOT NULL, reconciliation jsonb NOT NULL DEFAULT '{}', UNIQUE(tenant_id,provider,stage_key,input_hash),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, job_id) REFERENCES jobs(tenant_id, id)
);

CREATE TABLE budget_reservations (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  account_id uuid NOT NULL, call_intent_id uuid NOT NULL, amount_micro bigint NOT NULL CHECK(amount_micro>=0), status text NOT NULL CHECK(status IN('RESERVED','SETTLED','RELEASED')), UNIQUE(tenant_id,call_intent_id),
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, account_id) REFERENCES budget_accounts(tenant_id, id),
  FOREIGN KEY (tenant_id, call_intent_id) REFERENCES call_intents(tenant_id, id)
);

CREATE TABLE audit_events (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  actor_id uuid, event_type text NOT NULL, object_ref text NOT NULL, before_hash text, after_hash text, request_id uuid NOT NULL, details jsonb NOT NULL,
  UNIQUE (tenant_id, id),
  FOREIGN KEY (tenant_id, actor_id) REFERENCES members(tenant_id, id)
);

CREATE TABLE metric_imports (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  uploaded_file_ref text NOT NULL, input_hash text NOT NULL, mapping_version text NOT NULL, source_revision text NOT NULL, status text NOT NULL CHECK(status IN('PREVIEW','COMMITTED','REJECTED')), period_start timestamptz NOT NULL, period_end timestamptz NOT NULL, timezone text NOT NULL, UNIQUE(tenant_id,blog_id,input_hash,mapping_version), CHECK(period_end>period_start),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id)
);

CREATE TABLE metric_rows (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  import_id uuid NOT NULL, platform text NOT NULL, entity_key text NOT NULL, metric text NOT NULL, value numeric, status text NOT NULL, unit text NOT NULL, denominator_metric text, period_start timestamptz NOT NULL, period_end timestamptz NOT NULL, dimension_hash text NOT NULL, source_revision text NOT NULL, source_updated_at timestamptz, is_current boolean NOT NULL DEFAULT true, row_data jsonb NOT NULL, CHECK(period_end>period_start), UNIQUE(tenant_id,blog_id,platform,entity_key,metric,period_start,period_end,dimension_hash,source_revision),
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id),
  FOREIGN KEY (tenant_id, blog_id, import_id) REFERENCES metric_imports(tenant_id, blog_id, id)
);

CREATE TABLE experiments (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  blog_id uuid NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now(),
  hypothesis text NOT NULL, preregistration jsonb NOT NULL, status text NOT NULL CHECK(status IN('PLANNED','RUNNING','SUPPORTED','REFUTED','INCONCLUSIVE','INVALID')), started_at timestamptz, ended_at timestamptz, results jsonb,
  UNIQUE (tenant_id, id),
  UNIQUE (tenant_id, blog_id, id),
  FOREIGN KEY (tenant_id, blog_id) REFERENCES blogs(tenant_id,id)
);


-- Scope enforcement. Application must set authenticated values with SET LOCAL inside every tx.
-- Shared means tenant-scoped sources/ops, not public to every blog. Evidence usage requires allowed_blog_ids check.
ALTER TABLE tenants ENABLE ROW LEVEL SECURITY;
ALTER TABLE tenants FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_scope ON tenants USING (id = NULLIF(current_setting('app.tenant_id',true),'')::uuid) WITH CHECK (id = NULLIF(current_setting('app.tenant_id',true),'')::uuid);

ALTER TABLE members ENABLE ROW LEVEL SECURITY;
ALTER TABLE members FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON members USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE blogs ENABLE ROW LEVEL SECURITY;
ALTER TABLE blogs FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON blogs USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]) OR current_setting('app.allow_shared',true)='on')) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]) OR current_setting('app.allow_shared',true)='on'));
ALTER TABLE blog_grants ENABLE ROW LEVEL SECURITY;
ALTER TABLE blog_grants FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON blog_grants USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE profile_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE profile_versions FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON profile_versions USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE author_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE author_records FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON author_records USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE sources FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON sources USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on' AND allowed_blog_ids && (COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on' AND cardinality(allowed_blog_ids)>0 AND allowed_blog_ids <@ (COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]));
ALTER TABLE source_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE source_snapshots FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON source_snapshots USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on' AND allowed_blog_ids && (COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on' AND cardinality(allowed_blog_ids)>0 AND allowed_blog_ids <@ (COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]));
ALTER TABLE observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE observations FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON observations USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE events FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON events USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE opportunities FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON opportunities USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND ((blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]) OR (blog_id IS NULL AND current_setting('app.allow_shared',true)='on')))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND ((blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]) OR (blog_id IS NULL AND current_setting('app.allow_shared',true)='on'))));
ALTER TABLE evidence_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence_items FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON evidence_items USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on' AND allowed_blog_ids && (COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on' AND cardinality(allowed_blog_ids)>0 AND allowed_blog_ids <@ (COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]));
ALTER TABLE claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE claims FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON claims USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE claim_evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE claim_evidence FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON claim_evidence USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE briefs ENABLE ROW LEVEL SECURITY;
ALTER TABLE briefs FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON briefs USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE topic_reservations ENABLE ROW LEVEL SECURITY;
ALTER TABLE topic_reservations FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON topic_reservations USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE articles FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON articles USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE article_revisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE article_revisions FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON article_revisions USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE article_claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE article_claims FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON article_claims USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON assets USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE article_assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE article_assets FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON article_assets USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE review_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE review_reports FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON review_reports USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE exports ENABLE ROW LEVEL SECURITY;
ALTER TABLE exports FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON exports USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE export_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE export_files FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON export_files USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE publication_receipts ENABLE ROW LEVEL SECURITY;
ALTER TABLE publication_receipts FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON publication_receipts USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON jobs USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND ((blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]) OR (blog_id IS NULL AND current_setting('app.allow_shared',true)='on')))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND ((blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]) OR (blog_id IS NULL AND current_setting('app.allow_shared',true)='on'))));
ALTER TABLE job_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_events FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON job_events USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE budget_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_accounts FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON budget_accounts USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE call_intents ENABLE ROW LEVEL SECURITY;
ALTER TABLE call_intents FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON call_intents USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE budget_reservations ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_reservations FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON budget_reservations USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE audit_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_events FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON audit_events USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on') WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND current_setting('app.allow_shared',true)='on');
ALTER TABLE metric_imports ENABLE ROW LEVEL SECURITY;
ALTER TABLE metric_imports FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON metric_imports USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE metric_rows ENABLE ROW LEVEL SECURITY;
ALTER TABLE metric_rows FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON metric_rows USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));
ALTER TABLE experiments ENABLE ROW LEVEL SECURITY;
ALTER TABLE experiments FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_blog_scope ON experiments USING (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[]))) WITH CHECK (tenant_id = NULLIF(current_setting('app.tenant_id',true),'')::uuid AND (blog_id = ANY(COALESCE(NULLIF(current_setting('app.blog_ids',true),''),'{}')::uuid[])));

-- Immutable content snapshots: new edits create rows, not UPDATE. Authorized retention deletes are separate.
CREATE FUNCTION hfbo_reject_revision_update() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'immutable snapshot: create a new revision'; END $$;

CREATE TRIGGER immutable_profile_versions BEFORE UPDATE ON profile_versions FOR EACH ROW EXECUTE FUNCTION hfbo_reject_revision_update();
CREATE TRIGGER immutable_briefs BEFORE UPDATE ON briefs FOR EACH ROW EXECUTE FUNCTION hfbo_reject_revision_update();
CREATE TRIGGER immutable_article_revisions BEFORE UPDATE ON article_revisions FOR EACH ROW EXECUTE FUNCTION hfbo_reject_revision_update();
CREATE TRIGGER immutable_source_snapshots BEFORE UPDATE ON source_snapshots FOR EACH ROW EXECUTE FUNCTION hfbo_reject_revision_update();

CREATE INDEX jobs_ready_idx ON jobs(status,not_before,priority DESC) WHERE status='QUEUED';
CREATE INDEX jobs_lease_idx ON jobs(lease_until) WHERE status='RUNNING';
CREATE INDEX opportunity_rank_idx ON opportunities(tenant_id,blog_id,status,rank DESC);
CREATE INDEX claim_expiry_idx ON claims(tenant_id,valid_until);
CREATE INDEX asset_expiry_idx ON assets(tenant_id,blog_id,expires_at);
CREATE INDEX export_expiry_idx ON exports(tenant_id,blog_id,valid_until);
CREATE INDEX metrics_current_idx ON metric_rows(tenant_id,blog_id,metric,period_start) WHERE is_current;

-- R1: synchronous HTTP request idempotency, separate from jobs.idempotency_key.
CREATE TABLE api_idempotency (
  id uuid PRIMARY KEY,
  tenant_id uuid NOT NULL REFERENCES tenants(id),
  actor_subject text NOT NULL,
  method text NOT NULL CHECK(method IN ('POST','PATCH','PUT','DELETE')),
  canonical_path text NOT NULL,
  idempotency_key text NOT NULL,
  request_hash text NOT NULL CHECK(request_hash ~ '^[0-9a-f]{64}$'),
  status text NOT NULL CHECK(status IN ('IN_PROGRESS','COMPLETED','OUTCOME_UNKNOWN')),
  response_code integer, response_body jsonb, output_ref text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  expires_at timestamptz NOT NULL,
  UNIQUE(tenant_id,actor_subject,method,canonical_path,idempotency_key),
  CHECK(expires_at>created_at)
);
ALTER TABLE api_idempotency ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_idempotency FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_actor_scope ON api_idempotency
USING (tenant_id=NULLIF(current_setting('app.tenant_id',true),'')::uuid AND actor_subject=current_setting('app.actor_subject',true))
WITH CHECK (tenant_id=NULLIF(current_setting('app.tenant_id',true),'')::uuid AND actor_subject=current_setting('app.actor_subject',true));

-- Supersede the old current row and insert the replacement in one transaction.
CREATE UNIQUE INDEX one_current_metric ON metric_rows
(tenant_id,blog_id,platform,entity_key,metric,period_start,period_end,dimension_hash)
WHERE is_current;

-- Scope arrays must refer only to blogs of this tenant, even for a privileged ingest worker.
CREATE FUNCTION hfbo_validate_allowed_blogs() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE b uuid;
BEGIN
 IF cardinality(NEW.allowed_blog_ids)=0 THEN RAISE EXCEPTION 'empty source scope'; END IF;
 FOREACH b IN ARRAY NEW.allowed_blog_ids LOOP
  IF b IS NULL OR NOT EXISTS(SELECT 1 FROM blogs WHERE tenant_id=NEW.tenant_id AND id=b)
  THEN RAISE EXCEPTION 'source scope references another tenant or inaccessible blog'; END IF;
 END LOOP;
 RETURN NEW;
END $$;
CREATE TRIGGER source_scope_ids BEFORE INSERT OR UPDATE ON sources FOR EACH ROW EXECUTE FUNCTION hfbo_validate_allowed_blogs();
CREATE TRIGGER snapshot_scope_ids BEFORE INSERT ON source_snapshots FOR EACH ROW EXECUTE FUNCTION hfbo_validate_allowed_blogs();
CREATE TRIGGER evidence_scope_ids BEFORE INSERT OR UPDATE ON evidence_items FOR EACH ROW EXECUTE FUNCTION hfbo_validate_allowed_blogs();

-- Link scope is checked independently of mere FK existence. Parent source scope is narrowed, never widened.
CREATE FUNCTION hfbo_check_claim_evidence_scope() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
 IF NOT EXISTS (
  SELECT 1 FROM evidence_items e
  JOIN source_snapshots ss ON ss.tenant_id=e.tenant_id AND ss.id=e.snapshot_id
  JOIN sources so ON so.tenant_id=ss.tenant_id AND so.id=ss.source_id
  WHERE e.tenant_id=NEW.tenant_id AND e.id=NEW.evidence_id
    AND NEW.blog_id=ANY(e.allowed_blog_ids)
    AND NEW.blog_id=ANY(ss.allowed_blog_ids)
    AND NEW.blog_id=ANY(so.allowed_blog_ids)
 ) THEN RAISE EXCEPTION 'claim evidence scope denied'; END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER claim_evidence_scope BEFORE INSERT OR UPDATE ON claim_evidence FOR EACH ROW EXECUTE FUNCTION hfbo_check_claim_evidence_scope();

CREATE FUNCTION hfbo_check_parent_revision() RETURNS trigger LANGUAGE plpgsql AS $$
DECLARE parent_version integer;
BEGIN
 IF NEW.parent_revision_id IS NOT NULL THEN
  SELECT version INTO parent_version FROM article_revisions
   WHERE tenant_id=NEW.tenant_id AND blog_id=NEW.blog_id
     AND article_id=NEW.article_id AND id=NEW.parent_revision_id;
  IF parent_version IS NULL OR parent_version>=NEW.version
   THEN RAISE EXCEPTION 'parent must be an older revision of the same article'; END IF;
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER parent_revision_guard BEFORE INSERT ON article_revisions FOR EACH ROW EXECUTE FUNCTION hfbo_check_parent_revision();

COMMIT;

-- Queue claim REFERENCE only. Run inside a short tx using a correctly scoped worker role.
-- WITH pick AS (
--   SELECT id FROM jobs WHERE status='QUEUED' AND not_before<=now()
--   ORDER BY priority DESC,not_before,id FOR UPDATE SKIP LOCKED LIMIT 1
-- ) UPDATE jobs j SET status='RUNNING', lease_owner=:worker_id,
--   lease_until=now()+interval '120 seconds', fencing_token=j.fencing_token+1,
--   attempt=j.attempt+1, updated_at=now()
-- FROM pick WHERE j.id=pick.id RETURNING j.*;
-- No external model/HTTP call while holding this transaction.
-- Completion/heartbeat must WHERE tenant_id=:tenant AND id=:id AND fencing_token=:token AND status='RUNNING'.
-- Queue lease reclaim MUST reconcile prior call_intents; no blind second paid request.
-- Budget reserve: SELECT account FOR UPDATE; require limit not null; check spent+reserved+quote<=limit;
-- INSERT reservation + intent + UPDATE reserved in ONE transaction. Settlements similarly atomically apply delta.
-- Actual over-quote billing must still be recorded in spent_micro. overrun_micro exposes it; new reservations are denied and an exception/audit is required.
