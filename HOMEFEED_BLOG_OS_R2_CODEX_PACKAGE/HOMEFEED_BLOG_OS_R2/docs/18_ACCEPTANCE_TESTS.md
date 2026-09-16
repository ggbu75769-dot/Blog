# 18. 인수시험 명세 — R1

버전: 4.1.0-r1. 140개는 제품 인수시험 계획이며 전부 NOT_RUN. 오프라인 실행 결과는 별도 reports에 있다.

## AT-001 · 저장소 기준선과 범위 동결 / 정상

작업: T001 | 요구: REQ-001 | 계층: RELEASE_EVIDENCE | 상태: NOT_RUN

**Given:** 기존 저장소·최종 문서 (정상 범위)

**When:** branch/status/변경파일과 기존 AGENTS를 확인하고 스택·경로·미입력을 분리해 기록

**Then:** 사용자 변경이 보존되고 자동게시 제외가 확정됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-002 · 저장소 기준선과 범위 동결 / 오류·경계

작업: T001 | 요구: REQ-001 | 계층: RELEASE_EVIDENCE | 상태: NOT_RUN

**Given:** 기존 저장소·최종 문서 (부적격·상충·경계 입력 주입)

**When:** branch/status/변경파일과 기존 AGENTS를 확인하고 스택·경로·미입력을 분리해 기록

**Then:** 기존 변경을 덮어쓰거나 새 게시기능을 포함하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-003 · 계약 검증 도구 연결 / 정상

작업: T002 | 요구: REQ-002 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** schemas·states·OpenAPI·tasks (정상 범위)

**When:** 스키마검사·참조해결·추적행렬·버전검사를 CI에 연결

**Then:** 정상 fixtures와 문서 참조가 검증됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-004 · 계약 검증 도구 연결 / 오류·경계

작업: T002 | 요구: REQ-002 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** schemas·states·OpenAPI·tasks (부적격·상충·경계 입력 주입)

**When:** 스키마검사·참조해결·추적행렬·버전검사를 CI에 연결

**Then:** 미정의 상태·없는 AT·깨진 ref를 거부

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-005 · 공급자·운영 입력 진단 / 정상

작업: T003 | 요구: REQ-003 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** source registry·키의 존재여부 (정상 범위)

**When:** configured와 permitted와 actual_probe를 나누고 비용없는 사전검사부터 실행

**Then:** 미연결은 NOT_CONFIGURED로 나옴

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-006 · 공급자·운영 입력 진단 / 오류·경계

작업: T003 | 요구: REQ-003 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** source registry·키의 존재여부 (부적격·상충·경계 입력 주입)

**When:** configured와 permitted와 actual_probe를 나누고 비용없는 사전검사부터 실행

**Then:** 키 없이 LIVE 수집 성공을 표시하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-007 · DB·저장소 개발환경 / 정상

작업: T004 | 요구: REQ-004 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 참조DDL·스택 ADR (정상 범위)

**When:** 격리된 DB와 object store를 구성하고 migration apply/restore 시험

**Then:** 빈 DB에서 원고·작업 데이터를 저장함

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-008 · DB·저장소 개발환경 / 오류·경계

작업: T004 | 요구: REQ-004 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 참조DDL·스택 ADR (부적격·상충·경계 입력 주입)

**When:** 격리된 DB와 object store를 구성하고 migration apply/restore 시험

**Then:** 운영 DB에 무검증 참조DDL 실행을 거부

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-009 · 인증·tenant/blog 격리 / 정상

작업: T005 | 요구: REQ-005 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 권한표·tenant context (정상 범위)

**When:** 앱 role·RLS·복합FK·파일/캐시 scope를 구현

**Then:** 자기 블로그 데이터만 조회됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-010 · 인증·tenant/blog 격리 / 오류·경계

작업: T005 | 요구: REQ-005 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 권한표·tenant context (부적격·상충·경계 입력 주입)

**When:** 앱 role·RLS·복합FK·파일/캐시 scope를 구현

**Then:** 다른 tenant ID와 개인기록 접근은404/403

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-011 · 블로그·문체 버전 관리 / 정상

작업: T006 | 요구: REQ-006 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 승인 주제·문체 샘플 (정상 범위)

**When:** 초기 설정·프로필버전·활성/중지·core/adjacent/excluded 관리

**Then:** 두 프로필의 편집 기준이 다르게 적용됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-012 · 블로그·문체 버전 관리 / 오류·경계

작업: T006 | 요구: REQ-006 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 승인 주제·문체 샘플 (부적격·상충·경계 입력 주입)

**When:** 초기 설정·프로필버전·활성/중지·core/adjacent/excluded 관리

**Then:** 프로필 변경이 기존 원고를 무단 덮어쓰면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-013 · 실제 사실·경험 기억 / 정상

작업: T007 | 요구: REQ-007 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 사용자 승인자료·경험 (정상 범위)

**When:** 경험의 대상·기간·blog scope·증빙과 문체예문을 분리

**Then:** 승인한 실제 경험만 맞는 글에서 사용

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-014 · 실제 사실·경험 기억 / 오류·경계

작업: T007 | 요구: REQ-007 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 사용자 승인자료·경험 (부적격·상충·경계 입력 주입)

**When:** 경험의 대상·기간·blog scope·증빙과 문체예문을 분리

**Then:** 예문 속 여행을 실제 경험으로 등록하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-015 · 업로드·자산 권리 / 정상

작업: T008 | 요구: REQ-008 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 원본 파일·사용권 (정상 범위)

**When:** quarantine·MIME/hash·scope·만료·caption을 구현

**Then:** 허가된 실파일만 READY

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-016 · 업로드·자산 권리 / 오류·경계

작업: T008 | 요구: REQ-008 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 원본 파일·사용권 (부적격·상충·경계 입력 주입)

**When:** quarantine·MIME/hash·scope·만료·caption을 구현

