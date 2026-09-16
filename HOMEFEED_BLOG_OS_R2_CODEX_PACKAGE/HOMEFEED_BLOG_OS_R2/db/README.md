# PostgreSQL 참조 DDL

34개 테이블의 신규 DB용 참조 구조다. 본 패키지 제작에서는 PostgreSQL에 적용하지 않았다. 문서 검증기는 테이블/참조/정책의 텍스트 구조만 검사한다. SQL 파싱·migration 적용·rollback·RLS 우회·동시성은 T004/T044/T049에서 실제 DB로 수행한다.

앱 역할은 table owner/superuser/BYPASSRLS가 아니어야 한다. 인증된 tenant/blog context를 SET LOCAL로 설정하고 connection pool 반환 전에 transaction을 끝낸다. shared scope는 인증된 중앙 worker/서비스 단계에만 부여하며 외부 요청에서 임의로 받지 않는다. evidence_items.allowed_blog_ids, asset 권리, claim 의미는 추가 repository 검증이 필요하다.

budget UI의 minor 단위는 외부 호출 가격의 micro 단위로 정확히 변환한다. null limit는 무제한이 아니라 paid disabled다. actual 비용이 견적을 초과하면 원장에 실제 비용을 별도로 기록하고 예산 초과 예외로 처리해야 한다. overrun_micro는 한도 초과를 드러내며 실제 비용 기록을 막지 않는다. 한도 제어는 신규 예약의 원자적 승인 조건으로 수행하고, 초과 시 새 요청을 중단한다. 이 동시성·정산 로직은 T034에서 검증한다.

JSONB는 임의 payload 저장 허가가 아니다. API/worker에서 고정 JSONSchema·ID scope·version을 먼저 검증한다. rollback은 객체 보존 요구에 맞는 migration down 또는 backup restore로 검증한다.
