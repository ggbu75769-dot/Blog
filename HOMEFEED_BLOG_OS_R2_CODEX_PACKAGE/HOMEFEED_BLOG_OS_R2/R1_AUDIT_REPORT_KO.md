# HOMEFEED BLOG OS R1 — 감사·수정·재검증 보고서

버전: 4.1.0-r1 | 기준일: 2026-09-15 | 공개 게시는 사용자가 수행한다.

## 결론

기존 최종 패키지의 문서 검사70건을 다시 실행해 통과한 뒤, 잘못된 입력·언어 간 동작·자료 연결을 별도로 점검했다. 17개 계약·검증 공백이 확인되어 스키마·참조 코드·API·SQL·문서·개발순서를 함께 수정했다. 운영 중 사고나 실제 서비스 취약점이 17개 발견됐다는 의미는 아니다.

최종 문서·계약 검사: **73 PASS / 0 FAIL**. 추가 회귀검사: **112 PASS / 0 FAIL**. 두 검사는 일부 겹치며 독립적인 제품 기능 전체를 검증한 것이 아니다.

## 사용자 결과물에 직접 영향 주는 수정

| 문제 | 발생할 수 있는 영향 | 수정 |
|---|---|---|
| 조사 전부터 완성 브리프 필수 | 주제→조사→기획 시작 경로가 막힘 | 초기 brief nullable, 집필 전 확정 brief 필요 |
| 미갱신 value 0 허용 | 아직 데이터 없는 글을 실패로 학습 | status/value 조건·null 보존 |
| 다른 글의 revision/review 연결 | 잘못된 원고를 검수 완료로 착각 | article/revision/content/bundle hash 결속 |
| 공유 근거의 블로그 범위 미강제 | 다른 채널 자료·경험 혼입 가능 | source/snapshot/evidence allowlist와 tenant 동시 확인 |
| Python/JS 해시 불일치 | 같은 원고의 버전·승인이 엇갈림 | 제한된 단일 정규화 계약 + 두 런타임 비교 |
| REPLAY 표시가 상단에만 존재 | 예제를 실제 조사·집필로 잘못 표시 | 원문 수준 실행 계보와 출고 모드 결속 |
| 권리·시간·최종 파일 점검 분리 부족 | 오래된 사실 또는 파일 없는 원고 전달 | 다운로드 전 근거·승인·파일 재검사 |

## 기획과 글쓰기 품질 보강

안전성 검사를 통과해도 글이 매력적이라는 뜻은 아니다. 기획에서는 같은 사건의 후보를 비교하고, 지금 읽을 이유·새로운 답·첫 화면·실제 자료·수동 게시 가능시점을 평가한다. 집필에서는 동일한 자료와 비용을 사용해 단일 프롬프트/기존 흐름/R1 흐름을 익명 비교한다.

평가 축은 첫 화면 기대 충족, 새로운 정보, 근거 충실도, 자연스러운 문체, 복사 준비도다. 독립적인 실제 평가자2명과 수정시간을 사용하도록 명세했다.24개 설계 시나리오는 만들었으나 실제 사람 평가나 LIVE 원고 생성의 성공 결과가 아니다. 평가실패·보류도 분모에 포함한다.

## 결함17건의 확인 방식

| ID | 발견 내용 | 확인 방식 |
|---|---|---|
| B01 | 미갱신과 숫자0의 모순 | NEGATIVE_SCHEMA_PROBE |
| B02 | 정의되지 않은 글 형식 | NEGATIVE_SCHEMA_PROBE |
| B03 | 타입 라벨과 실제 payload 불일치 | NEGATIVE_SCHEMA_PROBE |
| B04 | 검증보다 먼저 만료되는 근거 | NEGATIVE_SCHEMA_PROBE |
| B05 | 상위 경로로 탈출하는 파일명 | NEGATIVE_SCHEMA_PROBE |
| B06 | 실행 가능한 비HTTP 출처 URL | NEGATIVE_SCHEMA_PROBE |
| B07 | 근거·경험기록 없는 SUPPORTED 체험 | NEGATIVE_SCHEMA_PROBE |
| B08 | 관측 구간 상하한 역전 | NEGATIVE_SCHEMA_PROBE |
| B09 | 근거 RLS가 블로그 allowlist를 검사하지 않음 | STATIC_DDL_INSPECTION |
| B10 | 공유 원문에 블로그별 범위가 없음 | STATIC_DDL_INSPECTION |
| B11 | 부모 버전 FK가 같은 article을 강제하지 않음 | STATIC_DDL_INSPECTION |
| B12 | 출력의 article과 revision을 별도 FK로만 검사함 | STATIC_DDL_INSPECTION |
| B13 | 출력의 검수보고서와 revision 결속이 없음 | STATIC_DDL_INSPECTION |
| B14 | 정수값을 가진 float의 Python/JS 직렬화 차이 | CROSS_LANGUAGE_EXECUTED |
| B15 | articles.brief_id NOT NULL인데 사전 조사 상태도 Article에 포함됨 | STATIC_CONTRACT_INSPECTION |
| B16 | 동기 API의 idempotency 저장 계약은 있으나 전용 DDL 없음 | STATIC_DDL_INSPECTION |
| B17 | 같은 metric 논리키의 current가 두 개일 수 있는 DDL | STATIC_DDL_INSPECTION |