**Then:** MIME위장·누락파일·타블로그권리는 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-017 · 허용 원문 reader·SSRF 방어 / 정상

작업: T009 | 요구: REQ-009 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** source permission·URL (정상 범위)

**When:** DNS/redirect/크기/시간제한·HTML정제·read_scope를 구현

**Then:** 실제 읽은 구간과 hash 저장

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-018 · 허용 원문 reader·SSRF 방어 / 오류·경계

작업: T009 | 요구: REQ-009 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** source permission·URL (부적격·상충·경계 입력 주입)

**When:** DNS/redirect/크기/시간제한·HTML정제·read_scope를 구현

**Then:** 메타데이터IP·빈셸을 원문성공 처리하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-019 · Naver 검색 어댑터 / 정상

작업: T010 | 요구: REQ-010 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 앱자격·query·sort (정상 범위)

**When:** 공식요청 validation·결과정제·쿼터·snapshot을 구현

**Then:** display/start/sort와 실제결과 저장

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-020 · Naver 검색 어댑터 / 오류·경계

작업: T010 | 요구: REQ-010 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 앱자격·query·sort (부적격·상충·경계 입력 주입)

**When:** 공식요청 validation·결과정제·쿼터·snapshot을 구현

**Then:** total을 PV로 쓰거나 무한429재시도하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-021 · Datalab 어댑터 / 정상

작업: T011 | 요구: REQ-011 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** keywordGroups·기간·필터 (정상 범위)

**When:** 요청fingerprint·date/week/month·ratio를 보존

**Then:** 같은조건 상대추세만 비교

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-022 · Datalab 어댑터 / 오류·경계

작업: T011 | 요구: REQ-011 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** keywordGroups·기간·필터 (부적격·상충·경계 입력 주입)

**When:** 요청fingerprint·date/week/month·ratio를 보존

**Then:** 다른요청 ratio병합·분단위 검색량 표시는 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-023 · 선택형 유튜브·SNS 입력 / 정상

작업: T012 | 요구: REQ-012 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 허가 provider 또는 import (정상 범위)

**When:** metadata/transcript/visual 범위를 분리하고 미연결을 표시

**Then:** 자막자료는 자막분석 범위로 저장

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-024 · 선택형 유튜브·SNS 입력 / 오류·경계

작업: T012 | 요구: REQ-012 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 허가 provider 또는 import (부적격·상충·경계 입력 주입)

**When:** metadata/transcript/visual 범위를 분리하고 미연결을 표시

**Then:** 자막만으로 화면확인·유지율을 채우면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-025 · 홈피드 관측 import / 정상

작업: T013 | 요구: REQ-013 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** surface/session/time/card 자료 (정상 범위)

**When:** 표면·개인화·세션·카드중복·반올림을 정규화

**Then:** 실제 HOMEFEED 표본만 별도 집계

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-026 · 홈피드 관측 import / 오류·경계

작업: T013 | 요구: REQ-013 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** surface/session/time/card 자료 (부적격·상충·경계 입력 주입)

**When:** 표면·개인화·세션·카드중복·반올림을 정규화

**Then:** 검색결과나 일반모바일 ref를 홈판으로 변경 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-027 · 사건 군집·원출처 계열 / 정상

작업: T014 | 요구: REQ-014 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 관측·원문메타 (정상 범위)

**When:** occurred/published/seen 분리·독립원출처·동일사건 묶기

**Then:** 재인용5개가 같은 fact계열로 연결

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-028 · 사건 군집·원출처 계열 / 오류·경계

작업: T014 | 요구: REQ-014 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 관측·원문메타 (부적격·상충·경계 입력 주입)

**When:** occurred/published/seen 분리·독립원출처·동일사건 묶기

**Then:** 오래된사건 재게시를 신규사건으로 확정하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-029 · 수요·편집 우선순위 / 정상

작업: T015 | 요구: REQ-015 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 관측·가설가중치 (정상 범위)

**When:** 누락항0·coverage·표본한계·gate를 분리해 rank 계산

**Then:** 점수와 근거·누락이 같이 출력

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-030 · 수요·편집 우선순위 / 오류·경계

작업: T015 | 요구: REQ-015 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 관측·가설가중치 (부적격·상충·경계 입력 주입)

**When:** 누락항0·coverage·표본한계·gate를 분리해 rank 계산

**Then:** 점수를 홈판확률로 표시하거나 누락 재정규화 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-031 · 멀티블로그 배정·중복 예약 / 정상

작업: T016 | 요구: REQ-016 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 질문·답·profile (정상 범위)

**When:** 의미비교·scope·unique reservation을 transaction으로 구현

**Then:** 동시요청에도 동일기획1개 배정

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-032 · 멀티블로그 배정·중복 예약 / 오류·경계

작업: T016 | 요구: REQ-016 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 질문·답·profile (부적격·상충·경계 입력 주입)

**When:** 의미비교·scope·unique reservation을 transaction으로 구현

**Then:** 말투만바꾼 동일글 다중배정은 거부

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-033 · 근거팩 조사 파이프라인 / 정상

작업: T017 | 요구: REQ-017 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 기획 질문·원문 (정상 범위)

**When:** 필요 claim·locator·독립근거·읽기범위·권한을 구성

**Then:** 실제 근거가있는 주장만 SUPPORTED

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-034 · 근거팩 조사 파이프라인 / 오류·경계

작업: T017 | 요구: REQ-017 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 기획 질문·원문 (부적격·상충·경계 입력 주입)

**When:** 필요 claim·locator·독립근거·읽기범위·권한을 구성

**Then:** 스니펫만으로 중요한 최신사실 검증완료 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-035 · 주장·상충·정정 연결 / 정상

작업: T018 | 요구: REQ-018 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** ResearchPack (정상 범위)

**When:** 주장종류·scope·valid_until·conflict·영향원고 연결

