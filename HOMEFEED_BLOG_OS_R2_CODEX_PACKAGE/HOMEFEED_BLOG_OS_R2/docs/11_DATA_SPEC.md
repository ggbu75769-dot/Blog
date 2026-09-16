# 11. 데이터·저장·버전 명세서

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 원칙
모든 사용자 데이터는 tenant_id를 갖는다. 블로그별 데이터는 blog_id도 갖고 DB·앱·파일·캐시·검색 인덱스 전체에 scope를 적용한다. UUID는 서버가 생성하고 외부 원본 ID는 별도 필드다. 시간은 timestamptz, 돈은 정수 minor/micro 단위와 currency, unknown metric은 NULL+status를 사용한다. float로 금액을 누적하지 않는다.

## 테이블 그룹
| 그룹 | 주요 테이블 | 역할 |
|---|---|---|
| 계정·편집 | tenants, members, blogs, blog_grants, profile_versions, author_records | 소유권·문체·개인 사실/경험 |
| 자료·관측 | sources, source_snapshots, observations, events | 실제 접근 범위·시각·관심 신호 |
| 기획 | opportunities, briefs, topic_reservations | 질문·새 답·배정·중복예약 |
| 근거 | evidence_items, claims, claim_evidence | 주장·원문 연결·독립 근거 |
| 원고 | articles, article_revisions, article_claims | 불변 버전과 본문 연결 |
| 자산·검수 | assets, article_assets, review_reports | 파일·권리·검수 해시 |
| 출력·수동 기록 | exports, export_files, publication_receipts | 실제 파일과 사용자 게시 기록 |
| 운영 | jobs, job_events, call_intents, budget_accounts, budget_reservations, audit_events | 재개·비용·변경 |
| 성과 | metric_imports, metric_rows, experiments | 원본 집계·매핑·시험 |

`db/reference_schema.sql`은 신규 PostgreSQL용 참조 DDL이며 실제 배포 migration으로 검증된 것이 아니다. 기존 DB에는 바로 실행하지 않는다. M0에서 migration 계획을 수립하고 disposable DB에서 적용·롤백·RLS를 시험한다.

## 변경 불변성
article_revisions는 UPDATE하지 않는다. 수정은 새 revision과 parent_revision_id로 남기고 articles.current_revision_id만 낙관적 잠금으로 바꾼다. briefs와 profile_versions도 버전형이다. 모든 검수·export는 revision_id와 content_hash를 참조한다. claim statement를 변경하면 새 claim 버전을 생성하거나 영향을 받는 검수를 무효화해야 한다.

## 해시 정의 — R1 규범
불변 ArticleIR와 검수 문맥은 `HFBO-NFC-INT-1` 규칙으로 직렬화한 bytes의 SHA-256을 사용한다. 이는 RFC8785 JCS 구현이라고 주장하지 않는, 이 제품의 제한된 계약이다. 문자열·키 NFC, 유니코드 코드포인트 순서 정렬, bool/null 보존, 안전 정수값의 숫자만 허용한다. 소수는 필요한 스키마에서 decimal string으로 표현한다. NaN/Infinity·안전범위 밖 정수·비정상 surrogate·NFC 키 충돌은 거부한다. Python/JavaScript 실제 벡터 시험은 `reference_core/canonical.py`, `canonical.mjs`, `examples/r1/canonical_vectors.json`에 있다.

이 규칙은 모든 외부 JSON 수치를 바꾸는 것이 아니다. Datalab/성과의 ratio는 원본 숫자와 단위를 유지한다. 원문 bytes는 별도 원본 hash를 유지한다. HTTP idempotency request_hash는 검증된 동일 요청 bytes에 대한 서버 SHA-256이며 클라이언트가 계산한 값을 신뢰하지 않는다. 의미가 비슷해도 bytes가 다른 요청으로 같은 key를 재사용하면409를 반환할 수 있는 보수적 계약이다.

content_hash는 불변 ArticleIR 전체를 결속한다. 공개 본문 유사도는 별도 fingerprint다. 검수 문맥 hash는 article hash, 프로필, 브리프, 기회 질문·답·재검토 시점, claims, 근거, 원문 hash·read_scope·execution_mode·블로그 범위, 현재 소스 권한, 자산, 실제 경험기록, 정책버전을 결속한다. 점수/성공확률 필드는 포함하지 않는다. `reference_core/contracts.py:bundle_hash`가 결정적 참조다. 해시가 같다는 것은 내용의 진실성이 아니라 같은 입력이라는 뜻이다.

