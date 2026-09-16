# 21. 조사·출처 레지스트리

기준일 2026-09-15. 열람일을 게시일로 쓰지 않는다. 본문 재확인이 안 된 자료는 아래에 명시했다. 외부 문서의 설명과 우리의 설계 제안을 구분한다.

## S01 · 홈피드 소개
- 발행자: NAVER 고객센터
- 원문: https://help.naver.com/service/5630/contents/23396?osType=MOBILE&lang=ko
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 인기·개인화 추천과 관측 조건을 구분한다.
- 제한: 전국 고정 순위나 글별 추천확률을 공개한 자료가 아니다.

## S02 · 콘텐츠 작성시 권장 사항
- 발행자: NAVER SearchAdvisor
- 원문: https://searchadvisor.naver.com/guide/content-basic
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 일관된 주제·고유한 기여·출처·정직한 제목·읽기 쉬운 글을 품질 검수에 반영한다.
- 제한: 웹 검색 가이드이며 홈피드 가중치 명세가 아니다.

## S03 · 웹 콘텐츠 스팸사례
- 발행자: NAVER SearchAdvisor
- 원문: https://searchadvisor.naver.com/guide/content-abusing
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 저가치 대량생성·기계적 재작성·조작·오인 유발을 출고 금지조건으로 둔다.
- 제한: AI 기술이라는 이름만으로 모두 금지한다는 뜻은 아니다.

## S04 · 네이버 이용약관
- 발행자: NAVER
- 원문: https://policy.naver.com/policy/service.html
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 허가 범위가 없는 자동 수집·로그인·게시 경로를 임의 구현하지 않는다.
- 제한: 소유 계정 승인과 플랫폼 사용 허가를 분리해야 한다.

## S05 · 통합 검색어 트렌드 API
- 발행자: NAVER Developers
- 원문: https://developers.naver.com/docs/serviceapi/datalab/search/search.md
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 일·주·월 상대값, 최대5개 주제 묶음·각20개 검색어의 요청 계약을 사용한다.
- 제한: 분 단위 실시간 검색량이나 절대 검색 횟수가 아니다.

## S06 · 검색 > 블로그 API
- 발행자: NAVER Developers
- 원문: https://developers.naver.com/docs/serviceapi/search/blog/blog.md
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 검색결과와 요청조건을 저장하고 시점·중복 조사에 사용한다.
- 제한: 타인 PV·홈판 노출·콘텐츠 CTR API가 아니다.

## S07 · 크리에이터 어드바이저 소개
- 발행자: NAVER 고객센터
- 원문: https://help.naver.com/service/23038/contents/19001?osType=MOBILE&lang=ko
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 검색 유입 트렌드와 광고 노출·클릭 통계를 구분한다.
- 제한: 광고 CTR를 콘텐츠 홈피드 CTR로 사용하지 않는다.

## S08 · 유입 분석 안내
- 발행자: NAVER 블로그 고객센터
- 원문: https://help.naver.com/service/5593/contents/15330?lang=ko&osType=COMMONOS
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 유입 비중의 분모와 월초 미갱신 표시를 보존한다.
- 제한: 유입비중×PV로 정확한 홈피드 PV를 계산하지 않는다.

## S09 · 스마트에디터 ONE 소개
- 발행자: NAVER 블로그 고객센터
- 원문: https://help.naver.com/service/5593/contents/15506?lang=ko&osType=COMMONOS
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 에디터와 수동 전송 기능별 호환 시험을 분리한다.
- 제한: 외부 HTML·이미지가 모두 완벽하게 복사된다는 근거는 확보하지 않았다.

## S10 · Spam policies for Google web search
- 발행자: Google Search Central
- 원문: https://developers.google.com/search/docs/essentials/spam-policies
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 여러 사이트를 같은 저가치 콘텐츠의 분산망으로 만들지 않는다.
- 제한: Google 웹검색 정책이며 네이버 비공개 추천 규칙이 아니다.