**Then:** 상충·범위차이를 구분하고 보류

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-036 · 주장·상충·정정 연결 / 오류·경계

작업: T018 | 요구: REQ-018 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** ResearchPack (부적격·상충·경계 입력 주입)

**When:** 주장종류·scope·valid_until·conflict·영향원고 연결

**Then:** 모델다수결·최신날짜만으로 충돌해소 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-037 · 내용 기획·새 기여 / 정상

작업: T019 | 요구: REQ-019 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** reader question·근거 (정상 범위)

**When:** 답·정보빈칸·논지·section목적·중단조건을 구조화

**Then:** 기존글과 다른 비교/해석/절차가 지정됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-038 · 내용 기획·새 기여 / 오류·경계

작업: T019 | 요구: REQ-019 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** reader question·근거 (부적격·상충·경계 입력 주입)

**When:** 답·정보빈칸·논지·section목적·중단조건을 구조화

**Then:** 키워드만 있고 새답이 없는 브리프 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-039 · 제목·이미지·첫문단 계획 / 정상

작업: T020 | 요구: REQ-020 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 최종답·근거·시각가능성 (정상 범위)

**When:** 제목8/이미지방향3/도입2를 만든 뒤 약속일치로 선별

**Then:** 제목의숫자와 비교가 본문답과 연결

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-040 · 제목·이미지·첫문단 계획 / 오류·경계

작업: T020 | 요구: REQ-020 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 최종답·근거·시각가능성 (부적격·상충·경계 입력 주입)

**When:** 제목8/이미지방향3/도입2를 만든 뒤 약속일치로 선별

**Then:** 내용과무관한 부·몸무게·충격표현으로 후킹 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-041 · 모델 게이트웨이·계약 / 정상

작업: T021 | 요구: REQ-021 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** model/key/pricing·schemas (정상 범위)

**When:** 역할별입력·structured output·repair·토큰/비용·hash 기록

**Then:** 정상응답을 typed output으로 저장

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-042 · 모델 게이트웨이·계약 / 오류·경계

작업: T021 | 요구: REQ-021 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** model/key/pricing·schemas (부적격·상충·경계 입력 주입)

**When:** 역할별입력·structured output·repair·토큰/비용·hash 기록

**Then:** 실패 JSON·미지원모델·예산없음은 fail closed

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-043 · 내용 중심 집필기 / 정상

작업: T022 | 요구: REQ-022 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** Brief·Evidence·Profile (정상 범위)

**When:** 새사실 필요시 research request, claim별 논리초안 생성

**Then:** 근거 범위 안에서 완결한 답 작성

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-044 · 내용 중심 집필기 / 오류·경계

작업: T022 | 요구: REQ-022 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** Brief·Evidence·Profile (부적격·상충·경계 입력 주입)

**When:** 새사실 필요시 research request, claim별 논리초안 생성

**Then:** 없는 1인칭·숫자·출처를 추가하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-045 · 반대 검토·논리 점검 / 정상

작업: T023 | 요구: REQ-023 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 초안·실제근거 (정상 범위)

**When:** 예외·인과비약·비교대상·상관·전문성오인 검사

**Then:** 조건다른비교와 과도단정을 발견

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-046 · 반대 검토·논리 점검 / 오류·경계

작업: T023 | 요구: REQ-023 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 초안·실제근거 (부적격·상충·경계 입력 주입)

**When:** 예외·인과비약·비교대상·상관·전문성오인 검사

**Then:** 작성자 자기점수만 신뢰하면 실패

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-047 · 블로그별 문체 편집 / 정상

작업: T024 | 요구: REQ-024 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 검토초안·허가예문·profile (정상 범위)

**When:** 추상반복·리듬·최근구조를 고치고 내용은 유지

**Then:** 같은자료도 적합한 관점·말투로 편집

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-048 · 블로그별 문체 편집 / 오류·경계

작업: T024 | 요구: REQ-024 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 검토초안·허가예문·profile (부적격·상충·경계 입력 주입)

**When:** 추상반복·리듬·최근구조를 고치고 내용은 유지

**Then:** 타블로그 경험·고의오타·상투패턴 반복 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-049 · 최종 본문 의미 재검수 / 정상

작업: T025 | 요구: REQ-025 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 편집후제목·본문·표·캡션 (정상 범위)

**When:** 주장 재추출·orphan·숫자/주체/범위·인용대조

**Then:** 일부→전체 변경과 고아주장을 잡음

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-050 · 최종 본문 의미 재검수 / 오류·경계

작업: T025 | 요구: REQ-025 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 편집후제목·본문·표·캡션 (부적격·상충·경계 입력 주입)

**When:** 주장 재추출·orphan·숫자/주체/범위·인용대조

**Then:** 초안만 검사하거나 모델발급 통과문구 수용 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-051 · 결정적 출고 게이트 / 정상

작업: T026 | 요구: REQ-026 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** revision·review·assets·policy (정상 범위)

**When:** 스키마/hash/expiry/scope/marker/파일조건을 서버에서 검사

**Then:** 모두 유효한 원고만 출고후보

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-052 · 결정적 출고 게이트 / 오류·경계

작업: T026 | 요구: REQ-026 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** revision·review·assets·policy (부적격·상충·경계 입력 주입)

**When:** 스키마/hash/expiry/scope/marker/파일조건을 서버에서 검사

**Then:** stale review·다른버전·없는자산은 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-053 · 자산 Resolver·대안 처리 / 정상

작업: T027 | 요구: REQ-027 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** visual need·rights·budget (정상 범위)

**When:** 실제파일 확보·캡션·설명그림 구분·권리만료·대안기획

**Then:** 필수이미지는 실제 파일로 존재

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-054 · 자산 Resolver·대안 처리 / 오류·경계

작업: T027 | 요구: REQ-027 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** visual need·rights·budget (부적격·상충·경계 입력 주입)

**When:** 실제파일 확보·캡션·설명그림 구분·권리만료·대안기획

