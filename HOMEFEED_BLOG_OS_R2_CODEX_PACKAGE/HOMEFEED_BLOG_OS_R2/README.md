# HOMEFEED BLOG OS R2 — 원고의 내용과 읽기 품질 개정본

**릴리스 4.2.0-r2 · 2026-09-16 · 공개 게시는 사용자 수행**

R1 전체 설계와 새 편집 명세를 포함한 교체 패키지다. 주력 네이버 블로그 한 개의 월 PV 100만 목표, 네이버·티스토리·자체 블로그용 주제→조사→집필→완성 원고 경로를 유지한다. 쇼츠·커머스가 아니다.

## 먼저 볼 파일
1. `examples/editorial_r2/01_DATALAB/preview.html`: 실제 R1 원고를 내용부터 다시 편집한 예.
2. `examples/editorial_r2/02_GOOGLE_PHOTOS/preview.html`, `03_USBC/preview.html`: 구체적인 독자 질문으로 작성한 두 새 원고.
3. `R2_REVIEW_REPORT_KO.md`: 이번 실제 확인·수정·검증의 범위.
4. `CODEX_START_HERE.md`: 저장소에 적용할 첫 지시문.
5. `docs/31~38`: 내용 기여·집필·평가·출력·작업·검증 기준.

세 샘플은 이 세션에서 직접 집필한 문체 검토용 텍스트다. 실제 자동 파이프라인 실행·독립 사람평가·현재 급상승 주제 검증·에디터 입력·바이럴 성과는 NOT_RUN이다. 표지와 사진이 필요한 최종 홈피드 패키지로 승인된 것이 아니다.

## 핵심 변화
- 원고에 실제로 있는 ‘독자에게 남는 답’을 정확한 문구와 근거로 연결.
- 질문이 틀렸으면 재기획, 내용이 부족하면 조사, 반복이면 삭제/합치기, 문장만 어색하면 부분 편집.
- 제목·첫 화면 기대와 본문 충족을 분리 평가.
- 독자형 출처 표기와 내부 검수 정보를 분리.
- 보안 시험 예제를 tests/adversarial로 격리.
- 판별기·가짜 후기·오타 주입을 목표로 사용하지 않음.

## 문서·코드 관계
기존 ArticleIR 등 스키마는 4.1.0을 유지한다. 새 편집 review는 schemas/r2/editorial_review.schema.json의 `r2.editorial.1` 확장이다. reference_core는 R1 계약 시험, editorial_r2는 새 출력/검토 참조 코드다. 앱·모델 집필 서비스 자체는 아직 구현·실행한 것이 아니다.

기존 작업60/제품시험140에 R2 작업10/제품시험30이 추가된다. 모두 실제 앱에서 실행하기 전에는 NOT_STARTED/NOT_RUN으로 남긴다. 실행한 오프라인 시험은 reports/r2와 reports의 명령 결과를 확인한다. 이 숫자를 원고 품질이나 바이럴 성과로 해석하지 않는다.

## 재현
```
python tools/verify_checksums.py
python -m pip install -r requirements-validation.txt
python tools/validate_bundle.py
python tools/run_r1_checks.py
python -m unittest discover -s tests/r2 -v
python tools/build_r2_previews.py
```
검사 실행은 reports와 일부 fixture를 갱신한다. 패키지 무결성은 압축 해제 직후 먼저 확인한다. 네트워크·모델 비용·게시 계정을 요구하지 않는 참조 검사다.

## 최종 사용자 경험
사용자는 원고와 사진·출처를 먼저 읽는다. 내부 점수와 작업 메모는 펼침 영역에서 확인한다. 자동 준비 가능한 원고와 내용이 부족해 보류한 원고를 구분한다. 조회수 목표를 채우려고 저가치 글을 늘리지 않는다.
