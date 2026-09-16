# R1 구현·검증 상태

| 영역 | 현재 상태 | 실제 증거 또는 후속 조건 |
|---|---|---|
| 기획·설계·계약 개정 | 작성 완료 | docs00~30, schemas, contracts, api |
| 문서·스키마 검사 | 73 PASS / 0 FAIL | reports/DOCUMENT_VALIDATION.json |
| 추가 회귀검사 | 112 PASS / 0 FAIL | reports/R1_REGRESSION.json |
| 결정적 참조 규칙 | 일부 코드 제공·실행 | reference_core; 실제 앱 아님 |
| DB DDL·연결 | 정적 검사만 | 실제 PostgreSQL parse/migrate/RLS/concurrency NOT_RUN |
| 제품 작업60개 | NOT_STARTED | 제품 저장소가 제공되지 않음 |
| 제품 인수시험140개 | NOT_RUN | 명세와 실제 실행을 분리 |
| 실제 자료·모델·집필 연결 | NOT_RUN | 허용된 연결·예산·실제 앱 필요 |
| 자연스러움·수정시간 | NOT_RUN | 사람 평가 프로토콜과24설계시나리오만 제공 |
| 네이버·티스토리 에디터 | NOT_RUN | 사용자가 실제 비공개 편집기에서 수동 확인 |
| 홈피드·월100만 | 미검증 목표 | 실제 primary-blog 월별 통계 필요 |

추가 회귀검사의 구분: {"OFFLINE_REFERENCE": 91, "CROSS_LANGUAGE_EXECUTED": 6, "LOCAL_FILE_EXECUTED": 3, "STATIC_CONTRACT": 1, "STATIC_DDL_ONLY": 11}. 정적 검사는 실제 DB 실행이 아니다. 합성 REPLAY 출력에는 불량 HTML 문자를 넣은 음성 사례도 포함되므로 출고용 글로 쓰지 않는다.