**Then:** 프롬프트를 자산으로 세거나 가짜효과사진 대체 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-055 · ArticleIR 렌더러 / 정상

작업: T028 | 요구: REQ-028 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** typed IR·assets (정상 범위)

**When:** TXT/HTML/MD·표·공개출처·escape·parity 생성

**Then:** 모든공개 block과 출처가 보존됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-056 · ArticleIR 렌더러 / 오류·경계

작업: T028 | 요구: REQ-028 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** typed IR·assets (부적격·상충·경계 입력 주입)

**When:** TXT/HTML/MD·표·공개출처·escape·parity 생성

**Then:** script·내부 claimID·private메모 누출 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-057 · 네이버 수동 전송·복사 / 정상

작업: T029 | 요구: REQ-029 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** IR·실제이미지·캡션 (정상 범위)

**When:** 제목/전체/블록복사·이미지순서·fallback·가이드

**Then:** 클립보드실패도 TXT로 이어서 사용

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-058 · 네이버 수동 전송·복사 / 오류·경계

작업: T029 | 요구: REQ-029 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** IR·실제이미지·캡션 (부적격·상충·경계 입력 주입)

**When:** 제목/전체/블록복사·이미지순서·fallback·가이드

**Then:** 로컬이미지 자동전송·실에디터완벽보존 주장 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-059 · 티스토리·자체블로그 media-map / 정상

작업: T030 | 요구: REQ-030 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 수동업로드 image URL mapping (정상 범위)

**When:** local refs→검증URL 변환·새hash·누락검사

**Then:** 모든필수이미지URL과 캡션이 일치

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-060 · 티스토리·자체블로그 media-map / 오류·경계

작업: T030 | 요구: REQ-030 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 수동업로드 image URL mapping (부적격·상충·경계 입력 주입)

**When:** local refs→검증URL 변환·새hash·누락검사

**Then:** 깨진URL·외부스크립트·자동게시 옵션 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-061 · Export manifest·다운로드 / 정상

작업: T031 | 요구: REQ-031 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** revision·gate·자산 (정상 범위)

**When:** public-only/전체분리·path/hash·zip·다운로드권한

**Then:** manifest와 실제파일·scope가 일치

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-062 · Export manifest·다운로드 / 오류·경계

작업: T031 | 요구: REQ-031 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** revision·gate·자산 (부적격·상충·경계 입력 주입)

**When:** public-only/전체분리·path/hash·zip·다운로드권한

**Then:** ../·절대경로·만료링크·private공개는 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-063 · 대기원고 신선도·정정 / 정상

작업: T032 | 요구: REQ-032 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** valid_until·sourcechange (정상 범위)

**When:** 다운로드재검사·영향원고추적·재조사·정정안 생성

**Then:** 만료시 READY해제와 재검토

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-064 · 대기원고 신선도·정정 / 오류·경계

작업: T032 | 요구: REQ-032 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** valid_until·sourcechange (부적격·상충·경계 입력 주입)

**When:** 다운로드재검사·영향원고추적·재조사·정정안 생성

**Then:** 옛 export를 최신확인된것처럼 제공 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-065 · 영속 큐·lease·fencing / 정상

작업: T033 | 요구: REQ-033 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** job state·DB (정상 범위)

**When:** 잠금·짧은transaction·heartbeat·checkpoint·fencing

**Then:** 재시작해도 같은단계 중복commit 없음

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-066 · 영속 큐·lease·fencing / 오류·경계

작업: T033 | 요구: REQ-033 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** job state·DB (부적격·상충·경계 입력 주입)

**When:** 잠금·짧은transaction·heartbeat·checkpoint·fencing

**Then:** lease잃은worker 결과 채택 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-067 · 예산 예약·유료호출 intent / 정상

작업: T034 | 요구: REQ-034 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 승인예산·가격버전 (정상 범위)

**When:** tenant/blog 순서잠금·reserve·actual·unknown 대사

**Then:** 동시요청도 spent+reserved≤cap

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-068 · 예산 예약·유료호출 intent / 오류·경계

작업: T034 | 요구: REQ-034 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 승인예산·가격버전 (부적격·상충·경계 입력 주입)

**When:** tenant/blog 순서잠금·reserve·actual·unknown 대사

**Then:** timeout을0원처리·무제한재호출 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-069 · 예외함·제한재시도 / 정상

작업: T035 | 요구: REQ-035 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** stage failure·대안 (정상 범위)

**When:** 재시도가능성·자료요청·대안·hold·cancel 구현

**Then:** 한원고예외여도 다른적격원고 계속

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-070 · 예외함·제한재시도 / 오류·경계

작업: T035 | 요구: REQ-035 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** stage failure·대안 (부적격·상충·경계 입력 주입)

**When:** 재시도가능성·자료요청·대안·hold·cancel 구현

**Then:** force_pass·동일오류 무한재시도 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-071 · 일정·대기열 자동운영 / 정상

작업: T036 | 요구: REQ-036 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 프로필일정·상한·대기열 (정상 범위)

**When:** cadence dedupe·늦은tick처리·queue cap·source watermark

**Then:** 키워드수동입력없이 정상 파이프라인 시작

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-072 · 일정·대기열 자동운영 / 오류·경계

작업: T036 | 요구: REQ-036 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 프로필일정·상한·대기열 (부적격·상충·경계 입력 주입)

**When:** cadence dedupe·늦은tick처리·queue cap·source watermark

**Then:** 적체중 계속집필·중복tick 과금 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-073 · 원고 편집·검수 UI / 정상

작업: T037 | 요구: REQ-037 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** IR·revision·gate (정상 범위)

**When:** 읽기/검수탭·diff·IfMatch·부분수정·접근성

**Then:** 수정 후 새revision·검수대기 표시

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-074 · 원고 편집·검수 UI / 오류·경계

