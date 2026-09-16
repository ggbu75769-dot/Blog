# HOMEFEED BLOG OS · implementation guidance

## Mission
Build the topic-to-finished-article editorial service specified in this package. Public posting is performed by the user on every platform. Do not implement publishing bots, platform login, posting APIs, auto comments, traffic manipulation, or video/commerce workflows.

## Read first
`docs/00_SCOPE_AND_DECISIONS.md`, `docs/01_PRODUCT_PRD.md`, `docs/10_ARCHITECTURE.md`, `docs/16_WORK_PLAN.md`, then the selected task in `docs/17_TASK_SPECIFICATIONS.md` and its acceptance cases in `docs/18_ACCEPTANCE_TESTS.md`.

## Working rules
- Inspect the real repository and preserve uncommitted user work. Do not overwrite existing AGENTS.md, force-push, reset hard, or deploy without authorization.
- Treat JSON schemas, states, requirements, task dependencies, and API contracts as a connected specification. Resolve conflicts explicitly and update tests with changes.
- Source credentials and actual providers may be missing. Implement REPLAY honestly; LIVE work must use configured and permitted sources and budgets. Never fabricate completion.
- Use genuine evidence for facts and scoped user records for personal experience. Style examples are not author biography.
- Verify the final edited article, not only the initial draft. No synthetic private analytics, homefeed probabilities, or AI-detector evasion.
- Keep tenant/blog scope in DB, cache, files, retrieval and prompts. Writer outputs cannot issue approval or modify budgets.
- Every expensive or long-running operation needs a durable job, checkpoint, idempotency and bounded retries. Unknown provider outcomes require reconciliation.
- Output real text, images where required, captions, sources and manual handoff guides. A prompt or placeholder is not an asset.
- Report executed tests separately from planned acceptance and manual editorial tests. Run `python tools/validate_bundle.py` when changing specification assets; this is NOT a service test suite.
- Finish a bounded task per session: implement, test, review and report. Do not promise future autonomous work.

## Code review
Block regressions that reintroduce automatic public posting, mix ad CTR and content CTR, turn null metrics into zero, leak private evidence into public exports, reuse stale review hashes, or rewrite a hypothetical/persona as real experience.


## R1 invariants and iteration
Read docs/25–30 for the verified gaps and migration impact. Use contracts/task_order.txt, not numerical task order. Run both tools/validate_bundle.py and tools/run_r1_checks.py. reference_core is not the production HTTP/DB/LLM implementation. Use REPRODUCE → REGRESSION → FIX → FULL RELATED CHECKS → CONTRACT/DOC SYNC; never delete failing tests to claim success. Preserve real data provenance, reviewer storage authenticity and source/blog scopes.

Editorial quality has a separate gate: compare candidate questions and first-screen promises, then separately evaluate finished writing with genuine blinded readers and edit time. Automated style scoring alone cannot certify human readiness or homefeed exposure.


## R2 content-first override
Apply docs/31~38 and CODEX_START_HERE.md for editorial workflow. Preserve all R1 safety/scope/rights/freshness controls. Keep ArticleIR 4.1.0 compatibility and use the separate r2.editorial.1 review sidecar. Never present deterministic lint, manually authored examples, or synthetic reader roles as real human or viral validation. Do not post publicly. Adversarial rendering fixtures belong only in tests/adversarial; never import them into a public article queue. If a document contract conflicts, record and resolve it across machine and prose specs rather than picking a convenient PASS.
