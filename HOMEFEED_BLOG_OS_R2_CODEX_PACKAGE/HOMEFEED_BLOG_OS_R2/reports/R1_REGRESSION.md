# R1 회귀검사 실행 결과

PASS 112 / FAIL 0
실행: 2026-09-15T20:29:46.904203+00:00

코드가 실제 실행된 범위와 정적 DDL 검사를 layer로 구분한다. 제품 통합·사람 평가·조회수 검증은 아니다.

| 검사 | 범위 | 결과 |
|---|---|---|
| B01 missing metric is not zero | OFFLINE_REFERENCE | PASS |
| B02 unknown article type rejected | OFFLINE_REFERENCE | PASS |
| B03 discriminator binds payload | OFFLINE_REFERENCE | PASS |
| B04 evidence reversed interval rejected | OFFLINE_REFERENCE | PASS |
| B05 traversal filename rejected | OFFLINE_REFERENCE | PASS |
| B06 executable citation URL rejected | OFFLINE_REFERENCE | PASS |
| B07 unsupported first-person record rejected | OFFLINE_REFERENCE | PASS |
| B08 reversed observation interval rejected | OFFLINE_REFERENCE | PASS |
| Writer cannot forge gate field | OFFLINE_REFERENCE | PASS |
| Produced response cannot be null | OFFLINE_REFERENCE | PASS |
| Correct discriminator accepted | OFFLINE_REFERENCE | PASS |
| Blog assignment cannot be null | OFFLINE_REFERENCE | PASS |
| PASS cannot contain critical finding | OFFLINE_REFERENCE | PASS |
| Required human review cannot be missing | OFFLINE_REFERENCE | PASS |
| Title source hostname credentials rejected | OFFLINE_REFERENCE | PASS |
| Duplicate block id rejected | OFFLINE_REFERENCE | PASS |
| Orphan citation rejected | OFFLINE_REFERENCE | PASS |
| Visual required cannot be text-only | OFFLINE_REFERENCE | PASS |
| Unknown canonical card id rejected | OFFLINE_REFERENCE | PASS |
| Source scope cannot be empty | OFFLINE_REFERENCE | PASS |
| Unupdated null metric is accepted | OFFLINE_REFERENCE | PASS |
| Observed actual zero is accepted | OFFLINE_REFERENCE | PASS |
| Negative pageviews rejected | OFFLINE_REFERENCE | PASS |
| Percent is not normalized ratio | OFFLINE_REFERENCE | PASS |
| Metric period cannot be reversed | OFFLINE_REFERENCE | PASS |
| Valid reference bundle passes only as REPLAY | OFFLINE_REFERENCE | PASS |
| Replay cannot be labelled LIVE | OFFLINE_REFERENCE | PASS |
| Expired at exact boundary | OFFLINE_REFERENCE | PASS |
| Article wording changed after review | OFFLINE_REFERENCE | PASS |
| Evidence summary changed after review | OFFLINE_REFERENCE | PASS |
| Source permission change invalidates review | OFFLINE_REFERENCE | PASS |
| New review still cannot allow denied transfer | OFFLINE_REFERENCE | PASS |
| Other blog evidence denied | OFFLINE_REFERENCE | PASS |
| Other blog raw snapshot denied | OFFLINE_REFERENCE | PASS |
| Other blog source registration denied | OFFLINE_REFERENCE | PASS |
| Other tenant evidence denied | OFFLINE_REFERENCE | PASS |
| Wrong revision report denied | OFFLINE_REFERENCE | PASS |
| Wrong blog profile denied | OFFLINE_REFERENCE | PASS |
| Profile version changed denied | OFFLINE_REFERENCE | PASS |
| Brief from another opportunity denied | OFFLINE_REFERENCE | PASS |
| Orphan factual claim denied | OFFLINE_REFERENCE | PASS |
| Conflict not treated as supported | OFFLINE_REFERENCE | PASS |
| Unavailable source not silently substituted | OFFLINE_REFERENCE | PASS |
| Future review cannot grant readiness | OFFLINE_REFERENCE | PASS |
| Paused blog cannot keep producing | OFFLINE_REFERENCE | PASS |
| Expired source permission blocks download | OFFLINE_REFERENCE | PASS |
| Metadata-only source not body evidence | OFFLINE_REFERENCE | PASS |
| Future source snapshot denied | OFFLINE_REFERENCE | PASS |
| Relabelled run cannot promote replay snapshot | OFFLINE_REFERENCE | PASS |
| Python/JS korean_nfc | CROSS_LANGUAGE_EXECUTED | PASS |
| Python/JS integer_number | CROSS_LANGUAGE_EXECUTED | PASS |
| Python/JS unicode_codepoint_keys | CROSS_LANGUAGE_EXECUTED | PASS |
| Python/JS escapes | CROSS_LANGUAGE_EXECUTED | PASS |
| Python/JS nested | CROSS_LANGUAGE_EXECUTED | PASS |
| Python/JS max_integer | CROSS_LANGUAGE_EXECUTED | PASS |
| NFC key collision rejected | OFFLINE_REFERENCE | PASS |
| Nonfinite value rejected | OFFLINE_REFERENCE | PASS |
| Unsafe integer rejected | OFFLINE_REFERENCE | PASS |
| Fraction requires decimal string | OFFLINE_REFERENCE | PASS |
| Unpaired surrogate rejected | OFFLINE_REFERENCE | PASS |
| Duplicate raw JSON key rejected | OFFLINE_REFERENCE | PASS |
| JSON infinity rejected | OFFLINE_REFERENCE | PASS |
| Fetch guard redirect to localhost | OFFLINE_REFERENCE | PASS |
| Fetch guard metadata IP | OFFLINE_REFERENCE | PASS |
| Fetch guard host suffix attack | OFFLINE_REFERENCE | PASS |
| Fetch guard mixed DNS answers | OFFLINE_REFERENCE | PASS |
| Fetch guard IPv6 loopback | OFFLINE_REFERENCE | PASS |
| Public allowlisted fetch plan accepted | OFFLINE_REFERENCE | PASS |
| Portable path rejects '../a' | OFFLINE_REFERENCE | PASS |
| Portable path rejects '/tmp/a' | OFFLINE_REFERENCE | PASS |
| Portable path rejects 'a\\b' | OFFLINE_REFERENCE | PASS |
| Portable path rejects 'a//b' | OFFLINE_REFERENCE | PASS |
| Portable path rejects 'CON.txt' | OFFLINE_REFERENCE | PASS |
| Portable path rejects 'a/../b' | OFFLINE_REFERENCE | PASS |
| Portable path rejects 'A:drive' | OFFLINE_REFERENCE | PASS |
| Portable path rejects 'name.' | OFFLINE_REFERENCE | PASS |
| Portable path rejects 'a\x00b' | OFFLINE_REFERENCE | PASS |
| Portable filename reserved 'a?.png' | OFFLINE_REFERENCE | PASS |
| Portable filename reserved 'a*.txt' | OFFLINE_REFERENCE | PASS |
| Portable filename reserved 'a|b' | OFFLINE_REFERENCE | PASS |
| Portable filename reserved 'x#y.png' | OFFLINE_REFERENCE | PASS |
| Portable filename reserved 'a%2Fb' | OFFLINE_REFERENCE | PASS |
| Portable filename reserved 'a\x7fb' | OFFLINE_REFERENCE | PASS |
| Portable filename reserved 'a<b' | OFFLINE_REFERENCE | PASS |
| Reference render conservation and escaping | LOCAL_FILE_EXECUTED | PASS |
| Image without resolved file mapping rejected | OFFLINE_REFERENCE | PASS |
| Unequal table columns rejected | OFFLINE_REFERENCE | PASS |
| Post-render file corruption detected | LOCAL_FILE_EXECUTED | PASS |
| Symlink file is not exported | LOCAL_FILE_EXECUTED | PASS |
| Rounded velocity remains an interval | OFFLINE_REFERENCE | PASS |
| Different observer sessions not a trend | OFFLINE_REFERENCE | PASS |
| Counter reset not negative momentum | OFFLINE_REFERENCE | PASS |
| Unknown observations not zero momentum | OFFLINE_REFERENCE | PASS |
| Planner ready candidate | OFFLINE_REFERENCE | PASS |
| Planner no demand evidence | OFFLINE_REFERENCE | PASS |
| Planner scheduled not happened | OFFLINE_REFERENCE | PASS |
| Planner manual backlog full | OFFLINE_REFERENCE | PASS |
| Planner no paid budget | OFFLINE_REFERENCE | PASS |
| Planner user cannot post in time | OFFLINE_REFERENCE | PASS |
| Planner global repair budget exhausted | OFFLINE_REFERENCE | PASS |
| API/schema parity and pre-brief create | STATIC_CONTRACT | PASS |
| Composite FK target declarations | STATIC_DDL_ONLY | PASS |
| B11 parent same article | STATIC_DDL_ONLY | PASS |
| B12 export exact article and revision | STATIC_DDL_ONLY | PASS |
| B13 export exact reviewed revision | STATIC_DDL_ONLY | PASS |
| B15 opportunity before brief | STATIC_DDL_ONLY | PASS |
| B16 synchronous idempotency | STATIC_DDL_ONLY | PASS |
| B17 one current metric | STATIC_DDL_ONLY | PASS |
| B09/B10 scoped RLS sources | STATIC_DDL_ONLY | PASS |
| B09/B10 scoped RLS source_snapshots | STATIC_DDL_ONLY | PASS |
| B09/B10 scoped RLS evidence_items | STATIC_DDL_ONLY | PASS |
| RLS enabled for synchronous idempotency | STATIC_DDL_ONLY | PASS |

## 미실행
- PostgreSQL parse/migrations/RLS/transactions/concurrency
- production HTTP auth and signed download integration
- live source/model full pipeline
- semantic factuality and image-rights human review
- human naturalness and ready-to-post time study
- Naver/Tistory editor UAT
- homefeed and monthly-one-million efficacy
