# 05. 조사·근거·경험 데이터 작업명세

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## ResearchPack 산출물
각 기획의 reader_question, proposed_answer, fact_needs, source_registry, claims, conflicts, missing_evidence, asset_needs, independence_groups, inspected_scope를 저장한다. 단순 URL 목록은 완료된 ResearchPack이 아니다. 사실 근거마다 원문에서 어디를 확인했는지 locator와 필요한 짧은 설명이 있어야 한다.

## 주장의 종류
| kind | 의미 | 출고 조건 |
|---|---|---|
| fact | 날짜·수치·기능·발언 등 확인 가능한 주장 | 해당 내용을 지지하는 evidence·검수 시각·적용 범위 |
| analysis | 근거를 연결한 해석 | 기초 claim과 해석이라는 표현, 다른 해석 가능성 |
| recommendation | 제안하는 행동·선택 기준 | 왜 제안하는지 논거, 중요한 조건·한계 |
| hypothetical | 설명용 가정 | 가정임을 공개 본문에 표시, 실제 실적으로 전환 금지 |
| author_experience | 작성자가 한 실제 행동·관찰 | 승인된 경험 record와 기간·대상·사용 범위 |
| common_reasoning | 일반적인 설명·논리 | 사실처럼 보이는 외부 수치·시점이 숨겨져 있지 않은지 검사 |

중요한 사실이 포함된 문장인데 작성자가 claim 연결을 누락하면, 검수기가 최종 본문에서 주장 후보를 다시 추출해 orphan_claim으로 발견해야 한다. writer가 연결한 claim만 검사하는 방식은 충분하지 않다.

## 원문 확인 규칙
검색 스니펫은 후보 탐색용이다. 중요한 최신 주장에는 원문을 읽어야 한다. 원문이 JS 빈 셸·로그인 벽이면 READ_INCOMPLETE다. 같은 문서의 요약본만 확보한 경우 읽은 범위를 그 수준으로 기록한다. 다른 모델의 설명은 원출처가 아니다. source locator는 heading+paragraph, transcript timestamp, document page 등의 실제 제공 범위로 저장한다.

## 최신성
각 claim에는 valid_until과 recheck_policy가 있다. 가격·현재 제공 여부·일정·정책처럼 변동성 있는 주장은 짧은 기한, 역사적 사실은 긴 기한을 둘 수 있다. 기본값은 runtime 설정이며 네이버의 공식 신선도 가중치가 아니다. 정책·이슈가 바뀌는 이벤트가 도착하면 만료일 이전이라도 재검사한다. 내보내기 유효기한은 모든 핵심 claim·asset·opportunity 재검토 기한 중 가장 이른 값이다.

## 상충 출처 처리
권위가 높은 원문이 어떤 사실을 말하는지 확인하고 각 출처의 기준일·범위·대상을 대조한다. 최신 출처라는 이유만으로 자동 우선하지 않는다. 다른 버전·지역일 수 있다. 직접 충돌하는 중요 사실은 보류하거나, 충돌과 범위를 명확히 설명하는 분석형으로 전환한다. 모델 다수결로 진위를 결정하지 않는다.

## 작성자 기억의 격리
AuthorFact는 사용자 승인 시각·scope·공개허용 범위를 가진다. ExperienceRecord에는 owner, 대상·기간·행위·방법·자료 해시가 필요하다. 문체 예시에 나온 여행·구매·자녀·직업은 사실 기록으로 자동 수집하지 않는다. 사용자가 ‘좋아요’라고 한 원고도 그 안의 숫자나 경험을 승인한 것으로 취급하지 않는다. 기억 정정은 연결된 후속 원고까지 전파한다.

## 독창적 기여의 형식
comparison: 같은 조건으로 원문을 대조한 표.
calculation: 입력·단위·공식이 공개된 독립 계산.
interpretation: 확인한 내용과 해석을 구분한 논리.
procedure: 대상 조건·검증 범위가 있는 재현 가능한 절차.
observation: 실제 자료와 방법을 가진 관찰.
새 기여는 하나 이상 필요하지만 표 하나를 자동 생성했다고 통과하지 않는다. 실제 독자 질문을 해결하는지 편집 검수에서 판정한다.

## 자료 재사용과 권리
사실 확인에 읽을 수 있는 자료와 본문에 인용·사진 재게시할 수 있는 자료를 분리한다. 출처 표기는 사용허가를 대신하지 않는다. 원문의 긴 문장을 그대로 붙이는 것이 아니라 자체 설명으로 작성하며 인용은 필요한 짧은 범위에서 권리·맥락을 검토한다. 라이선스 불명 자산은 ready가 아니다. 개인정보는 필요한 최소 범위만 전송·보존한다.

## 실패 출력
research result는 ready=true 한 개로 끝내지 않는다. SUPPORTED / NEEDS_SOURCE / CONFLICTING / INSUFFICIENT_ACCESS / NEEDS_EXPERIENCE를 구분하고, 누락된 주장·필요 자료·공개자료 기반 대안·재시도 가능 여부를 반환한다. 연구 실패는 다른 기획을 중단시키지 않는다.