## 반복 수정 과정

기존70건 통과 → 추가 반례로17개 공백 확인 → 계약/코드 수정 → 1차 회귀101통과·1실패 → 한 줄 테이블을 잘못 읽은 정적 검사기 수정 → 102통과 → 출처범위/계보 반례 추가105통과 → 파일명 호환성 반례 추가112통과. 최종 계약 추적성 검사도73건 통과했다. 중간 실패를 삭제하지 않고 reports/ITERATION_1_REGRESSION.json에 보존했다.

## 실제 실행한 추가검사 분류

| 분류 | 건수 | 범위 |
|---|---:|---|
| OFFLINE_REFERENCE | 91 | 합성 입력으로 결정적 참조 함수·스키마 검사 |
| CROSS_LANGUAGE_EXECUTED | 6 | Python/Node 실제 byte·hash 대조 |
| LOCAL_FILE_EXECUTED | 3 | 실제 파일 생성·내용 보존·해시·symlink 거절 |
| STATIC_CONTRACT | 1 | API 등 계약 구조 검사 |
| STATIC_DDL_ONLY | 11 | SQL 텍스트의 연결·RLS 선언 확인. DB 실행 아님 |

## 명세 확장

31개 상세 문서,60개 요구사항,60개 개발 작업,140개 예정 제품 인수시험,24개 집필 평가 설계 시나리오,30개 도메인 타입,43개 내부 API,35개 참조 DB 테이블을 포함한다. 작업과 시험은 문서/JSON 간 양방향 추적검사를 통과했다.

## 남은 실증과 출시 조건

PostgreSQL 실행 도구가 없는 환경이고 패키지 확보도 네트워크/DNS 오류로 완료하지 못해 실제 DB 실행은 미실행이다. 참조 SQL을 검증된 migration처럼 적용하면 안 된다. 실제 HTTP 권한, 전체 LIVE 모델 파이프라인, 원문 의미 대조, 이미지 권리·디코딩, 사람 평가, 네이버/티스토리 입력, 홈판 노출·월100만은 각각 별도 출시 게이트다.

오프라인 검사로 결정할 수 있는 부분과 실제 결과가 필요한 부분을 분리했다. 발견한 공백에 대한 수정은 완료했지만, 전체 서비스의 무결함이나 흥행을 증명했다는 주장은 하지 않는다. 실제 운영 게이트를 생략하지 않는 것이 이번 개정의 완료 기준이다.

## Codex 실행 순서

CODEX_START_HERE.md를 전달하고 현재 저장소를 확인한 뒤 의존순서로 구현한다. 수정은 재현→실패 시험→코드 수정→회귀시험→문서 동기화 순서다. 한 원고가 주제선택에서 실제 복사 준비까지 이어지는 경로를 먼저 완성한다. 새 규칙이 모든 글을 거절하지 않는지 정상 fixture도 계속 통과시킨다.

## 출처 재확인

공식 원문 7개를 재확인했다: S01·S02·S05·S11·S13·S17·S18. S08은 이번 요청에서 공통 페이지 shell만 보여 본문 재확인 미완료로 표시했다. 다른 출처는 이전 확인 이력을 보존했고 이번에 모두 재조사한 것으로 쓰지 않았다. 세부 URL과 제한은 contracts/sources.json 및 docs/21에 있다.
