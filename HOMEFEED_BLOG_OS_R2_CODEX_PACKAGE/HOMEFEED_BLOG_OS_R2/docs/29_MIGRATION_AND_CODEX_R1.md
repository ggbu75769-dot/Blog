# 29. 기존 final.1에서 R1으로 적용하는 작업

## 저장소 보존
기존 AGENTS와 git diff부터 읽는다. 사용자 작업을 reset/stash/drop하지 않는다. R1은 이전 문서의 단순 부록이 아니라 schemas/API/DDL/작업순서를 함께 갱신한 패키지다. 기존 문서와 새 schema를 섞으면 재현된 결함이 남을 수 있다.

## 적용 순서
1. 현재 문서와 앱의 버전/경로/구현 범위를 기록한다.
2. schema_version4.1.0과 canonicalization 이름을 도입한다.
3. 기존 hash로 승인된 원고는 새 규칙의 자동 PASS를 상속하지 않는다. 원본 보존 후 새 revision/검수로 이행한다.
4. SourceRegistration/SourceSnapshot의 allowed_blog_ids와 snapshot.execution_mode를 backfill한다. 범위·출처 모드를 모르면 빈 범위/REVIEW_REQUIRED로 별도 보류한다. 과거 샘플을 LIVE로 추측하지 않는다.
5. ArticleCreate의 optional brief와 articles.opportunity_id를 연결한다. 기존 article은 실제 brief→opportunity 관계로 채우고 실패행은 quarantine한다.
6. 다른 article을 가리키는 revision/parent/review 연결을 조회해 격리한 뒤 복합FK를 추가한다. 임의로 가장 최신 revision을 골라 수정하지 않는다.
7. current metric 중복은 원본 보고서 revision과 갱신시점으로 결정하고 불명확하면 검토한다.
8. 동기 idempotency 저장소를 추가하고 동시 요청/결과불명/재시작을 시험한다.
9. scoped RLS/claim-evidence 트리거를 disposable DB에서 적용·rollback·역할별 시험한다.
10. 원고·파일·패키지·문체·전송을 검증한 뒤 최소 블로그에서 실제 자료를 연결한다.

## 되돌리기
서버 바이너리를 이전 버전으로 되돌려도 새 hash나 공개 원고 기록을 지우지 않는다. 기능 플래그로 신규생성을 멈추고 마지막으로 검증된 read path를 유지한다. schema의 되돌릴 수 없는 데이터변경은 별도 백업과 restore rehearsal을 요구한다. 기존 고객/게시글이 있다면 정정·다운로드 재검수 통지까지 고려한다.

## Codex 수행 방식
한 번의 작업은 재현 사례→최소 수정→단위/계약→관련 통합→문서 동기화 순서로 수행한다. 각 완료 보고에는 실제 명령, exit code, 고친 결함 ID, 미실행 시험을 적는다. 앱키가 없으면 REPLAY를 진행하되 LIVE 스위치를 켜서 시연하지 않는다. README의 검사 개수보다 실제 결과 JSON을 원본으로 사용한다.