작업: T037 | 요구: REQ-037 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** IR·revision·gate (부적격·상충·경계 입력 주입)

**When:** 읽기/검수탭·diff·IfMatch·부분수정·접근성

**Then:** 충돌저장·내부메모 공개탭 누출 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-075 · 기회·자료 연구 UI / 정상

작업: T038 | 요구: REQ-038 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 관측·기획·근거 (정상 범위)

**When:** 왜지금·새답·근거/누락·배정·보류이유

**Then:** 검색·홈판·SNS 증거 유형이 구분됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-076 · 기회·자료 연구 UI / 오류·경계

작업: T038 | 요구: REQ-038 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 관측·기획·근거 (부적격·상충·경계 입력 주입)

**When:** 왜지금·새답·근거/누락·배정·보류이유

**Then:** 타인비공개통계나 예측확률 조작 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-077 · 오늘·온보딩 UI / 정상

작업: T039 | 요구: REQ-039 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 프로필·예외·ready·예산 (정상 범위)

**When:** 첫설정·상태/빈화면·모바일·stop/resume

**Then:** 오늘완성원고와 다음행동이 명확함

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-078 · 오늘·온보딩 UI / 오류·경계

작업: T039 | 요구: REQ-039 | 계층: CONTRACT_OR_UNIT | 상태: NOT_RUN

**Given:** 프로필·예외·ready·예산 (부적격·상충·경계 입력 주입)

**When:** 첫설정·상태/빈화면·모바일·stop/resume

**Then:** 미설정/미갱신을 성공/0으로 표시 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-079 · 수동 게시 기록 / 정상

작업: T040 | 요구: REQ-040 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 사용자 URL·시각·version (정상 범위)

**When:** 로컬저장·scope·수정본차이·USER_RECORDED 상태

**Then:** 원고와 게시기록이 별도 연결됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-080 · 수동 게시 기록 / 오류·경계

작업: T040 | 요구: REQ-040 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 사용자 URL·시각·version (부적격·상충·경계 입력 주입)

**When:** 로컬저장·scope·수정본차이·USER_RECORDED 상태

**Then:** 네트워크 write·URL만으로 VERIFIED 표시 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-081 · 성과 import·매핑·revision / 정상

작업: T041 | 요구: REQ-041 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 사용자 보고서 파일 (정상 범위)

**When:** dry-run·분모/기간·중복·최신revision·unknown

**Then:** 재업로드중복없고 미갱신이 구분됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-082 · 성과 import·매핑·revision / 오류·경계

작업: T041 | 요구: REQ-041 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 사용자 보고서 파일 (부적격·상충·경계 입력 주입)

**When:** dry-run·분모/기간·중복·최신revision·unknown

**Then:** ratio×PV·월누적+일별중복합산 차단

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-083 · 조회목표·품질·비용 보고서 / 정상

작업: T042 | 요구: REQ-042 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 실제metrics·cost·edits (정상 범위)

**When:** 주력/합계분리·월경계·창성숙도·지표정의

**Then:** 주력100만과 다른채널합계 별도

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-084 · 조회목표·품질·비용 보고서 / 오류·경계

작업: T042 | 요구: REQ-042 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 실제metrics·cost·edits (부적격·상충·경계 입력 주입)

**When:** 주력/합계분리·월경계·창성숙도·지표정의

**Then:** 미게시원고를0PV실패로 학습 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-085 · 실험·수정 학습 / 정상

작업: T043 | 요구: REQ-043 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 실제결과·수정diff·버전 (정상 범위)

**When:** 사전가설·holdout·shadow·제한적용·rollback

**Then:** 문체수정과 사실수정이 다르게 반영

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-086 · 실험·수정 학습 / 오류·경계

작업: T043 | 요구: REQ-043 | 계층: APPLICATION_INTEGRATION | 상태: NOT_RUN

**Given:** 실제결과·수정diff·버전 (부적격·상충·경계 입력 주입)

**When:** 사전가설·holdout·shadow·제한적용·rollback

**Then:** 가상독자/자기점수/단일대박을실증으로 표시 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-087 · 공격·격리·공개패키지 검증 / 정상

작업: T044 | 요구: REQ-044 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 악성URL/HTML/파일/범위 fixture (정상 범위)

**When:** prompt injection·SSRF·XSS·scope·private export 시험

**Then:** 공격입력 차단과 감사가 확인됨

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-088 · 공격·격리·공개패키지 검증 / 오류·경계

작업: T044 | 요구: REQ-044 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 악성URL/HTML/파일/범위 fixture (부적격·상충·경계 입력 주입)

**When:** prompt injection·SSRF·XSS·scope·private export 시험

**Then:** 문서만있고 실제 악성시험 skip은 미통과

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-089 · 두 블로그 replay E2E / 정상

작업: T045 | 요구: REQ-045 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 고정 source·두profile (정상 범위)

**When:** 기획부터원고·출력·restart까지 실제흐름 실행

**Then:** 각블로그 완성원고와 scope가 맞음

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-090 · 두 블로그 replay E2E / 오류·경계

작업: T045 | 요구: REQ-045 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** 고정 source·두profile (부적격·상충·경계 입력 주입)

**When:** 기획부터원고·출력·restart까지 실제흐름 실행

**Then:** fixture를 LIVE 관심/성과로 표시 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-091 · 실제 소스·모델 E2E / 정상

작업: T046 | 요구: REQ-046 | 계층: LIVE | 상태: NOT_RUN

**Given:** 승인된키·원문·예산 (정상 범위)

**When:** 실제요청·글생성·최종근거대조·비용기록

**Then:** source→HANDOFF_READY실경로 증거

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-092 · 실제 소스·모델 E2E / 오류·경계

작업: T046 | 요구: REQ-046 | 계층: LIVE | 상태: NOT_RUN

**Given:** 승인된키·원문·예산 (부적격·상충·경계 입력 주입)

**When:** 실제요청·글생성·최종근거대조·비용기록

