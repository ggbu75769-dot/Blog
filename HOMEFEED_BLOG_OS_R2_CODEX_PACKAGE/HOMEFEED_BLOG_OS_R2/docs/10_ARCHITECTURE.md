# 10. 시스템 아키텍처·개발 구조

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 기본 구조
단일 저장소에 web, api, worker, shared-contracts를 두는 모듈형 구조다. 신규 프로젝트의 제안은 Next.js/TypeScript UI와 FastAPI/Python 업무·작업 워커, PostgreSQL, S3 호환 객체저장소다. 기존 저장소가 있으면 이 역할을 기존 스택에 매핑하는 ADR을 먼저 작성한다. 특정 버전·모델명을 추측해 고정하지 않고 M0에서 지원되는 안정 버전을 검증한 뒤 lockfile에 고정한다. 디자인이 다른 스택에도 적용되도록 도메인 계약을 독립시킨다.

```text
브라우저 → 인증된 업무 API → PostgreSQL
                              ├─ 프로필·원고·근거·성과
                              ├─ job_queue·events·lease
                              └─ idempotency·budget_ledger
                      worker → 허용 소스 / 모델 / 이미지 공급자
                             → 객체저장소 → 안전한 미리보기/ZIP
```

모든 외부 공개 발행 경로는 없다. /publish, /schedule-post, 네이버 로그인 세션, CMS write token을 생성하지 않는다. 수동 게시 기록 API는 로컬 메타데이터만 저장한다.

## 저장소 제안
apps/web: 화면·미리보기·복사·업로드·SSE.
apps/api: 인증·RBAC·입력 검증·사용자 액션.
workers/pipeline: 일정·조사·집필·검수·export 단계 실행.
packages/domain: 계약 생성 타입·상태·에러·ID.
packages/adapters: Naver 검색/Datalab·일반웹·모델·파일.
packages/renderers: ArticleIR→텍스트/HTML/Markdown/패키지.
packages/policies: 근거·자산·범위·신선도·출고 판정.
infra: 로컬 compose·migration·backup 작업.
tests: unit/contract/integration/replay/live/manual.
실제 생성 위치는 기존 저장소 점검 후 정하되 이 책임은 유지한다.

## 동기·비동기 경계
CRUD·검증·목록 조회는 요청 안에서 완료한다. 원문 수집·모델 호출·렌더·대량 import는 job으로202를 반환한다. API process가 종료돼도 작업은 DB에 남는다. SSE는 진행 표시용이며 상태의 원본은 DB다. 완료는 결과물 해시와 checkpoint commit 후 표시한다.

## 영속 작업 큐
기본 큐는 PostgreSQL의 행 잠금과 lease를 사용한다. SELECT FOR UPDATE SKIP LOCKED는 다른 소비자가 잠근 작업을 건너뛰는 큐형 처리에 사용할 수 있으나 일반 분석의 일관된 전체 보기로 사용하면 안 된다.[S12]
1. 짧은 트랜잭션에서 실행가능 job을 잠그고 lease_owner·lease_until·fencing_token을 증가시킨다.
2. 필요 비용을 예약하고 외부호출 intent를 생성한 뒤 commit한다.
3. 외부호출은 DB lock을 잡지 않은 상태에서 수행한다.
4. 결과 저장 시 현재 fencing_token과 일치할 때만 checkpoint를 확정한다.
5. lease를 잃은 worker의 늦은 응답은 채택하지 않고 별도 대사 대상으로 저장한다.
기본 lease120초·heartbeat30초·동시worker2는 시작 설정이다. 실제 공급자 시간과 부하 시험으로 변경한다.

## 모델 게이트웨이
실행 구성에는 provider, model_identifier, capability_probe_at, json_output_support, context_limit, token_budget, pricing_version, timeout, retention 조건을 둔다. 문서에 최신 모델 이름·단가를 임의로 적지 않는다. 구조화 출력이 지원되지 않으면 파서와 제한된 repair1회를 적용한다. 형식을 끝내 맞추지 못하면 안전하게 실패한다.

request_id와 prompt_version, input_evidence_hash, blog_profile_version, output_hash를 기록한다. 동일 입력의 캐시도 tenant/blog·권한·freshness 범위를 포함한다. 캐시된 검수결과는 문서가 변경되면 재사용할 수 없다. 고위험 판단은 작은 모델의 저렴한 추정만으로 대체하지 않는다.

## 데이터·파일 경계
원문·이미지·export는 private bucket에 저장하고 DB에는 key/hash를 둔다. 미리보기는 별도 origin 또는 엄격한 CSP sandbox로 제공한다. 사용자가 업로드한 HTML/script를 앱 권한으로 실행하지 않는다. 로그에는 키·개인 자료·긴 원문을 남기지 않는다.

## 확장 순서
한 인스턴스에서 재개·중복·권리·검수까지 구현한 뒤 worker 수를 늘린다. job 큐가 실제 병목이 되기 전 Redis·Kafka·별도 벡터DB를 도입하지 않는다. 실증 없는 ‘백만조회 대응’ 서버 확장은 금지한다. 백만 조회는 네이버에서 발생하는 콘텐츠 지표이지 우리 앱의 초당 요청량 목표가 아니다.


## R1: 추가 구조
동기 HTTP 쓰기 중복처리는 jobs key와 별개의 api_idempotency 테이블로 관리한다. 자동 생산의 대기열은 사용자의 실제 게시 가능 시간과 원고 유효기한을 함께 고려한다. 자료 탐색과 준비를 멈추지 않되 게시 전 만료될 원고의 신규 유료 집필은 REFRAME_OR_DEFER한다. 각 단계별 재시도 제한 외에 원고 전체 repair6회 초기 상한을 둔다. 미래 가중치/모델 최적화보다 이 참조 규칙을 실제 저장소·API·큐와 연결하는 T051~T060을 먼저 적용한다.
