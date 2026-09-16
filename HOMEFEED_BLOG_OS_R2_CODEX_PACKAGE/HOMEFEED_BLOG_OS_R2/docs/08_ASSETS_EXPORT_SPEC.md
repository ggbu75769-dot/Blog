# 08. 이미지·완성 원고·수동 게시 패키지 명세

문서 기준: 2026-09-15 · 설계 동결: 4.1.0-r1 · 공개 게시: 사용자 수행


## 자산 Resolver
입력: brief의 visual_need, blog scope, 역할, 실제증거 필요 여부, 공급자·예산.
우선순위: 사용자 소유 파일→범위가 맞는 허가 자산→라이선스 확인 자료→설명용 자체 제작. 이미지 생성 서비스는 선택형이며 모델·가격·조건은 연결 시 probe한다. 사실 증거가 필요한 사진을 생성 이미지로 대체하지 않는다. 검색 이미지의 존재는 재게시 권리를 뜻하지 않는다.

출력: 실제 object_key/file_hash/mime/size/width/height, origin, rights_basis, allowed_blogs, allowed_platforms, attribution_text, expires_at, alt_text, caption, display_role, transformation_log. 저장된 파일의 MIME과 내용이 맞는지 검사하고 SVG는 sanitize 또는 서버에서 래스터화한다. 외부 이미지 URL만 남겨 다운로드 없이 완성 표시하지 않는다.

## ArticleIR와 렌더
표현의 단일 원본은 ArticleIR JSON이다. paragraph/heading/list/table/quote/callout/image block을 지원한다. 모든 block은 안정적인 block_id를 가진다. 각 문장의 claim 연결은 내부 메타이며 공개 문장에 ID를 노출하지 않는다. public_citations는 원작자·문서명·URL로 읽을 수 있게 렌더한다.

이미지 블록은 asset_id를 참조하고 서버가 실제 파일을 찾아야 한다. 표는 headers와 rows 배열이며 임의 HTML을 받지 않는다. 브라우저 HTML을 그대로 신뢰해 렌더하지 않고 allowlist 태그로 생성한다. title은 본문 밖 별도 필드다. category/tags는 제안일 뿐 플랫폼에 자동 설정됐다고 하지 않는다.

## 다운로드 구성
공개 콘텐츠 폴더에는 article.txt, article.md, article.html, assets/가 들어간다. 운영 가이드에는 naver_handoff.md, tistory_handoff.md, owned_handoff.md, asset_order.json, manifest.json을 둔다. private/에는 evidence_index.json, review_report.json, change_log.json을 둔다. ‘공개 본문만’ 다운로드에는 private/이 포함되지 않는다. 전체 ZIP에는 private/가 있다는 것을 명시한다.

글마다 DOCX는 선택 출력이다. 문서 출력 라이브러리는 실제 글의 블록과 이미지를 사용해야 하며 단순 HTML 스크린샷 한 장으로 원고를 대체하지 않는다. 사용자 운영에서는 TXT/HTML/이미지 순서표를 기본 경로로 지원한다.

## 네이버 수동 전송
1. 최종 제목 별도 복사.
2. 본문 text/plain 복사 또는 문단/소제목 묶음별 복사.
3. 실제 파일을 순서대로 삽입하고 caption과 source를 옆 가이드에서 확인.
4. 표/인용/대표이미지는 네이티브 에디터에서 설정할 항목을 안내.
5. 모바일 표시와 제목·출처 누락을 사용자가 확인.
본문에는 ‘이미지 삽입’, TODO, 내부 검수 메모를 넣지 않는다. 이미지 위치는 별도 가이드가 block_id와 주변 문장을 가리킨다. 로컬 HTML 전체 복사로 네이버 ONE의 서식·이미지가 완벽히 보존된다고 보장할 근거는 없다.[S09]

## 티스토리·자체 블로그 전송
단순 HTML과 Markdown을 제공한다. 로컬 이미지 경로는 플랫폼에서 자동 업로드되지 않으므로 먼저 파일 업로드 후 생긴 URL을 사용자가 media-map에 넣으면 해당 버전의 HTML을 다시 생성할 수 있다. media-map을 적용한 새 export는 URL·누락을 다시 검수한다. 아직 URL이 없으면 HTML을 ‘플랫폼 게시완료’가 아니라 ‘원고 전송용’으로 표시한다. HTML 모드와 스킨별 표시가 다를 수 있어 실제 에디터 시험이 필요하다.[S16]

## Manifest
article_id, revision_id, blog_id, content_hash, review_bundle_hash, policy_version, generated_at, valid_until, allowed_use, files[{path,hash,mime,size,visibility}], assets, public_sources를 저장한다. 디렉터리 탈출(../), 절대경로, 서명된 민감 URL, 외부 script를 차단한다. 제목만 바꿔도 새로운 content_hash가 필요하다. valid_until은 최소 재검토 기한으로 계산한다.

## READY 조건
서버에서 스키마 유효, 내용 비어있지 않음, 필수 답·근거·이미지 있음, rights scope 유효, 고위험 검토 완료, 문체와 제목 약속 검토 완료, orphan claim 없음, 미완성 표식 없음, public/private 분리, 출력 블록 수·텍스트·표·이미지 순서 보존을 확인한다. 원고 내용의 의미 판단은 별도 검수 결과가 필요하다. 스키마 통과만으로 의미 검증 통과가 아니다.

## 만료와 수동 게시
준비 완료 후 사용자가 며칠 뒤 올릴 수 있다. READY 원고의 다운로드 버튼은 현재 valid_until을 확인하고 지나면 재검토 작업을 시작한다. 기존 다운로드 파일까지 회수할 수는 없으므로 생성시각과 재확인 권고시각을 가이드에 넣는다. 앱의 등록된 URL은 USER_RECORDED이며, 실제 원격 확인이 없으면 VERIFIED라고 바꾸지 않는다. 미게시 원고를 PV=0 실패로 학습하지 않는다.


## R1: 출력 보존과 파일 검증
IR의 제목·블록·표 셀·목록·캡션·공개 출처가 TXT/HTML로 보존되는지 비교한다. 외부 HTML은 문자열로 escape하며 무작위 href/src를 그대로 실행하지 않는다. 파일 경로는 상위탈출·절대경로·Windows 예약명·대소문자/NFC 중복·symlink를 차단한다. 파일 해시와 용량이 manifest와 다르면 다운로드하지 않는다. REPLAY 예제를 LIVE 또는 HANDOFF_READY 생산 실적으로 승격하지 않는다. 예제 렌더 성공은 네이버 에디터 붙여넣기 성공이 아니다.


## R2 보완 우선 적용
내용·문체·독자 평가·독자용 출력의 상세는 docs/31~38을 함께 적용한다. 특히 부족한 내용은 문체로 덮지 않고 조사/재기획하며, 최종 본문의 실제 payoff 구절과 review 버전을 연결한다. R1 사실·권리·scope·최신성 gate는 약화하지 않는다. R2 예제는 인간평가·실제 에디터·트렌드 효과가 확인되지 않은 편집 기준용 원고다.