**Then:** 미입력시 BLOCKED를pass로 집계 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-093 · 실제 에디터 수동 호환성 / 정상

작업: T047 | 요구: REQ-047 | 계층: MANUAL | 상태: NOT_RUN

**Given:** 사용자 에디터·완성패키지 (정상 범위)

**When:** 텍스트/표/이미지형 각전송·모바일·출처 확인

**Then:** 복사·삽입후 누락없이 보임

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-094 · 실제 에디터 수동 호환성 / 오류·경계

작업: T047 | 요구: REQ-047 | 계층: MANUAL | 상태: NOT_RUN

**Given:** 사용자 에디터·완성패키지 (부적격·상충·경계 입력 주입)

**When:** 텍스트/표/이미지형 각전송·모바일·출처 확인

**Then:** 로컬preview만으로 실에디터 통과 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-095 · 30편 블라인드 품질 평가 / 정상

작업: T048 | 요구: REQ-048 | 계층: MANUAL | 상태: NOT_RUN

**Given:** 실제원고30·평가자2 (정상 범위)

**When:** 익명평가·수정시간·사실검사·점수불일치 보존

**Then:** 중대오류0·목표점수 충족

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-096 · 30편 블라인드 품질 평가 / 오류·경계

작업: T048 | 요구: REQ-048 | 계층: MANUAL | 상태: NOT_RUN

**Given:** 실제원고30·평가자2 (부적격·상충·경계 입력 주입)

**When:** 익명평가·수정시간·사실검사·점수불일치 보존

**Then:** AI평가를 인간평가로 세거나 실패원고 제외 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-097 · 부하·복구·관측·운영복귀 / 정상

작업: T049 | 요구: REQ-049 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** job부하·backup·failures (정상 범위)

**When:** 10profile격리·worker kill·복원·로그·rollback 시험

**Then:** 실제복구·hash·예약대사 확인

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-098 · 부하·복구·관측·운영복귀 / 오류·경계

작업: T049 | 요구: REQ-049 | 계층: INTEGRATION | 상태: NOT_RUN

**Given:** job부하·backup·failures (부적격·상충·경계 입력 주입)

**When:** 10profile격리·worker kill·복원·로그·rollback 시험

**Then:** 미측정 SLO를달성실적으로 기재 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-099 · 릴리스 인수·실행문서 / 정상

작업: T050 | 요구: REQ-050 | 계층: RELEASE_EVIDENCE | 상태: NOT_RUN

**Given:** 전체AT·실행로그·배포계획 (정상 범위)

**When:** 완료/미실행·의존성·보안·설정·알려진한계 정리

**Then:** 실행증거가있는범위만 완료기재

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-100 · 릴리스 인수·실행문서 / 오류·경계

작업: T050 | 요구: REQ-050 | 계층: RELEASE_EVIDENCE | 상태: NOT_RUN

**Given:** 전체AT·실행로그·배포계획 (부적격·상충·경계 입력 주입)

**When:** 완료/미실행·의존성·보안·설정·알려진한계 정리

**Then:** 자동게시 재도입·근거없는월100만보장 금지

**증거:** 입력 fixture 또는 실제자료 범위, 실행명령·결과·버전·대상, 출력/오류 기록

## AT-101 · 정규화·해시 계약과 Python/Node 동등성 / AT-101

작업: T051 | 요구: REQ-051 | 계층: CANONICAL_CROSS_RUNTIME | 상태: NOT_RUN

**Given:** 6개 정상 JSON 벡터를 두 구현에 입력

**When:** UTF-8 byte 및 SHA256 비교

**Then:** 값이 모두 일치하고 계약 버전이 기록됨

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-102 · 정규화·해시 계약과 Python/Node 동등성 / AT-102

작업: T051 | 요구: REQ-051 | 계층: CANONICAL_NEGATIVE | 상태: NOT_RUN

**Given:** NFC 충돌키·분수·범위초과·NaN

**When:** 각 입력 정규화 시도

**Then:** 명시적 오류로 중단하며 값을 강제로 변경하지 않음

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-103 · 정규화·해시 계약과 Python/Node 동등성 / AT-103

작업: T051 | 요구: REQ-051 | 계층: CANONICAL_RAW_BYTES | 상태: NOT_RUN

**Given:** 동일 의미지만 다른 HTTP body bytes

**When:** 같은 idempotency 키로 재전송

**Then:** 기존 raw hash와 다르면 conflict 처리

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-104 · 정규화·해시 계약과 Python/Node 동등성 / AT-104

작업: T051 | 요구: REQ-051 | 계층: CANONICAL_MIGRATION | 상태: NOT_RUN

**Given:** 구버전 해시 원고와 검수본

**When:** R1 전환 수행

**Then:** 원본 이력 보존·재해시·재검수 후 새 승인

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-105 · JSON Schema 조건·의미 검증·API 계약 일치 / AT-105

작업: T052 | 요구: REQ-052 | 계층: CONTRACT | 상태: NOT_RUN

**Given:** 미갱신 metric value=null 정상예제

**When:** API validation 실행

**Then:** 허용됨

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-106 · JSON Schema 조건·의미 검증·API 계약 일치 / AT-106

작업: T052 | 요구: REQ-052 | 계층: CONTRACT | 상태: NOT_RUN

**Given:** 미갱신 value=0과 다른 envelope payload

**When:** API validation 실행

**Then:** 4xx와 필드 오류 반환

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-107 · JSON Schema 조건·의미 검증·API 계약 일치 / AT-107

작업: T052 | 요구: REQ-052 | 계층: SEMANTIC_UNIT | 상태: NOT_RUN

**Given:** 검증보다 빠른 만료 및 역전 관측 구간

**When:** 의미 validator 실행

**Then:** 고유 오류코드로 거절

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-108 · JSON Schema 조건·의미 검증·API 계약 일치 / AT-108

