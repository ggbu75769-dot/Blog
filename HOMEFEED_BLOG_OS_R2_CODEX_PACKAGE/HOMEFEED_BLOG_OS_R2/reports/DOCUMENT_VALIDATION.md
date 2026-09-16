# 문서·스키마 검증 실행 보고서

실행 시각: 2026-09-15T20:30:23.275383+00:00
실제 실행 결과: PASS 73 / FAIL 0.

**제품 기능·DB·실제 블로그·조회수 시험의 통과 결과가 아니다.**

별도 제품 인수시험 140개는 설계만 작성했으며 모두 NOT_RUN 상태다.

| ID | 검사 | 결과 |
|---|---|---|
| DOC-001 | Domain Draft 2020-12 syntax | PASS |
| DOC-002 | Domain refs resolve locally | PASS |
| DOC-003 | Example blog_profile.json | PASS |
| DOC-004 | Example blog_profile_living.json | PASS |
| DOC-005 | Example source_registration.json | PASS |
| DOC-006 | Example source_snapshot.json | PASS |
| DOC-007 | Example observation.json | PASS |
| DOC-008 | Example opportunity.json | PASS |
| DOC-009 | Example evidence_item.json | PASS |
| DOC-010 | Example content_brief.json | PASS |
| DOC-011 | Example article_ir.json | PASS |
| DOC-012 | Example review_findings.json | PASS |
| DOC-013 | Example publication_receipt.json | PASS |
| DOC-014 | Example metric_row.json | PASS |
| DOC-015 | Example export/manifest.json | PASS |
| DOC-016 | Array example claims.json | PASS |
| DOC-017 | Schema wrapper AgentEnvelope.schema.json | PASS |
| DOC-018 | Schema wrapper ArticleIR.schema.json | PASS |
| DOC-019 | Schema wrapper AssetPlan.schema.json | PASS |
| DOC-020 | Schema wrapper BlogProfile.schema.json | PASS |
| DOC-021 | Schema wrapper CardPlan.schema.json | PASS |
| DOC-022 | Schema wrapper ContentBrief.schema.json | PASS |
| DOC-023 | Schema wrapper ExportManifest.schema.json | PASS |
| DOC-024 | Schema wrapper GateReport.schema.json | PASS |
| DOC-025 | Schema wrapper MetricRow.schema.json | PASS |
| DOC-026 | Schema wrapper Observation.schema.json | PASS |
| DOC-027 | Schema wrapper PublicationReceipt.schema.json | PASS |
| DOC-028 | Schema wrapper ResearchPack.schema.json | PASS |
| DOC-029 | Schema wrapper ReviewFindings.schema.json | PASS |
| DOC-030 | Schema wrapper RoutingDecision.schema.json | PASS |
| DOC-031 | Schema wrapper SourceRegistration.schema.json | PASS |
| DOC-032 | Unique task IDs | PASS |
| DOC-033 | Unique requirement IDs | PASS |
| DOC-034 | Unique acceptance IDs | PASS |
| DOC-035 | Task, requirement, acceptance traceability | PASS |
| DOC-036 | Topological task order | PASS |
| DOC-037 | Acceptance specs explicitly NOT_RUN | PASS |
| DOC-038 | Bidirectional task/requirement/AT links | PASS |
| DOC-039 | 24 editorial scenarios explicitly unexecuted | PASS |
| DOC-040 | Reference implementation exists but not the product app | PASS |
| DOC-041 | All state transitions are defined | PASS |
| DOC-042 | HANDOFF_READY not a publication state | PASS |
| DOC-043 | Manual-only and replay defaults | PASS |
| DOC-044 | Single primary-blog calendar-month target | PASS |
| DOC-045 | Paid access disabled without approved budget | PASS |
| DOC-046 | Ranking weights sum to one, not a probability | PASS |
| DOC-047 | Bounded lease heartbeat | PASS |
| DOC-048 | OpenAPI version and unique operation IDs | PASS |
| DOC-049 | OpenAPI schema references resolve | PASS |
| DOC-050 | API path params and write idempotency headers | PASS |
| DOC-051 | No platform publisher routes | PASS |
| DOC-052 | Writer contract cannot carry a server gate | PASS |
| DOC-053 | Example scope isolation and brief link | PASS |
| DOC-054 | All article claim/citation refs exist | PASS |
| DOC-055 | Unique article blocks | PASS |
| DOC-056 | Table rows match headers | PASS |
| DOC-057 | Reference text-only example not fake image-ready | PASS |
| DOC-058 | Public reference has no working placeholders or tool tokens | PASS |
| DOC-059 | Immutable IR hash matches manifest and review | PASS |
| DOC-060 | Export reference file sizes, hashes, scope | PASS |
| DOC-061 | Source register IDs unique | PASS |
| DOC-062 | Source provenance and limitation fields | PASS |
| DOC-063 | SQL table names unique (text structure only) | PASS |
| DOC-064 | Reference DDL clearly unapplied | PASS |
| DOC-065 | Each reference table enables and forces RLS (text only) | PASS |
| DOC-066 | Durable job/budget/fencing fields exist (text only) | PASS |
| DOC-067 | Negative schema: writer cannot add gate_report | PASS |
| DOC-068 | Negative schema: invalid blog UUID | PASS |
| DOC-069 | Negative schema: export cannot claim public posting | PASS |
| DOC-070 | Negative schema: opportunity not a calibrated probability | PASS |
| DOC-071 | Required implementation handoff files exist | PASS |
| DOC-072 | Documentation sequence 00 through 38 exists | PASS |
| DOC-073 | No private credentials or artifact tool citation tokens in authored docs | PASS |

## 미실행 영역
- application implementation
- PostgreSQL parse/migration/RLS/concurrency
- LIVE source/model pipeline
- image-generation/asset-render pipeline
- Naver/Tistory editor UAT
- human naturalness blind study
- homefeed exposure/growth validation
