# Validation Record - 2026-07-14u (governance findings on example code inform instead of gating)

TODO 23, chartered by 14t: an example demoing agent+shell without approval is a correct
finding at the wrong severity — and the labeled boundary (1,110 model-call examples TPs)
forbids fixing that with scope exclusion. The 13f move, extended to governance: a
**code-role taxonomy entry**, never an exception list (12t).

## What shipped

- `CodeRole.EXAMPLE_CODE` in the 13f taxonomy (`codeRoleClassification.ts`): a path under
  `examples?/`, `samples?/` or `demos?/` — the same segments TEST_GAP's layer scoping has
  used since 11i. `severityOverride: INFO`, with the action text stating both truths:
  documentation-by-code does not gate a deployment, and it IS the pattern users copy, so
  fixing it improves what ships downstream.
- The governance evaluator (`aiSystemPolicyEvaluator.ts`, v1.10.0) classifies each
  runtime context once and stamps example-role findings with the classification fields
  and the INFO override — all four governance rules uniformly (model-call, agent-shell,
  prompt-validator, state-write). **Detection untouched**: same findings, same anchors,
  same finding_ids (severity is not hashed).

## Measured — the whole diff is the charter, nothing else

- **Benchmark: 0 findings added, 0 removed; 3,345 severity flips (1,115 subjects × 3
  configs), every one `AI_MODEL_CALL_WITHOUT_VALIDATOR` on an example path → INFO**
  (vercel-ai 1,048, openai-node 37, openai-python 19, mem0 11). The gate stops blocking
  on an SDK's demo tree and keeps blocking on its runtime.
- **Injection: 0 added/removed; 9 flips** — the 2 agent-shell examples TPs (14t) and 1
  prompt-validator example, × 3 configs.
- Security families (`UNSAFE_EVAL` 6, `SHELL_EXECUTION` 1 on example paths) are a
  different detector layer with their own risk axis (14r risk-classes them per row) —
  deliberately out of charter; extending the taxonomy there is its own measured arc.
- **Ledgers re-emitted where the severity column went stale** (a ledger describes the
  detector): benchmark ledger 12m → **14u** (1,253 rows, 1,115 severities refreshed,
  labels byte-identical by finding_id) and agent/shell 14t → **14u** (2 refreshed).
  `EVIDENCE_MANIFEST` repointed; the reconciliation test binds it to `CURRENT_LEDGERS`;
  both corpora reconcile with **0 unexplained deltas**. Dossier regenerated — TP/FP
  counts unchanged (labels did not move).
- **427/427 tests** (+1: example path → INFO + classification; same content on `src/` →
  default severity).

## What this means for the buyer

A vercel-ai audit's governance gate no longer blocks on 1,048 findings in the `examples/`
tree it ships as documentation — it blocks on the 4 runtime ones. The findings are still
in the report, labeled "Example code", with the action text saying why they matter
anyway. Detection and risk, separated — the same doctrine that runs the whole registry
(12t, 13f, 14m, 14r).