작업: T052 | 요구: REQ-052 | 계층: API_INTEGRATION | 상태: NOT_RUN

**Given:** 전체 원본 및 OpenAPI 타입

**When:** 양방향 정상/비정상 요청 시험

**Then:** 동일한 데이터 범위와 오류 계약 유지

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-109 · PostgreSQL 연결 무결성과 실제 RLS·동시성 / AT-109

작업: T053 | 요구: REQ-053 | 계층: POSTGRES_RLS | 상태: NOT_RUN

**Given:** 테넌트2개·블로그3개·허용목록 공유 자료

**When:** 비owner 앱 역할로 read/write

**Then:** 허용된 범위만 접근 가능

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-110 · PostgreSQL 연결 무결성과 실제 RLS·동시성 / AT-110

작업: T053 | 요구: REQ-053 | 계층: POSTGRES_INTEGRITY | 상태: NOT_RUN

**Given:** 같은 블로그의 원고A/B·각 revision/review

**When:** A export에 B review 연결

**Then:** FK 또는 제약으로 거절

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-111 · PostgreSQL 연결 무결성과 실제 RLS·동시성 / AT-111

작업: T053 | 요구: REQ-053 | 계층: POSTGRES_CONCURRENCY | 상태: NOT_RUN

**Given:** 같은 논리 metric와 idem키 동시 트랜잭션

**When:** 경쟁 insert/commit

**Then:** current 하나·외부작업 한 번만 보장

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-112 · PostgreSQL 연결 무결성과 실제 RLS·동시성 / AT-112

작업: T053 | 요구: REQ-053 | 계층: POSTGRES_MIGRATION | 상태: NOT_RUN

**Given:** 기존 null/오연결/중복행 샘플

**When:** 전환·중단·rollback 실행

**Then:** 오염행 격리·무단연결 없음·이력 보존

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-113 · 기획 전 원고 생성·상태 전이·API 멱등성 / AT-113

작업: T054 | 요구: REQ-054 | 계층: API_INTEGRATION | 상태: NOT_RUN

**Given:** 기획 전 opportunity

**When:** ArticleCreate 요청

**Then:** 초기 brief null 원고 생성 성공

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-114 · 기획 전 원고 생성·상태 전이·API 멱등성 / AT-114

작업: T054 | 요구: REQ-054 | 계층: API_INTEGRATION | 상태: NOT_RUN

**Given:** brief없는 초기원고

**When:** 집필 상태로 직접 변경

**Then:** 거절하고 요구 입력 반환

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-115 · 기획 전 원고 생성·상태 전이·API 멱등성 / AT-115

작업: T054 | 요구: REQ-054 | 계층: HTTP_CONCURRENCY | 상태: NOT_RUN

**Given:** 동일 actor/key/body 요청2개

**When:** 동시에 처리

**Then:** 같은 resource/response로 복귀

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-116 · 기획 전 원고 생성·상태 전이·API 멱등성 / AT-116

작업: T054 | 요구: REQ-054 | 계층: HTTP_IDEMPOTENCY | 상태: NOT_RUN

**Given:** 동일키 다른body 또는 다른actor

**When:** 재요청

**Then:** 전자는 conflict·후자는 격리

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-117 · 서버 검수본 결속·만료·다운로드 직전 재검증 / AT-117

작업: T055 | 요구: REQ-055 | 계층: AUTH_INTEGRATION | 상태: NOT_RUN

**Given:** 클라이언트 issuer=review_service PASS JSON

**When:** 출고 API에 제출

**Then:** 클라이언트 판정 무시·서버저장 검수 조회

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-118 · 서버 검수본 결속·만료·다운로드 직전 재검증 / AT-118

작업: T055 | 요구: REQ-055 | 계층: SEMANTIC_INTEGRATION | 상태: NOT_RUN

**Given:** 승인후 내용/정책/이미지권리 변경

**When:** 다운로드 요청

**Then:** 해시불일치로 재검수

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-119 · 서버 검수본 결속·만료·다운로드 직전 재검증 / AT-119

작업: T055 | 요구: REQ-055 | 계층: TIME_BOUNDARY | 상태: NOT_RUN

**Given:** 검수/근거 expiry 바로전·정각·이후

**When:** 고정시계로 출고 가드

**Then:** 정각부터 차단

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-120 · 서버 검수본 결속·만료·다운로드 직전 재검증 / AT-120

작업: T055 | 요구: REQ-055 | 계층: PROVENANCE_INTEGRATION | 상태: NOT_RUN

**Given:** REPLAY source만 있는 bundle

**When:** 상위label만LIVE변경

**Then:** LIVE출고 거절

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-121 · 기획 후보 비교·발행 준비시간·관측 편향 처리 / AT-121

작업: T056 | 요구: REQ-056 | 계층: EDITORIAL_UNIT | 상태: NOT_RUN

**Given:** 동일 사건 기획3개·유효 근거

**When:** 다음 행동 결정

**Then:** 차별점·자료준비·시점 근거가 함께 기록

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-122 · 기획 후보 비교·발행 준비시간·관측 편향 처리 / AT-122

작업: T056 | 요구: REQ-056 | 계층: OBSERVATION_UNIT | 상태: NOT_RUN

**Given:** 반올림 조회구간·동일조건 재관측

**When:** 속도계산

**Then:** 구간값과 불확실성 유지

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-123 · 기획 후보 비교·발행 준비시간·관측 편향 처리 / AT-123

작업: T056 | 요구: REQ-056 | 계층: OBSERVATION_UNIT | 상태: NOT_RUN

**Given:** 다른account/surface 또는 reset

**When:** 속도계산

**Then:** 비교불가/reset 상태로 종료

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-124 · 기획 후보 비교·발행 준비시간·관측 편향 처리 / AT-124

작업: T056 | 요구: REQ-056 | 계층: SCHEDULER_INTEGRATION | 상태: NOT_RUN