## FK와 범위
원고·작업·자산 연결은 tenant+blog+ID 복합 키로 교차 블로그 참조를 막는다. R1은 같은 블로그 안의 다른 글도 혼동하지 않도록 article_id+revision_id+content_hash까지 결속하고, export가 참조하는 review의 revision/hash도 일치시키는 FK를 추가한다. 공유 가능한 공개 근거는 tenant 범위에서 보관하되 별도 allowlist로 blog 사용을 제어한다. nullable blog_id를 ‘모두 접근 가능’으로 자동 해석하지 않는다. 개인 기억과 경험은 기본 blog 범위이며 공유는 명시적 승인과 새 scope grant가 필요하다.

## 유일성·인덱스
- source snapshot: tenant+source+canonical_url+content_hash.
- observation: provider+external_id+surface+observer_session+observed_at+filter_hash.
- topic reservation: tenant+event+question_fingerprint+answer_fingerprint, active 예약에 unique.
- job: tenant+idempotency_key, 단계별 stage_key와 retry attempt 분리.
- metric row: tenant+blog+platform+entity+metric+period+dimension_hash+source_revision.
- index: jobs(status,not_before,priority), opportunities(blog_id,status,rank), article_revisions(article_id,version), claims(valid_until), assets(expires_at), exports(valid_until).

## 지표 정규화
원본 보고서 파일은 변경 없이 hash를 보관하고 mapping_version으로 해석한다. 날짜 구간·timezone·보고서 갱신시각·단위·분모를 보존한다. 같은 보고서를 재가져오면 중복 추가하지 않고 import 상태를 반환한다. 나중 보고서가 확정치를 제공하면 source_revision을 올리고 이전 값을 숨기되 감사 이력은 보존한다. 월 누적과 일별을 동시에 합산하지 않는다.

## 상태의 정규 원본
JSON schema가 타입·필수필드를 정의하고 contracts/states.json이 상태 전이를 정의한다. DB에서는 유효값을 CHECK로 보조한다. 상태 전이·게이트 권한·해시 결속은 서버가 검증한다. OpenAPI에서는 임의 result JSON으로 전체 계약을 대체하지 않고 해당 스키마를 참조한다.

## 삭제·보존
권리·동의 만료는 새 사용을 차단하고 연결된 cache/export를 무효화한다. 실제 게시물은 이 서비스가 지울 수 없으므로 사용자에게 정정·삭제 요청을 제시한다. tenant 삭제는 원본·인덱스·캐시·export·backup retention에 걸친 절차로 실행한다. 기본 raw30일·업무로그90일·사용자 원고 지속보관은 제안값이며 source 권리가 더 짧으면 짧은 쪽을 따른다. 정확한 법적 보존기간으로 주장하지 않는다.

## R1: 생성 전 단계와 브리프
articles는 scoped opportunity_id를 필수로 갖고, 조사 전에는 brief_id가 NULL일 수 있다. BRIEF_READY 이후 제작 상태는 같은 opportunity/blog의 brief가 반드시 있어야 한다. ArticleCreate의 brief_id는 생략 가능하다. 완성 브리프를 만들려면 원고가 필요하고 원고를 만들려면 브리프가 필요한 순환을 만들지 않는다.

## R1: 공유 자료와 원본
sources/source_snapshots/evidence_items 모두 allowed_blog_ids를 명시한다. RLS는 현재 서버가 부여한 blog_ids와의 겹침을 읽기에, 부분집합을 쓰기에 적용한다. app.allow_shared만으로 전부 열지 않는다. claim_evidence 연결은 부모 원문과 소스의 현재 범위도 확인한다. 범위 회수는 연결·캐시·검수·내보내기를 무효화하고, 과거에 사용했다는 이유로 새 사용을 허용하지 않는다.

## R1: 실제 DB 시험의 범위
참조 DDL의 FK/RLS/트리거를 수정했지만 현재 환경에는 PostgreSQL 바이너리가 없어 적용하지 못했다. 설치도 네트워크 이름 해석 실패로 진행되지 않았다. 정적 FK 키 대응 검사는 PostgreSQL 문법·실제 RLS·동시성 시험을 대체하지 않는다. T053을 disposable PostgreSQL에서 실행하기 전에는 DB 보안 완료로 처리하지 않는다.
