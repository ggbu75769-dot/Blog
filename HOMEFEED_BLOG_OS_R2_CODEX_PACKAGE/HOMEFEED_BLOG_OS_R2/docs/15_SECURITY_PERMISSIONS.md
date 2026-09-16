# 15. 보안·권한·개인정보·권리 명세

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 위협 모델
외부 페이지의 prompt injection, 불명 파일, SSRF, XSS, tenant/blog 데이터 누출, 가짜 GateReport, 유료호출 폭주, 공급자 키 노출, 무단 원문·사진 재게시, 게시 기록 위조, 데이터 삭제 누락을 다룬다. 공개 게시와 로그인 자동화를 제거함으로써 플랫폼 계정 비밀번호·쿠키는 수집할 필요가 없다.

## 권한
Owner는 설정·예산·편집프로필 승인, Editor는 원고수정·자료제출·수동게시기록, Viewer는 허용된 원고조회, Worker는 해당 job에 필요한 최소 읽기/쓰기만 가진다. 모델은 DB 직접접근·gate 통과 발급·예산변경·외부 게시 권한이 없다.

PostgreSQL RLS를 사용할 때 table owner나 BYPASSRLS 권한이 우회할 수 있다는 점을 고려한다. 앱·worker 역할을 owner와 분리하고 필요한 테이블은 FORCE ROW LEVEL SECURITY, tenant context 부재 시 deny한다. RLS는 blog scope 검사를 자동으로 대신하지 않으므로 앱·복합FK도 확인한다.[S13]

## SSRF·다운로드
URL scheme은 https 기본, 허용된 http 예외만 등록한다. loopback/private/link-local/metadata 주소와 credentials-in-url을 차단한다. DNS resolve와 redirect마다 재검사한다. 허용 host도 공격자가 바꿀 수 있는 리다이렉트를 포함하므로 목적지를 다시 검증한다. 응답 bytes·timeout·압축해제 크기를 제한한다. downloaded file path를 사용자가 직접 정하지 못한다.

## HTML·파일
렌더러는 ArticleIR에서 안전한 태그만 만든다. script/iframe/form/event handler/javascript: URL을 차단한다. preview는 앱 세션과 격리된 origin 또는 sandbox·CSP를 사용한다. 파일은 내용 검사 전 quarantine, 원본과 파생물 해시를 저장한다. ZIP entry는 상대경로만 허용하고 ..·절대경로·심볼릭링크를 금지한다. 개인 근거 파일은 공개-only export에서 제외한다.

## 비밀키
소스·모델 key는 secret manager 또는 배포환경 안전 저장소 참조만 DB에 저장한다. 프런트엔드 bundle·prompt·로그·export에 값을 넣지 않는다. 로컬 .env는 gitignore, .env.example에는 변수명만 둔다. 새 공급자는 읽기·저장·모델전송·라이선스 범위를 확인해야 한다.

## 자료 권리와 삭제
read 허가는 재게시 허가가 아니다. 출처 표기는 권리 문제의 자동 해결이 아니다. 권리 만료·삭제 요청은 원본 저장소·캐시·검색인덱스·아직 사용 중인 export를 추적해 반영한다. 이미 사용자가 다운로드·게시한 파일을 회수했다고 주장하지 않으며 정정/삭제 안내를 제공한다. 동의 기록을 사용자 프로필 변경과 분리해 감사한다.

## 감사
actor, action, target, prior_hash, new_hash, reason, request_id, timestamp를 남긴다. 값이 너무 큰 원문과 키는 기록하지 않는다. 강제 통과 버튼은 만들지 않는다. 예외 해결은 새 근거 제출→재검토 순서다. 고위험 주제의 사람 확인은 누가 무엇을 확인했는지 남긴다.


## R1: server context와 RLS 한계
app.tenant_id/app.blog_ids/app.actor_subject는 인증 뒤 서버가 트랜잭션 범위에 설정한다. 클라이언트/LLM에게 SQL 실행권이나 이를 변경할 통로를 주지 않는다. pooled connection을 재사용할 때 이전 문맥이 남지 않는 시험을 추가한다. RLS는 arbitrary SQL 실행/서버 자체 탈취를 해결하는 장치가 아니다. 원문 fetch는 allowlist·DNS·각 redirect·IP 주소와 최종 egress 정책까지 확인해야 하며 오프라인 URL 검사만으로 실제 SSRF 방어 완료라 표시하지 않는다.