**Given:** 게시가능시간 미입력·대기열가득·예산부족

**When:** 새원고 결정

**Then:** 보류/refresh·추가유료집필 없음

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-125 · 기획·원고 분리 블라인드 벤치마크 / AT-125

작업: T057 | 요구: REQ-057 | 계층: HUMAN_BLIND | 상태: NOT_RUN

**Given:** 30개 실제 독립소재 평가셋

**When:** 기획과원고를 각각익명평가

**Then:** 2명 실제 평가·분모·실패포함

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-126 · 기획·원고 분리 블라인드 벤치마크 / AT-126

작업: T057 | 요구: REQ-057 | 계층: HUMAN_EDIT_TIME | 상태: NOT_RUN

**Given:** 완성원고와원문·중요결함기준

**When:** 독자가 복사준비까지수정

**Then:** 수정시간·수정내용·잔여오류보고

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-127 · 기획·원고 분리 블라인드 벤치마크 / AT-127

작업: T057 | 요구: REQ-057 | 계층: HUMAN_FAITHFULNESS | 상태: NOT_RUN

**Given:** 실제경험없는소재·애매한공식자료

**When:** 원고전수근거대조

**Then:** 체험조작과확정과장0 또는출시보류

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-128 · 기획·원고 분리 블라인드 벤치마크 / AT-128

작업: T057 | 요구: REQ-057 | 계층: EVAL_REPRODUCIBILITY | 상태: NOT_RUN

**Given:** B0/B1/B2 동일자료와예산

**When:** 분리한기간으로비교

**Then:** 사후샘플교체와평가정보누출없음

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-129 · 렌더 의미 보존·자산 파일·전송 완성도 / AT-129

작업: T058 | 요구: REQ-058 | 계층: RENDER_INTEGRATION | 상태: NOT_RUN

**Given:** 모든블록/캡션/표/링크fixture

**When:** HTML/text출력비교

**Then:** 의미있는값누락없이보존

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-130 · 렌더 의미 보존·자산 파일·전송 완성도 / AT-130

작업: T058 | 요구: REQ-058 | 계층: FILESYSTEM_NEGATIVE | 상태: NOT_RUN

**Given:** symlink/상위경로/대소문자충돌/tamper

**When:** 파일검증

**Then:** 모두차단

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-131 · 렌더 의미 보존·자산 파일·전송 완성도 / AT-131

작업: T058 | 요구: REQ-058 | 계층: ASSET_INTEGRATION | 상태: NOT_RUN

**Given:** 필수이미지누락/손상/라이선스만료

**When:** 전송준비상태요청

**Then:** HANDOFF_READY불가

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-132 · 렌더 의미 보존·자산 파일·전송 완성도 / AT-132

작업: T058 | 요구: REQ-058 | 계층: MANUAL_EDITOR | 상태: NOT_RUN

**Given:** 실제파일과내용·네이버/티스토리입력

**When:** 사용자가비공개에디터에서확인

**Then:** 텍스트/표/사진/출처/모바일 일치증거

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-133 · 미갱신 통계·정정 이력·미래정보 누출 없는 학습 / AT-133

작업: T059 | 요구: REQ-059 | 계층: METRIC_INTEGRATION | 상태: NOT_RUN

**Given:** 관측/미갱신/누락/정정된동일metric

**When:** 반복import

**Then:** status보존·current하나

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-134 · 미갱신 통계·정정 이력·미래정보 누출 없는 학습 / AT-134

작업: T059 | 요구: REQ-059 | 계층: LEARNING_ASOF | 상태: NOT_RUN

**Given:** 후속성과가붙은과거후보

**When:** 의사결정시점dataset구성

**Then:** 미래열제외

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-135 · 미갱신 통계·정정 이력·미래정보 누출 없는 학습 / AT-135

작업: T059 | 요구: REQ-059 | 계층: AGGREGATION | 상태: NOT_RUN

**Given:** 월말발행·다음달누적·여러플랫폼

**When:** 월PV보고서

**Then:** 주력블로그그달발생분만합산

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-136 · 미갱신 통계·정정 이력·미래정보 누출 없는 학습 / AT-136

작업: T059 | 요구: REQ-059 | 계층: LEARNING_NEGATIVE | 상태: NOT_RUN

**Given:** 거절후보·정정로그·실패원고

**When:** 성과보고서생성

**Then:** 선택편향과분모를보존

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-137 · R1 회귀시험·실제 운영 단계별 출시 판정 / AT-137

작업: T060 | 요구: REQ-060 | 계층: OFFLINE_RELEASE | 상태: NOT_RUN

**Given:** 의도적으로한회귀실패삽입

**When:** release검사실행

**Then:** nonzero exit·성공으로포장하지않음

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-138 · R1 회귀시험·실제 운영 단계별 출시 판정 / AT-138

작업: T060 | 요구: REQ-060 | 계층: RELEASE_EVIDENCE | 상태: NOT_RUN

**Given:** 실제DB/사람/에디터로그없음

**When:** R2/R4 판정

**Then:** NOT_RUN 또는BLOCKED

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-139 · R1 회귀시험·실제 운영 단계별 출시 판정 / AT-139

작업: T060 | 요구: REQ-060 | 계층: RESILIENCE | 상태: NOT_RUN

**Given:** 시간초과·예산소진·수정상한도달

**When:** 여러블로그실행

**Then:** 문제작업만격리·무한반복없음

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.

## AT-140 · R1 회귀시험·실제 운영 단계별 출시 판정 / AT-140

작업: T060 | 요구: REQ-060 | 계층: SCOPE_RELEASE | 상태: NOT_RUN

**Given:** 수동게시범위와새자동게시route

**When:** 범위검사

**Then:** 자동게시기능도입차단

**증거:** 실제 입력 범위·실행명령·시간·버전·반환값·오류·실행자와 원본 로그. 정적검사로 통합시험을 대체하지 않는다.
