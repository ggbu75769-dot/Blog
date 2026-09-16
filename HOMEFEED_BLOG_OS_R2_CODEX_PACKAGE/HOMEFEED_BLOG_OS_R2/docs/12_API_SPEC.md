# 12. 내부 API 작업명세서

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 범위
api/openapi.yaml은 **우리 서비스 내부 API**다. 네이버·티스토리에서 제공하는 API 명세가 아니다. 외부 게시 endpoint는 존재하지 않는다. publication_receipt는 사용자가 게시한 사실과 URL을 우리 DB에 기록하는 기능이다.

## 공통 규칙
API prefix /v1, JSON UTF-8, 인증은 서버 세션 또는 검증된 Bearer token이며 tenant_id는 인증 문맥에서 결정한다. 요청 body의 tenant_id를 믿지 않는다. 공개 signup·과금·외부 발행은 초기 비범위다. local dev만 허용된 테스트 로그인, 외부 배포 시 실제 인증과 TLS가 필요하다.

쓰기 요청은 Idempotency-Key를 받는다. key 범위는 tenant+actor+method+path이며 body_hash가 달라지면409다. 동일 결과는 설정된 retention 안에서 재사용한다. 문서 수정은 If-Match 또는 expected_revision_id를 받으며 충돌하면409와 현재 revision을 반환한다. 목록은 cursor 기반으로 정렬 키와 ID를 함께 사용한다.

## 응답
동기생성201, 기존조회200, 작업시작202{job_id,status}, 검증실패422, 권한403, 범위 밖 객체404, 중복/버전충돌409, 쿼터429, 공급자 일시실패503을 사용한다. 오류 body는 code,message,request_id,retryable,details를 가진다. source secret, 다른 tenant 객체의 존재 여부는 노출하지 않는다.

## 엔드포인트 묶음
- /blogs: 등록·조회·프로필 버전·활성화·일시정지.
- /sources: 등록·probe·허용된 수집 실행.
- /observations/imports: 홈피드·검색·수동 관측의 형식 검증과 저장.
- /opportunities: 조회·배정·브리프 생성 요청.
- /articles: 작업생성·버전조회·수정·재검토 요청.
- /assets: 파일 staging 완료·권리 입력·검증. 파일은 검증 전 QUARANTINED.
- /jobs: 상태·이벤트·정해진 재시도·취소.
- /exports: 출력요청·다운로드 링크·신선도 재검사.
- /publication-receipts: 사용자 게시 URL·시각·실제 수정본 기록.
- /metric-imports: dry-run 매핑·commit·원본 오류 보기.
- /reports: 블로그별 실제 성과·예산·품질.
- /exceptions: 해결자료 제출·대안 선택. 하드게이트 우회용 force_pass는 없다.
- /runtime/config: 예산·자동 제작 일정·상한. 변경은 감사와 version을 가진다.

## 외부연결 probe
read/configured/permission_missing/provider_unavailable/supported_formats/quota/pricing_version/checked_at을 구분한다. 미설정은 현재 데이터0건이 아니다. API 스키마를 검사한 것을 실제 수집 성공으로 표시하지 않는다. probe는 가능한 최소 비용 호출로 하며 결제되는 호출은 승인된 예산이 있어야 한다.

## 파일 업로드
업로드 준비→private staging URL→완료 통지→서버 파일형식·크기·악성콘텐츠·권리 검사→READY/REJECTED. 사용자가 object_key를 보냈다고 tenant scope를 신뢰하지 않는다. 이미지 bytes에 대한 MIME·해시 확인이 필요하다. 사용 가능 전까지 writer 입력·export에서 접근하지 못한다.

## Export
POST /articles/{article_id}/exports는 해당 revision의 모든 gate와 신선도를 다시 확인한 뒤 렌더 job을 만든다. body에는 target_platform과 revision_id만 받으며 arbitrary_html·publish 옵션은 거부한다. GET /exports/{export_id}/download는 사용자 선택된 공개-only/전체 패키지에 맞는 짧은 유효기간 링크를 반환한다. 만료하면409 REVALIDATION_REQUIRED 또는 재검토202를 제공한다.

## 수동 게시 기록
platform, url, posted_at, article_revision_id, final_content_hash(optional), user_note를 저장한다. URL 호스트를 target blog와 대조하되 소유 여부·공개 확인을 자동으로 단정하지 않는다. status=USER_RECORDED가 기본이다. 사용자가 현장에서 편집한 실제 본문을 제공하면 새 final_revision을 만들고 검수를 분리한다. 미게시 원고는 성과 실패의 분모에 넣지 않는다.

## SSE
GET /jobs/{id}/events는 id, event, data를 전송한다. 동일 tenant/blog 권한 검사, Last-Event-ID 재개, heartbeat, 만료 연결을 처리한다. 이벤트 유실이 의심되면 GET job에서 authoritative 상태를 다시 읽는다. 이벤트 페이로드에는 원문 전문·키를 넣지 않는다.


## R1: 변경된 요청·응답 계약
ArticleCreate는 blog_id/opportunity_id를 필수로 받고 brief_id는 생략/NULL 가능하다. 서버가 초기 상태를 결정한다. SourceCreate는 명시적인 allowed_blog_ids를 받되 모두 현재 actor의 허용 범위 안인지 검사한다. JSON body의 권리 주장만으로 AVAILABLE을 확정하지 않는다. 원문 execution_mode는 reader/import 작업의 실제 모드에서 부여하며 writer가 덮어쓰지 못한다. 수정가능 리소스 GET/PATCH 응답은 strong ETag를 제공한다. If-Match와 expected_version이 함께 있으면 같은 버전을 가리켜야 한다. API 사본 도메인 타입과 schemas/domain 사이의 완전 대응을 회귀검사한다.
