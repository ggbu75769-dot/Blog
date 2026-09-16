# 13. 자동화 워크플로·상태·복구 명세

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 두 종류의 상태를 나눈다
job 상태와 article readiness를 같은 열로 관리하지 않는다. job은 QUEUED/RUNNING/WAITING/COMPLETED/FAILED/CANCELLED다. 원고는 DISCOVERED→ASSIGNED→RESEARCHING→BRIEF_READY→DRAFTED→EDITING→VERIFYING→ASSET_READY→RENDERING→HANDOFF_READY로 진행한다. 필요 시 NEEDS_SOURCE/NEEDS_ASSET/NEEDS_EXPERIENCE/NEEDS_REVIEW/REVALIDATION_REQUIRED/DEFERRED/REJECTED로 이동한다. 출고물 이후의 USER_RECORDED는 별도 receipt이며 원고 제작 상태가 아니다.

## 상태 전이 권한
오케스트레이터만 단계를 진행하고, review worker만 gate 결과를 쓰며, export worker는 검증된 revision만 렌더한다. 사용자 수정은 revision을 생성하지만 HANDOFF_READY로 바로 바꿀 수 없다. 모델 출력의 status 문자열은 제안일 뿐 실제 상태를 바꾸지 않는다.

## 정상 흐름
스케줄 tick→활성 블로그·예산·대기열 확인→허용 소스 수집→중복 사건 정리→기회 평가→blog reservation→근거 조사→브리프 확정→집필→문체 편집→최종본문 재검수→자산 완성→출력 검증→HANDOFF_READY. tick은 cadence_key로 중복 제거하고 같은 작업이 실행 중이면 이어보기만 한다.

## 중단·재개
사용자 stop은 새 작업만 막고 진행 중 외부호출은 provider cancel 지원이 있을 때 취소한다. 취소 불가능한 결과는 받아 비용과 상태를 정리하되 후속 집필을 시작하지 않는다. restart는 마지막으로 commit된 checkpoint에서 재개한다. output_hash가 있으면 같은 단계의 모델을 무조건 재호출하지 않는다.

## Fencing과 exactly-once의 한계
lease 만료 후 다른 worker가 같은 job을 잡으면 fencing_token이 증가한다. 이전 worker는 DB 결과 commit 권한을 잃는다. 외부 유료호출이 timeout이면 provider_request_id로 상태를 확인한다. 공급자가 조회·idempotency를 지원하지 않으면 CALL_OUTCOME_UNKNOWN으로 두고 비용 예약을 유지하며 자동 반복 결제를 피한다. 내부 중복 작업 억제는 구현할 수 있지만 모든 외부 공급자의 exactly-once 과금을 보장할 수는 없다.

## 재시도 정책
일시적 HTTP 오류는 최대3회, exponential backoff+jitter, Retry-After 우선. 정책403·로그인·권리 미확인·quota exhausted는 즉시 재시도하지 않는다. LLM JSON repair1회, 문체수정2회, 근거보강2회는 초기 설정이다. 재시도마다 attempt는 늘지만 원고 개수로 세지 않는다. 반복 실패하면 예외와 대안을 기록한다.

## 예산 원장
전체 tenant 월 예산과 blog 일 예산을 고정 순서로 잠근다. spent+reserved+estimate가 한도 이하일 때만 reservation을 생성한다. 실제 결과 후 estimate→actual로 대사하고 차이를 반환 또는 추가 승인 상태로 처리한다. 오류라고 무조건0원으로 만들지 않는다. 정산 불명 예약은 별도 표시하며 사용자가 원장 증거를 확인한 뒤 조정한다.

## 적체·신선도
블로그별 대기 원고 상한을 넘으면 신규 집필을 멈추고 재검수·정정·빈 자산 해결을 우선한다. 실제 게시가 며칠 늦어졌다고 계속 새 원고로 밀어내지 않는다. 각 원고는 valid_until이 지나면 download 순간에도 recheck된다. 관심 신호가 오래되어도 역사적 설명으로 유효한 경우 자동 폐기 대신 재기획안을 제안한다.

## 장애 주입 목록
worker kill 전/후 외부호출, DB commit 후 SSE 유실, 중복 tick, stale lease 응답, budget 동시예약, object storage put 성공 후 DB 실패, source 304/변경/삭제, locale 날짜 오류, 블로그 일시정지 중 완료 응답을 시험한다. 각각 기대 결과를 AT 문서에서 추적한다.


## R1: 반복 개선의 종료
결함이 남아 있으면 고치되 무제한 self-improve 호출은 하지 않는다. stage별 한도와 원고 전체 비용/repair 한도를 동시에 검사한다. 한도 도달은 성공이 아니라 HUMAN_REVIEW/보류다. 작업 lease가 바뀌면 늦은 worker는 결과를 commit할 수 없다. 동일 Idempotency-Key의 결과가 불명이면 대사하며 다시 비용을 발생시키지 않는다. 공개 게시의 결과를 추측하는 경로는 없다.
