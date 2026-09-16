# 28. R1 결정적 계약과 참조 구현

## 실행 가능한 것
`reference_core/canonical.py`와 `.mjs`: 불변 JSON canonical bytes와 hash.
`reference_core/contracts.py`: JSON Schema+날짜/관측/주장/블로그범위/검수문맥의 결정적 검사, 기획작업 분기, 관측 증가구간.
`reference_core/render.py`: ArticleIR의 HTML/TXT 생성, escape, 파일명/해시/사이즈/심볼릭 링크 검사.
`tools/run_r1_checks.py`: 합성 반례, 정상 예제, 실제 Python/Node 벡터, 파일 출력, 정적 SQL 대응검사.

이 코드는 source reader·LLM·API auth·DB·전송UI를 포함한 전체 앱이 아니다. deterministic PASS는 의미상 사실성/권리 진위/사람 문체평가를 대체하지 않는다. GateReport의 issuer 필드는 스키마 라벨일 뿐 인증 증명서가 아니다. 서버는 실제 검수 서비스가 작성한 레코드만 가져와야 한다.

## Canonical 규칙
HFBO-NFC-INT-1은 RFC8785와 다른 제품 제한 계약이다.[S17] 문자열·키 NFC, Unicode scalar만 허용, Python codepoint와 동일한 순서로 JS 키 정렬, 정수값 ±(2^53−1), 소수 금지(해당 필드는 decimal string). 원본 자료/JSON 통계를 덮어쓰지 않는다. 1.0은1로, -0.0은0으로 정규화한다. NFC 키 충돌과 JSON 중복키는 덮어쓰지 않고 거부한다. 브라우저는 임의 객체를 canonical인 것처럼 서버 승인에 제출하지 못한다.

## 원고와 검수 결속
profile.blog_id = article.blog_id = brief.blog_id = gate.blog_id.
article.brief_id = brief.id; brief.opportunity_id = opportunity.id.
gate.revision_id = article.revision_id; gate.target_content_hash = actual hash.
gate.evidence_bundle_hash = 서버에서 현재 입력으로 계산한 문맥 hash.
자료 접근 범위/권리/버전/프로필이 바뀌면 본문이 같아도 재검수한다.

## 타입·날짜 검사
AgentEnvelope produced는 null 불가, payload_type과 실제 스키마 일치. NOT_UPDATED/NOT_AVAILABLE의 수치값은 null이다. 실제 관측0은0이다. referral_ratio는 ratio 단위의0~1이고 30%를 넣으려면 mapper에서0.3으로 바꿔 원본30을 별도 보존한다. verified_at<valid_until, period_start<period_end, interval.lower<=upper. 날짜 순서는 JSON Schema가 아닌 의미 검사에서 시행한다.[S18]

## 출고 검사 단계
1. 신뢰된 서버 저장소에서 문맥 로드.
2. 타입·참조·출처범위·지원상태·만료·프로필·원고 hash 확인.
3. 실제 의미 검수와 고위험 사람 검수 완료 확인.
4. 실제 파일 생성·권리·MIME/해시/크기·렌더 보존 검사.
5. 전체 manifest 생성 후 공개-only 다운로드.
6. 클릭 시점에 1~4의 신선도/권리·버전 변화 재검사.

reference assess_handoff는 2단계의 결정적 검사 참조다. 이 함수의 allowed=True만으로4단계 파일 검사가 완료됐다거나 HANDOFF_READY의 서비스 상태가 만들어졌다고 주장하지 않는다. 실제 자동 상태 전이는 서버 transaction과 검수 job에서 구현한다.

## URL/파일 보호의 범위
오프라인 fetch_guard는 호스트 allowlist·IP 사례·redirect마다 재검사할 규칙을 제공한다. 실제 DNS rebinding은 선택한 IP 고정과 egress proxy/네트워크 정책에서 추가로 막는다. URL검사 PASS만으로 실제 인터넷 연결의 안전을 보장하지 않는다. TXT/HTML escape는 콘텐츠를 단순 문자열로 보존하며 임의 script/style을 실행하지 않는다. 원본 이미지는 안전하게 디코딩/재인코딩한 뒤 READY를 부여해야 한다.
