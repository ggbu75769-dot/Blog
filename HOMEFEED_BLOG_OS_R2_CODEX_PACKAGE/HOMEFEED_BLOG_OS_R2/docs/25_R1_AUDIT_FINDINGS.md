# 25. R1 결함 점검·수정 보고서

버전: 4.1.0-r1 · 기준일: 2026-09-15

기존 패키지 검사70건을 먼저 재실행해 전부 통과한 뒤 반례를 별도로 넣었다. 아래17건은 모두 운영 중 발생한 사고가 아니다. 스키마 검증 공백·실제 런타임 간 차이·정적 DDL/생명주기 모순을 구분한다. 기존 문서에 의도는 있어도 기계 계약과 검사가 강제하지 않는 부분을 수정했다.

| ID | 문제 | 기존 확인 | R1 조치 |
|---|---|---|---|
| B01 | 미갱신과 숫자0의 모순 | ACCEPTED / NEGATIVE_SCHEMA_PROBE | 상태→값 conditional schema 및 의미 검사 |
| B02 | 정의되지 않은 글 형식 | ACCEPTED / NEGATIVE_SCHEMA_PROBE | 기획/ArticleIR 글형식 enum 동기화 |
| B03 | 타입 라벨과 실제 payload 불일치 | ACCEPTED / NEGATIVE_SCHEMA_PROBE | payload_type과 실제 payload 스키마 결속 |
| B04 | 검증보다 먼저 만료되는 근거 | ACCEPTED / NEGATIVE_SCHEMA_PROBE | 검증/만료 시각 순서 검사 |
| B05 | 상위 경로로 탈출하는 파일명 | ACCEPTED / NEGATIVE_SCHEMA_PROBE | 경로 패턴+portable path+실제 파일 검사 |
| B06 | 실행 가능한 비HTTP 출처 URL | ACCEPTED / NEGATIVE_SCHEMA_PROBE | HTTP(S)와 호스트·자격증명 검사 |
| B07 | 근거·경험기록 없는 SUPPORTED 체험 | ACCEPTED / NEGATIVE_SCHEMA_PROBE | 필수 경험ID/근거+실제 허용 기록 조회 |
| B08 | 관측 구간 상하한 역전 | ACCEPTED / NEGATIVE_SCHEMA_PROBE | 상하한 순서와 반올림 정밀도 검사 |
| B09 | 근거 RLS가 블로그 allowlist를 검사하지 않음 | MISSING / STATIC_DDL_INSPECTION | evidence RLS의 blog allowlist 조건 |
| B10 | 공유 원문에 블로그별 범위가 없음 | MISSING / STATIC_DDL_INSPECTION | sources와 snapshot의 blog scope를 명시 |
| B11 | 부모 버전 FK가 같은 article을 강제하지 않음 | MISSING / STATIC_DDL_INSPECTION | 같은 article의 과거 parent revision만 허용 |
| B12 | 출력의 article과 revision을 별도 FK로만 검사함 | MISSING / STATIC_DDL_INSPECTION | article/revision/content_hash 복합FK |
| B13 | 출력의 검수보고서와 revision 결속이 없음 | MISSING / STATIC_DDL_INSPECTION | review/revision/content/bundle hash 복합FK |
| B14 | 정수값을 가진 float의 Python/JS 직렬화 차이 | MISMATCH / CROSS_LANGUAGE_EXECUTED | HFBO-NFC-INT-1과 실제 Python/Node 벡터 |
| B15 | articles.brief_id NOT NULL인데 사전 조사 상태도 Article에 포함됨 | INCONSISTENT_LIFECYCLE / STATIC_CONTRACT_INSPECTION | opportunity 필수·brief 초기nullable·제작상태 CHECK |
| B16 | 동기 API의 idempotency 저장 계약은 있으나 전용 DDL 없음 | MISSING / STATIC_DDL_INSPECTION | 동기 요청용 api_idempotency 추가 |
| B17 | 같은 metric 논리키의 current가 두 개일 수 있는 DDL | MISSING / STATIC_DDL_INSPECTION | 현재 수치 하나만 허용하는 unique 인덱스 |

## 수정 과정에서 추가로 잡은 것
공유 원문의 읽기 범위와 REPLAY 출처 표시를 세부 입력까지 보존했다. 최상위 실행 모드만 LIVE로 바꾸어도 REPLAY 원문은 거부한다. metadata만 확보한 자료를 완독한 본문 근거처럼 처리하지 않는다. 정적 SQL 검사기의 한 줄 테이블 처리 결함도 발견해 고쳤다. 이 마지막 항목은 제품 DB 결함이 아니라 검사기 자체의 결함이었다.

## 실행의 구분
1차 회귀 실행에서101통과/1실패가 나왔다. 실패는 정적 검사기가 한 줄 tenants 테이블을 잘못 묶는 문제였다. 수정 뒤102통과/0실패, 출처 범위·provenance 반례를 추가한 뒤105통과/0실패가 확인되었다. 최종 실제 숫자는 reports/R1_REGRESSION.json을 따른다. 정적 DB 검사는 실제 PostgreSQL 적용시험을 대신하지 않는다.

## 남은 운영 검증
PostgreSQL 실행 환경이 없어 실제 DDL 적용·RLS·동시성은 미실행이다. API/LLM 연결, 사람의 자연스러움 판단, 실제 네이버/티스토리 전송, 홈판 성과도 미실행이다. 이 항목은 문서에 체크를 표시해서 완료할 수 없으며 제품 release gate로 유지한다.
