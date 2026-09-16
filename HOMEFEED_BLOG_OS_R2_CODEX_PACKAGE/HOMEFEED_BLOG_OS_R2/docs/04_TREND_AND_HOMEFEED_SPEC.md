# 04. 주제 탐지·홈판 연구 작업명세

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 수집 계약
SourceRegistration에는 source_kind, provider, allowed_hosts, can_fetch, can_store, can_send_to_model, can_republish, scope_evidence, checked_at, expires_at, quota_window, quota_limit, retention_policy를 저장한다. 공개 페이지라고 사진·전문·유료 자막을 재게시할 수 있다고 취급하지 않는다. 허가가 불명확하면 메타데이터 수준만 사용하거나 연결을 보류한다.[S04]

## P0 입력 경로
| 경로 | 구현 | 저장·해석 | 실패 대응 |
|---|---|---|---|
| Naver Blog Search | GET /v1/search/blog.json | query/sort/start/display/실제 응답 항목, total은 검색응답 규모이지 PV가 아님 | 403은 설정 확인, 429는 Retry-After·쿼터, 5xx 제한 재시도 |
| Naver Datalab | POST /v1/datalab/search | 요청 전체 fingerprint와 일·주·월 상대값 | 다른 요청의 상대값을 직접 병합하지 않음 |
| 공식 웹 원문 | 검증된 HTTP reader+정제기 | URL·원문 hash·조회시각·권한·필요 구간 | 원문 차단/빈 셸은 READ_INCOMPLETE |
| 사용자 자료 | JSON/CSV/텍스트/이미지 원본 업로드 | 동의·source_kind·수집시각·관측 범위 | 파일과 계정 자료가 없으면 빈 상태 유지 |
| 홈피드 관측 | 허가된 공급자 또는 사용자 관측 import | 표면·로그인·세션·카드·시각 | 일반 웹 검색으로 대체한 뒤 홈피드라고 라벨 금지 |

공식 검색 API의 display는 최대100, start는 최대1000이다. Datalab은 최대5개 주제어 묶음, 묶음별 최대20개 검색어를 받으며 시간단위는 일·주·월이다. 구현 시 공급자 문서를 다시 점검하고 계약시험으로 확인한다.[S05][S06]

## P1 선택형 경로
YouTube/SNS는 현재 연결된 공급자의 메타데이터·자막·본문 읽기 범위를 probe한 후 활성화한다. 영상 대본만 읽었으면 대본 분석으로 표시한다. 자막으로만 화면·복장·편집·그래프 수치를 확인했다고 하지 않는다. Instagram/TikTok 없는 환경에서도 공식 공지와 검색을 이용한 제작은 계속하지만 coverage에 해당 공급자가 빠졌다고 기록한다. 네이버 공식 글과 기술 발표는 URL·발표일·해석 범위를 가진 연구 레지스트리로 관리한다.

## 탐색 실행 계획
승인된 분야마다 기본 질문 묶음과 엔티티를 만든다. 검색어는 core·adjacent·event·followup 그룹으로 버전 관리한다. 회차당 가벼운 후보 상한50, 중복 제거 후 상세 비교10, 근거 조사3, 완성 상한2를 초기 예산 설정으로 둔다. 쿼터가 더 낮으면 실행량을 줄이며 새 계정을 만들어 우회하지 않는다. 숫자는 품질·비용 제어용 가설이다.

## 사건 정규화
occurred_at, published_at, modified_at, first_seen_at, observed_at, source_data_updated_at를 별개로 저장한다. 시간이 불명이면 null과 이유를 넣는다. 단순 수정으로 published_at을 현재시각으로 바꾸지 않는다. 날짜만 있는 원문에는 시각을 임의로 부여하지 않고 precision=date를 저장한다. 모든 내부 시각은 timezone-aware UTC, 사용자 표시는 Asia/Seoul이다.

## 홈피드 관측의 편향
surface는 HOMEFEED, NAVER_SEARCH, BLOG_APP_FEED, MOBILE_REFERRAL_UNKNOWN, CREATOR_SEARCH_TREND, OTHER로 분리한다. HOMEFEED 관측은 로그인 여부·관측자 익명 키·세션·표시순서·기기를 보존한다. 같은 관측자가 같은 카드에 재방문한 경우 독립 관측으로 세지 않는다. ‘관측 안 됨’은 ‘전체 홈판 미노출’이 아니다.[S01]

비교군은 같은 분야·비슷한 공개 시기·비슷한 형식의 검색 결과를 구성하되 노출된 글과 다른 모집단이라는 한계를 명시한다. 확인 안 된 비교 글을 ‘실패작’으로 라벨링하지 않는다. 높은 최소조회수 필터로 평범한 글을 제거하지 않는다.

## 관심 신호와 사실 근거의 분리
10개 글이 같은 발표문을 인용하면 관심 신호는 여러 개지만 독립 사실 근거는 하나의 계열이다. independence_group을 보존한다. 원문 불명 자료의 많음으로 사실의 신뢰도를 올리지 않는다. 인기 영상도 경쟁자 유지율·개별 수익이 없으면 null이다.

## 속도·포화도
정확한 반복 관측이 있을 때 v=(value2-value1)/(t2-t1)로 관측 속도를 계산한다. 음수 수정값·비교 불가능한 필터·반올림 수치에는 exact_rate를 만들지 않는다. 1.2만 등 표시는 interval과 display_precision을 보존한다. Datalab은 동일 query_fingerprint 안에서만 이전 구간과 비교하고 0으로 나누지 않는다.

포화도는 검색 상위 결과 중 같은 질문과 같은 답을 반복한 비율에 대한 표본 평가다. 전국 글 수나 경쟁 강도의 절대값이 아니다. 관측 크기와 시점을 함께 출력한다. 실제 사건의 유효기한을 정확히 예측한다고 주장하지 않는다.

## 관심 우선순위 초기식
rank=100×(0.25 demand+0.15 momentum+0.20 audience_fit+0.20 answer_gap+0.10 readiness+0.10 visual_clarity). 모든 값은0~1, 실제 근거가 없으면 해당 항은0이고 coverage에 누락을 기록한다. 알려진 항만으로 분모를 축소해 높은 점수를 만들지 않는다. 수요자료 없는 기획은 rank와 별개로 exploration/preview만 가능하다. 이 점수는 ‘편집 우선순위’이며 홈판 노출 확률이 아니다. 수식은 실험으로 바꿀 수 있지만 사실·권리 하드게이트는 점수로 상쇄할 수 없다.

## 변경 반영
공식 소스 변경은 이전 해시와 비교하여 연결된 claim·원고·내보내기에 REVALIDATION_REQUIRED를 전파한다. 원문에 들어 있는 프롬프트나 다운로드 명령은 실행 지시가 아니다. 지워진 자료는 접근 범위와 보존 권리 안에서만 증거를 보유한다.


## R1: 비교 가능한 급상승만 채택
같은 source/entity/surface/filter/observer/unit의 시간차 관측만 속도로 계산한다. 반올림 표시는 상하한을 유지하며 증가량/시간도 구간으로 계산한다. 수치 감소는 음의 관심이 아니라 원본 수정·리셋 가능성을 먼저 분리한다. 자료가 없으면0이 아니라 부족이며, 관심 증거가 없는 기획을 높은 자기점수만으로 WRITE로 보내지 않는다. 공식 일정만 확인된 기획은 PREPARE_ONLY에서 실제 공개 전 결과를 단정하지 않는다. 구체적인 기획 비교와 평가 설계는 docs/26·27 참조.
