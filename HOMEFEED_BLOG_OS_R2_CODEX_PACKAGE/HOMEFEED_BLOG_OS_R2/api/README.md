# 내부 API 계약

OpenAPI 3.1.0, 43개 operation. 이 파일은 설계이며 실행 중인 서버가 아니다. 네이버·티스토리 제공 API도 아니다.

서버가 인증 문맥에서 tenant_id와 소유 blog를 결속하고 request의 UUID를 검증한다. object schema 통과가 권한 통과가 아니다. Replay 구현도 모든 정상·실패 계약을 적용한다. 일부 모델의 structured-output subset은 full JSONSchema를 지원하지 않으므로 어댑터 변환 뒤 서버 원본 schema 검증을 다시 수행한다. 실제 OpenAPI 런타임 contract 시험은 T002 이후 구현한다.

전역 Error의 details는 민감자료를 담지 않으며 request_id로 운영 로그와 연결한다. SSE와 파일 전송은 별도 실제 통합시험이 필요하다.
