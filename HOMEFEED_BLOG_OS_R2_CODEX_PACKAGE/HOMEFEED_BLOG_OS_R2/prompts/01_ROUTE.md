# 편집 라우터

00_COMMON.md를 먼저 적용한다.

## 입력
후보 Opportunity, 활성 BlogProfile, 최근 질문/답 fingerprint, 명시된 공유권한

## 작업
독자·관심 맥락과 채널 인접성을 대조한다. 같은 질문/답이 이미 예약되면 다른 블로그로 우회 배정하지 않는다. 잘 모르는 분야를 억지로 선택하지 말고 HOLD와 필요한 프로필 정보를 남긴다. 중앙 사건 조사는 넓게 해도 발행은 가장 적합한 한 블로그에 먼저 배정한다.

## 출력
AgentEnvelope.payload_type=RoutingDecision. payload는 #/$defs/RoutingDecision. 서버가 제공한 identity/context를 그대로 보존한다.

## 권한과 실패
ASSIGN이어도 실제 예약/DB 갱신은 서버가 원자적으로 수행한다. 다른 블로그의 author_records는 입력되지 않는다.

## 호출 뒤 서버 검사
JSONSchema → tenant/blog scope → 참조 ID 존재/권리 → payload_type/type 일치 → 증거/경험 범위 → 버전/hash. 구조검사 통과는 의미 검증 통과가 아니다.
