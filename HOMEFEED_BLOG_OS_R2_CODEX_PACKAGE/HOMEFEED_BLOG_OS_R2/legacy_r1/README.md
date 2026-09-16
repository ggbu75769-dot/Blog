# HOMEFEED BLOG OS — R1 개정 개발 패키지

**4.1.0-r1 · 기준일 2026-09-15 · 공개 게시 = 사용자 수행**

기존 4.0.0-final.1 최종 패키지의 계약·코드·문서를 감사하고 수정한 전체 교체본이다. Commerce/Reels/Shorts나 자동 게시 시스템이 아니다. 주제 발견 → 내용 기획 → 조사 → 블로그별 자연스러운 집필 → 재검수 → 실제 자산과 수동 게시용 완성 원고까지를 구현한다. 목표는 주력 네이버 블로그 **한 개의 달력 월 조회수 100만**이며 아직 효과를 실증하지 않았다.

## 먼저 읽기

- 검토자: `R1_AUDIT_REPORT_KO.md`, `HOMEFEED_BLOG_OS_R1_DESIGN_REVIEW_KO.docx`.
- Codex: `CODEX_START_HERE.md` → `docs/00_SCOPE_AND_DECISIONS.md` → `docs/25_R1_AUDIT_FINDINGS.md` → `docs/26_EDITORIAL_DECISION_ENGINE_R1.md` → `docs/16_WORK_PLAN.md`.
- 한 파일 상세본: `HOMEFEED_BLOG_OS_R1_FULL_DESIGN_KO.md`. 원본은 docs와 machine-readable 계약이다.
- 기존 구현이 있으면 `docs/29_MIGRATION_AND_CODEX_R1.md`, `db/R1_MIGRATION_PLAN.md`를 먼저 보고 사용자 변경·기존 migration을 보존한다.

## 바뀐 핵심

기존 70개 문서 검사는 통과했지만 추가 반례에서 17개 계약·검증 공백을 확인했다. 이를 수정하고 실제 Python/Node 정규화 비교, 값·scope·시간·파일·출처 계보 회귀시험을 추가했다. 데이터베이스는 **정적 연결 검사만** 수행했으며 실제 PostgreSQL 적용·RLS·동시성 시험은 남아 있다.

기획은 관심 신호만으로 바로 집필하지 않고 같은 사건의 후보를 비교해 새 답·첫 화면·자료 준비·사용자의 게시 가능 시점까지 판단한다. 원고 품질은 기획 평가와 분리하고, 실제 두 평가자의 블라인드 평가·수정시간 측정으로 검증한다. 이 사람 평가는 아직 실행하지 않았다.

## 구성

| 위치 | 내용 |
|---|---|
| `docs/00~30` | 기존 설계 전체 수정본 + 감사·편집 결정·집필 벤치마크·실행 계약·전환·출시 게이트 |
| `contracts/` | 60개 요구, 60개 작업, 140개 예정 인수시험, 24개 설계 평가 시나리오, 18개 출처의 확인 범위 |
| `schemas/` | 30개 도메인 타입과 조건부 검증·예제 |
| `api/openapi.yaml` | 내부 업무 API 43개 operation. 네이버 제공 API가 아님 |
| `db/` | 35개 테이블의 미적용 참조 DDL 및 전환 계획 |
| `prompts/` | 공통 계약 + 9개 역할, 기획·문체·재검수 R1 규칙 |
| `reference_core/` | 실행 가능한 정규화·계약·판단·렌더 참조 함수. 제품 app이 아님 |
| `examples/r1/` | 합성 REPLAY 자료와 정규화 벡터·부정 입력 렌더 결과 |
| `tools/`, `reports/` | 재현 가능한 검사와 실제 실행 기록 |

## 실제 검증 범위

문서·스키마·추적성 검사: **73 PASS / 0 FAIL**.
추가 회귀검사: **112 PASS / 0 FAIL**. 여기에는 정적 DDL 검사가 포함된다. 둘은 일부 범위가 겹치므로 독립적인 제품 기능 185개를 검증했다는 뜻이 아니다.

제품 개발 작업 60개는 NOT_STARTED, 제품 인수시험 140개는 NOT_RUN이다. 제공된 참조 함수와 실행 검사 결과를 실제 DB·앱·LLM 집필·사람평가·편집기·홈판 검증으로 바꿔 표시하지 않는다.

## 재현 방법

Python 3.11+와 Node.js 18+의 호환 환경을 준비한다. 실제 제공 검사에는 Python 3.13.5 및 Node 22.16.0을 사용했다. 지원 버전 전체를 시험한 것은 아니다. Python 의존 버전은 `requirements-validation.txt`를 참조한다.

```bash
# 원본 압축 해제 직후 무결성부터 확인한다.
python tools/verify_checksums.py
python -m pip install -r requirements-validation.txt
python tools/validate_bundle.py
python tools/run_r1_checks.py
```

재검사는 reports와 예제 렌더 파일을 갱신하므로, 이후 전달본 checksum과 달라지는 것은 정상이다. checksum 검사는 변경 전 전달본을 대상으로 한다. 실패·SKIP·NOT_RUN을 PASS로 합산하지 않는다.

## 문서 우선순위와 호환성

사용자의 확정 범위가 최상위다. 도메인 필드는 schemas, 상태는 contracts/states, HTTP는 OpenAPI, 작업 순서는 tasks/task_order가 상세 원본이다. 충돌하면 원인과 결정 기록을 남기고 연결된 계약을 함께 고친다. R1의 HFBO-NFC-INT-1은 제한된 자체 정규화 계약이며 RFC8785 구현이 아니다. 기존 해시는 재검수 없이 새 해시로 승인 승계하지 않는다.

## 최초 입력 / 하지 않는 일

블로그 분야·URL(또는 임시 프로필), 문체 참고, 사용할 수 있는 원문·사진·경험, 허용 데이터/모델 연결, 비용 한도, 사용자가 글을 옮길 수 있는 대략적인 시간대가 필요하다. 없으면 REPLAY 개발을 먼저 한다. 게시 비밀번호·자동 게시 권한은 요구하지 않는다. 신규 결제·운영 DB변경·자동배포·비공개 계정작업을 임의 실행하지 않는다.

핵심 완료 기준은 그럴듯한 글 생성이 아니라 **선택 이유가 있는 기획 → 실제 근거 → 독자의 질문에 대한 새 답 → 자연스러운 원고 → 실제 자산 → 안전한 복사 준비**가 연결되는 것이다.
