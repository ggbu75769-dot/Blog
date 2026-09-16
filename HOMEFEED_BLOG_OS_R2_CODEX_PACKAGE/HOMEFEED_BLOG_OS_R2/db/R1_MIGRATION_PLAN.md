# R1 DB 적용 전 필수 점검

이 파일과 reference_schema.sql은 운영 DB에 적용한 migration이 아니다. 실제 Postgres 바이너리가 없는 현재 환경에서는 실행하지 않았다.

1. 백업 및 복구 가능한 disposable 복제 DB 확보.
2. article↔brief↔opportunity, revision parent, export↔review↔revision을 읽기전용으로 대사.
3. 불일치행 격리. 자동 선택으로 관계를 덮어쓰지 않음.
4. allowed_blog_ids·source execution_mode 명시적 backfill. 미확인값은 사용 보류.
5. 복합 unique/FK·scope trigger·idempotency·current metric unique 적용.
6. nonowner/NOBYPASSRLS role에서 tenant A/B, blog A/B, shared context on/off, pool reuse, 원문회수 후 재조회 시험.
7. API 동시key 두 요청, payload변경409, worker lease상실, budget 예약경쟁을 실제 transaction으로 시험.
8. upgrade/rollback/restore 명령과 결과를 저장.

부분 UNIQUE 인덱스는 일반 composite FK의 target으로 사용하지 않는다. 현재 metric 인덱스는 중복current를 막는 용도다. RLS는 서버가 신뢰된 context를 설정할 때의 추가 보호이며 사용자에게 직접 SQL/임의 SET 권한을 제공하면 안 된다. FORCE RLS도 superuser/BYPASSRLS에 적용되지 않는다.[S13]