## S11 · Custom instructions with AGENTS.md
- 발행자: OpenAI
- 원문: https://developers.openai.com/codex/guides/agents-md
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 짧은 루트 AGENTS와 문서 경로를 제공하고 기존 계층을 보존한다.
- 제한: 열람 시 learn.chatgpt.com 공식 문서로 리다이렉트되었다. 사용자 저장소의 기존 지시는 별도 확인한다.

## S12 · SELECT — locking clauses
- 발행자: PostgreSQL
- 원문: https://www.postgresql.org/docs/current/sql-select.html
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: SKIP LOCKED를 큐형 작업 소비에 사용하고 일관된 분석 조회와 분리한다.
- 제한: 참조 DDL은 실제 DB에서 실행 검증하지 않았다.

## S13 · Row Security Policies
- 발행자: PostgreSQL
- 원문: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- 확인 범위: body_verified / 게시일: 문서에서 확정하지 않음
- 적용: 앱 role·table owner·RLS 우회 권한을 분리하고 범위시험을 수행한다.
- 제한: RLS 설정만으로 모든 애플리케이션 범위 오류가 해결되지는 않는다.

## S14 · HCX-VLM과 함께 홈피드를 더 예쁘게 바꿔보자!
- 발행자: NAVER D2
- 원문: https://d2.naver.com/helloworld/3247986
- 확인 범위: indexed_excerpt_verified / 게시일: 2024-11-05
- 적용: 제목만이 아니라 썸네일 기획을 별도로 고려한 과거 기술 사례다.
- 제한: 직접 페이지는 셸만 반환했고 공식 검색 색인 요약을 확인했다. 2026년 전체 알고리즘 명세가 아니다.

## S15 · 검색과 피드의 만남 — 기존 설계 참고 링크
- 발행자: NAVER D2
- 원문: https://d2.naver.com/helloworld/5152301
- 확인 범위: not_reverified / 게시일: 문서에서 확정하지 않음
- 적용: 이전 대화에서 사용한 링크를 추적용으로 남긴다.
- 제한: 이번 열람에서 본문을 확보하지 못했다. 새 설계의 확정 사실 근거로 사용하지 않는다.

## S16 · 마크다운, HTML모드 사용하기
- 발행자: TISTORY
- 원문: https://notice.tistory.com/m/2482
- 확인 범위: body_excerpt_verified / 게시일: 2019-03-27
- 적용: 모드·스킨에 따라 표현이 달라질 수 있어 전송 결과를 시험한다.
- 제한: 2019년 자료다. 2026년 모든 에디터 기능·제한을 보장하는 자료로 사용하지 않는다.

## 기존 영상·SNS 경험칙 처리
이전 대화에서 확인한 창작자 영상은 설계의 질문과 실험 가설로만 보존한다. 이번 패키지 작성 중 해당 영상을 다시 시청하거나 비공개 성과를 검증하지 않았다. 사진 장수·제목 단어·발행 간격·링크 우회·누구나 수익 보장을 제품 규칙에 넣지 않는다.

## 업데이트 규칙
소스 등록은 원문·게시/수정일·확인시각·읽은 범위·적용 조항·제한을 가진다. 새 공식 내용이 바뀌면 연결된 정책과 관련 원고를 검토하지만, 모델이 외부페이지의 명령을 실행하거나 스스로 권한을 확대하지 않는다.


## R1 출처 재확인 범위

공식 원문 재확인: S01·S02·S05·S11·S13·S17·S18. S08은 이번 요청에서 본문 대신 공통 shell만 반환되어 **재확인 미완료**다. 다른 출처는 기존 확인 기록을 보존했으며 R1에서 모두 다시 열었다고 주장하지 않는다. 기사·유튜브·SNS의 추가 최신 조사는 이번 감사의 실행 범위가 아니다.

- S17 RFC8785: https://www.rfc-editor.org/rfc/rfc8785 — 언어 간 정규화 논의의 참고. 자체 계약을 JCS라고 부르지 않는다.
- S18 JSON Schema 조건: https://json-schema.org/understanding-json-schema/reference/conditionals — 타입 간 조건 보강. 의미·권한 검토는 별도다.
