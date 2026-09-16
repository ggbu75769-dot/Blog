# 20. 운영 입력·연결 준비 명세

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 한 번 필요한 사용자 입력
실제 블로그 이름·URL·주력 여부, 승인할 분야와 독자, 기존 문체 자료 또는 샘플 선택, 공개 허용 작성자 사실, 사용할 경험/사진, 월 예산과 시간대가 필요하다. 비밀번호나 게시 쿠키는 받지 않는다. 입력이 없으면 개발은 REPLAY로 계속하지만 LIVE 제작 가동을 완료했다고 표시하지 않는다.

## 연결별 준비표
| 연결 | 초기 필수성 | 필요한 입력 | live 확인 |
|---|---|---|---|
| Naver Search | P0 실연결 대상 | Client ID/Secret, 사용 scope·quota | 적법한 요청1회와 실제 응답 저장 |
| Naver Datalab | P0 실연결 대상 | 활성화·같은 앱 자격·쿼터 | date 구간 응답·요청 fingerprint 확인 |
| 공식 웹 reader | P0 필수 | allowlist와 권한 근거 | 원문·빈 셸·redirect 실패 시험 |
| 텍스트 모델 | P0 필수 | provider key, 모델, 요금표, 데이터처리 조건 | 구조화출력과 실제 비용기록 |
| 이미지 공급자 | 선택 | 모델/라이선스/가격 | 실제 파일·권리·캡션 |
| 사용자 이미지 업로드 | P0 필수 | 소유·권리·사용범위 | quarantine→검수→asset |
| YouTube/SNS | 선택 | 제공 가능한 API/공급자 권한 | 메타/자막/영상 범위 개별 확인 |
| 홈피드 관측 | 선택 | 허가된 공급자 또는 사용자 관측 | surface/session/time 정확성 |
| Creator Advisor·블로그통계 | P0 import 필수 | 사용자 보고서 파일 | 열·분모·기간 매핑 |
| Naver/Tistory 계정 write | 제외 | 필요 없음 | 구현하지 않음 |

모델명과 요금은 기준일 이후 바뀔 수 있으므로 문서에 허구의 고정값을 두지 않는다. 키 없이 실행 가능한 문서 검증과 고정 입력 시험을 먼저 제공한다. 공급자 연결을 확인하기 전 ‘무료/무제한/100% 자동’이라고 제품에 표시하지 않는다.

## 설정 변수
contracts/defaults.json이 제안 기본값이다. secrets는 .env.example의 이름만 안내하고 값은 넣지 않는다. 유료 호출은 monthly_budget_minor가 null이면 시작하지 않는다. Blog URL 없는 샘플 프로필은 demo=true이며 실제 성과에 포함하지 않는다. 활성 blog 수와 일 생산 상한은 운영자가 변경하되 중앙 예산을 넘을 수 없다.

## 호환성 매트릭스
export targets는 naver_manual, tistory_manual, owned_manual이다. 네이버는 소제목·본문·표·인용·이미지·캡션·출처별 수동 전송 시험을 기록한다. 자체 블로그도 CMS와 theme별로 결과가 다를 수 있다. 로컬 preview test만으로 platform_verified를 만들지 않는다. 브라우저 clipboard 실패 시 기본 텍스트 복사를 제공한다.
