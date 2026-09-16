# 19. 운영·장애 대응·인수 운영서

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 운영 모드
REPLAY: 포함된 픽스처와 mock provider만 사용한다. LIVE: 키·권한·소스·가격·예산·프로필이 확인된 연결을 사용한다. SHADOW: 실제 입력으로 기획 판단만 비교하고 신규 원고 출고를 변경하지 않는다. 이 모드는 테스트 도구 설정이지 플랫폼 기능이 아니다. production 환경에서는 REPLAY 데이터를 실제 성과표에 표시하지 않는다.

## 시작 전 체크
실제 저장소·lockfile·DB 대상·테넌트·블로그·소스 권한·secret ref·예산·object storage·clock·서버 TLS를 확인한다. 게시 계정 키는 입력받지 않는다. 등록한 source가 개인 경험 자료를 외부 모델에 전송할 권리를 포함하는지 확인한다. write 가능한 path는 작업 디렉터리와 private bucket으로 한정한다.

## 일일 운영
작업 상태·만료 export·source health·예산 예약·예외 대기시간·원고 수정/정정·보고서 갱신시각을 점검한다. READY 적체는 생산을 멈추는 조건이며 사용자에게 더 빨리 게시하도록 강제하지 않는다. 새 공식 공지나 핵심 원문 변경이 있으면 영향 원고만 재검사한다. 최근 정상 source observation이 없는 블로그는 최신 탐색 완료로 표시하지 않는다.

## 장애별 대응
| 코드 | 증상 | 조치 | 하지 않을 일 |
|---|---|---|---|
| SRC-403 | 접근/권한 문제 | 소스 비활성·권한 점검·허용 대체경로 | 계정/IP 바꿔 재시도 |
| SRC-429 | 쿼터 초과 | reset time까지 보류 | 여러 계정으로 분산 |
| SRC-INCOMPLETE | 빈 셸/자막 없음 | 읽은 범위 표시·대체 원문 | 전편 분석 완료 표시 |
| LLM-SCHEMA | 구조화 출력 실패 | 제한repair·재시도후 예외 | 원문 JSON 그대로 출고 |
| CALL-UNKNOWN | 유료호출 결과 불명 | provider ID 조회·예약 유지·대사 | 즉시 비용 반환·무제한 재호출 |
| REVIEW-STALE | 본문·근거·정책 hash 다름 | 새 검수 | 기존 통과 재사용 |
| ASSET-MISSING | 파일/권리 누락 | 대체 확보·기획 변경 | 프롬프트를 사진으로 간주 |
| METRIC-UNMAPPED | 통계 열/기간 불명 | dry-run 매핑 재확인 | 추정 PV 입력 |
| SCOPE-VIOLATION | 블로그/테넌트 누출 시도 | 작업중단·감사·토큰범위 확인 | 오류 숨기고 결과 반환 |

## 백업·복구
DB와 객체저장소의 일관성을 확보하는 backup manifest를 만든다. 제안 RPO24h/RTO4h는 설계 목표이지 측정 결과가 아니다. 주기적 복구훈련에서 실제 원고·자산·권리·job checkpoint를 되살려 다운로드 파일 hash를 비교한다. job 재개는 lease와 외부 intent 상태를 먼저 대사한다. 백업 복원 후 이미 끝난 유료 호출을 다시 실행하지 않는다.

## 관측 지표
queue wait, stage duration, provider error, unknown calls, retry cost, reserved budget, completed handoffs, stale exports, unsupported claims, orphan claims, fake experience blocks, render parity, manual edit time을 분리한다. LLM 응답시간과 사람 예외대기시간을 같은 처리시간 분모에 섞지 않는다.

## 배포와 복귀
기능별 feature flag를 사용한다. 새 prompt/profile/rank version은 shadow→제한적용→확장한다. 불량 원고가 나오면 생성 중단·영향 export stale 처리·기존 안정 버전 복귀·사용자에게 원고별 정정 필요를 알린다. 외부 게시물 수정·삭제는 사용자가 한다. migration rollback은 사전 restore 검증과 함께 설계하고 운영에서 즉흥적으로 수행하지 않는다.

## 출시 제출물
실제 명령 로그·버전·입력범위·검증 파일·render screenshots·미실행 항목·알려진 제한을 제출한다. ‘모든 테스트 통과’는 어떤 계층을 실행했는지 명시한다. 월100만·홈판1위·자연스러움은 테스트용0원/가짜 데이터로 검증했다고 적지 않는다.


## R1 회귀 실행 명령
`python tools/validate_bundle.py` 다음 `python tools/run_r1_checks.py`를 실행한다. 두 검사의 scope를 구분한다. `reports/R1_REGRESSION.json`의 STATIC_DDL_ONLY는 데이터베이스를 실행한 것이 아니다. DB가 없는 경우 NOT_RUN으로 남기고 네트워크·권한 준비 전 설치를 무한 재시도하지 않는다. 수정은 반드시 문제를 재현하는 사례, 정상 사례, 회귀 사례를 함께 포함한다.
