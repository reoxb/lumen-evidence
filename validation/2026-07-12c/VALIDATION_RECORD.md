# Validation Record - 2026-07-12c (grandfathered rules: measured + fixed)

Pays the last v1.0 honesty debt: the security rule families that
pre-date the lifecycle get their first labeled measurement — and the
measurement was bad enough to fix in the same arc. SecurityReviewer
**v1.3.0**. HARDCODED_CREDENTIALS **0.243 → 1.000**, UNSAFE_EVAL_USAGE
**0.524 → 1.000**, SHELL_EXECUTION 1.000 unchanged; **zero true-positive
movement** (29/29 TPs preserved), ledger benchmark untouched
(1248/1248).

## The retroactive measurement (pre-fix)

Labeling every grandfathered-rule row the corpus fires
([baseline_labeling.csv](baseline_labeling.csv), 92 rows adjudicated by
hand, generator aborts on any unclassified row):

| Rule | TP | FP | Precision |
|------|----|----|-----------|
| HARDCODED_CREDENTIALS | 17 | 53 | **0.243** |
| UNSAFE_EVAL_USAGE | 11 | 10 | **0.524** |
| SHELL_EXECUTION | 1 | 0 | 1.000 (n=1) |

The boundary families (CORE/APP), AI_AGENT_SHELL_WITHOUT_APPROVAL, and
AI_STATE_WRITE_WITHOUT_ROLLBACK fire **zero rows** over the corpus; a
self-audit of the auditor surfaced one AI_AGENT_SHELL false positive (a
regex `.exec()` read as shell execution in testGapReviewer.ts) —
registered, not fixed here.

## Every FP class was a mechanical bug, so all were fixed

The measurement's value was naming the classes; each had a clean,
corpus-grounded route and none was a design judgment:

- **UNSAFE_EVAL_USAGE (10 FP → 0)**: `\beval\s*\(` matched member access
  and definitions. `redis.eval` runs a static Lua script, torch
  `module.eval()` switches inference mode, `bench.eval()` is a
  benchmark's own method, `def eval(...)` is that method's definition —
  none is language eval. Fixed with a negative lookbehind (`.eval`,
  `medieval`, `retrieval` excluded) plus a def-guard. The genuine
  eval-of-model-output TPs (aflow/MetaGPT extraction, mineflayer code,
  the AI SDK calculator tools) all still fire.
- **HARDCODED_CREDENTIALS (53 FP → 0)**, four classes:
  - *identifier values* (5): `openai_api_key = "OPENAI_API_KEY"`,
    `POST_CUT_BY_TOKEN = "post_cut_by_token"` — the value is an env-var
    name or enum, guarded when it is pure UPPER_SNAKE or equals the key
    case-insensitively;
  - *placeholders in example code* (~25): `your-key`, `bearer-token`,
    `fixture-session-token`, `invalid-api-key`, `demo-access-token-123`
    — the YAML arm's placeholder guards ported to the code pattern
    (`my` deliberately excluded — `mySuperSecretPassword123` is a real
    secret shape);
  - *test fixtures* (~23): langfuse's `*.servertest.ts` under
    `__tests__/` — the context gate learned both conventions;
  - *local-server defaults* (2): `lm-studio` / `vllm-api-key`, which
    those servers accept as any-string keys.

  The real hardcoded credentials — aider's Mixpanel/PostHog write keys,
  mem0's PostHog key across ten client copies, the 11s CI/compose
  secrets — all still fire.

## Verification

- 303/303 tests (3 new: eval member/def non-hits with real-eval hits,
  the four HARDCODED value-guard classes with real-secret hits, the
  `__tests__`/`.servertest` gate).
- Re-measured over the corpus: **29/29 TPs preserved, 63/63 FPs
  eliminated** — all three rules at precision 1.000.
- `npm run compare` flip-check: the three ledger benchmark rules
  (model-call 0.993/0.997, FORMULA 1.000/1.000, STRUCTURED 0.941/1.000)
  show zero movement — the security-rule changes touch no ledger row.

## Read

The ladder's obligation for the grandfathered rules was retroactive
validation; the honest thing the measurement demanded was not a footnote
but a fix. Two default-on security rules were shipping at 0.24 and 0.52
precision — a real user (the divergence dogfooding) had already hit the
worst class. Measuring named the bugs; the same arc closed them at full
recall. v1.0's honesty debt is now paid in numbers, not promises.

## Artifacts

Standard batch set; the pre-fix adjudication in
[baseline_labeling.csv](baseline_labeling.csv); ledger carried unchanged
(1253 rows).
