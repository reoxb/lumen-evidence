# Rule Lifecycle

This document applies the portable doctrine —
[change classification gate](lumen-agentic-framework/change-classification-gate.md)
and [release discipline](lumen-agentic-framework/release-discipline.md) — to
this project's own product surface: detection rules and governance policies.

The auditor's official outputs are findings. Rule and policy changes are
therefore output-affecting changes and enter the classification gate.

## Classifying a rule change

- **Correctness** — the rule is brought back to its documented intent:
  fixing a false-positive class, honoring an existing exclusion contract,
  repairing provenance. Evidence bar: domain coherence + regression
  fixtures proving intended true positives still fire (the finding diff is
  strictly FP-removal, or every removed finding is attributed).
- **Detection expansion (optimization)** — the rule flags more than before:
  new patterns, new heuristics, relaxed thresholds, a new rule. Evidence
  bar: domain coherence + measured precision/recall on labeled validation
  data before the rule is promoted to default-on.

## The evidence bar has a command

Both bars above say "the finding diff is attributed" and "measured on labeled
validation data". That obligation is executable, and it must be run:

```
npm run compare                       # emits the batch
npm run ledger:check                  # reconciles it against every labeled artifact
npm run compare -- --corpus <name>    # a category corpus (access-control, injection)
npm run ledger:check -- --corpus <name> --batch audits/<name>_validation_labeling.csv
```

`ledger:check` exits 1 on any unexplained delta, so an arc cannot land on a labeled row
it never accounted for. It reads the current artifact per rule family from
`CURRENT_LEDGERS` (`src/cli/ledgerCheck.ts`) — **a family missing from that list is
silently unchecked, so a new rule family must add its baseline there.**

**Absence means different things depending on the label** (2026-07-13n). A row the batch
no longer produces is a recall **regression** if it was labeled TP, a precision **win** if
it was labeled FP, and a **confirmation** if it was labeled FN. A row is **out of scope**,
never "disappeared", if the batch never scanned its repository or never ran its mode.
Reading all of these as one thing is how a hand-rebuilt curation script invented a
four-row "hygiene debt" that had never existed, and how that phantom then propagated into
the backlog and into this codebase's own doctrine for a week.

The same run censuses **what fires with no label at all**, per rule. A rule may be
measured on a deliberately narrow corpus — `TEST_GAP_DETECTED` stood at precision 1.000
over n=51, on three repositories, while firing 2,949 rows across the benchmark (13n);
six tranches later the census prints `fired 2,276, labeled 2,276 — 0 UNLABELED` (16b),
the 13n debt settled by adjudication, not by implication — the denominator is stated,
never implied. See [support-matrix](support-matrix.md).

## Publishing the evidence

The public dossier lives at **https://reoxb.github.io/lumen-evidence/**, served by GitHub
Pages from the `reoxb/lumen-evidence` repo. That repo is a **published snapshot**, not a
source: every file in it is a copy of a generated or committed artifact from this repo.

Publishing was once a manual copy, and it froze — the page drifted five arcs behind main,
publishing a superseded ledger, `TEST_GAP` at the wrong `n`, and omitting a default-on
rule, while `verify.py` (the reader's own recompute-from-scratch script) held a third,
hand-maintained copy of the source pointers that disagreed with the page it was meant to
check. So publishing is now one command:

```
npm run evidence                 # regenerate index.html, EVIDENCE.md, verify.py from the labels
npm run ledger:check             # 0 unexplained deltas — never publish a drifting ledger
scripts/publish-evidence.sh      # assemble the publish repo and push; Pages rebuilds
```

`verify.py` is **generated** from `EVIDENCE_MANIFEST` (`npm run evidence`), so the three
pointer lists — `CURRENT_LEDGERS`, `EVIDENCE_MANIFEST`, and the verifier's `SOURCES` —
cannot drift apart; a test reconciles them. The publish script re-runs `verify.py` inside
the publish tree before pushing: if the reader's script would disagree with the page, the
publish fails.

**Disclosure is tiered** (decision 004, record 14ai). Each `EVIDENCE_MANIFEST` entry
carries a tier: public sources ship labels + records in the public repo, recomputable by
the public `verify.py`; gated sources (the differentiated families) publish numbers and
arc names on the page, and ship their ground truth per named evaluator via
`scripts/assemble-evidence-bundle.sh <recipient>` — full validation tree, support matrix,
recipient stamp, and a full-manifest `verify.py`, under NDA. The publish surface is a
manifest, never a mirror: `npm run evidence -- --publish-list` names every `validation/`
file the public repo ships, and tests hold the boundary both ways (every public link
resolves; no gated artifact leaks). **New families default to gated labels at launch**;
moving a family's labels to the public tier is an explicit per-family decision.
Readership is measured (`scripts/snapshot-traffic.sh`, upserted CSV under
`docs/traffic/`) — the traffic API forgets after 14 days, so it runs at least
fortnightly, and with every publish.

## Lifecycle states

```
proposed → provisional → validated → default-on
                              ↘ retired
```

- **Proposed** — design written; the rule states what it detects, why the
  pattern is a governance risk, and its expected false-positive classes.
- **Provisional** — implemented and merged, but not default-on: gated
  behind explicit opt-in (the `--enable-llm-rules` precedent) or clearly
  labeled provisional in output. Must land with fixtures covering intended
  hits and known non-hits.
- **Validated** — the rule has labeled validation rows (TP/FP/FN) from the
  validation harness and its precision/recall are recorded with the rule
  registry version used.
- **Default-on** — promoted only from validated. Promotion is a versioned
  policy change (bump the rule registry version; follow
  [policy-change-template](lumen-agentic-framework/policy-change-template.md)).
- **Retired** — a rule whose measured precision stays unacceptable, or
  whose detection surface is superseded, is removed or demoted; findings
  produced under it remain interpretable via version metadata.

## Current state (honest)

All rules that predate this lifecycle were promoted to default-on before it
existed and are **grandfathered** at default-on.

The original labeling debt (0 of 33 rows) was closed on 2026-07-09: the
first fully labeled validation batch (79 rows, registry 1.3.0) lives at
[`docs/validation/2026-07-09/VALIDATION_RECORD.md`](validation/2026-07-09/VALIDATION_RECORD.md),
and the defects it surfaced were fixed and re-measured the same day
([2026-07-09b](validation/2026-07-09b/VALIDATION_RECORD.md): TEST_GAP
precision 0.444 → 0.800, AI_PROMPT recall 0.833 → 1.000, clean FP-only
delta).

`AI_MODEL_CALL_WITHOUT_VALIDATOR` was the first rule to enter at
**provisional** (`--enable-provisional-rules`). The expanded-corpus
measurement ([2026-07-09c](validation/2026-07-09c/VALIDATION_RECORD.md),
n = 216 across 7 structured-output repos) scored precision **0.704** /
recall ≤ **0.731** and **refused promotion**, registering a detector fix
backlog. The precision fixes shipped and were re-measured same-day
([2026-07-09d](validation/2026-07-09d/VALIDATION_RECORD.md): 0.704 → 0.868,
clean delta), followed by the delegated-validation exoneration arc
([2026-07-09e](validation/2026-07-09e/VALIDATION_RECORD.md)): precision
**0.892** / recall ≤ **0.771**, a perfectly clean delta (exactly the 5
targeted instructor FPs disappeared, zero TP movement). Two candidate
exoneration designs were rejected by the labeled corpus itself (importer-
side validation; name-shaped BaseModel evidence — the latter cost 16 TPs
in a re-run before the usage-shaped discriminator fixed it; both are pinned
as tests). The provider-coverage arc then closed the recall blocker and was
re-measured against the same labeled corpus
([2026-07-09f](validation/2026-07-09f/VALIDATION_RECORD.md)): precision
**0.946** / recall **0.966** over 857 target rows. Registry **1.4.0**
promotes the rule to default-on. The promotion PR also landed AI SDK
structured-output recognition, so the default-on detector was re-measured
against the same labeled corpus
([2026-07-09g](validation/2026-07-09g/VALIDATION_RECORD.md)): precision
**0.946 → 0.962** with recall flat at **0.966** — 12 structured-output FPs
exonerated, two `Output.json()` rows relabeled FP → TP under the 09c
json-mode doctrine, zero TP movement. New rules and detection expansions
continue to enter at provisional and follow the ladder.

**Legacy rules and retroactive validation.** The v0.1 deterministic rules
(`PROMPT_MISSING_STRUCTURED_OUTPUT`, `PROMPT_CONTAINS_DETERMINISTIC_FORMULA`,
the boundary/security/test-gap families) pre-date this ladder and have
been default-on since before labeled validation existed. The ladder's
obligation for them is retroactive: build the labeled record they never
had. For the two prompt rules that record now exists — the
[2026-07-10b](validation/2026-07-10b/VALIDATION_RECORD.md) FN sweep
established their first measured denominators, and the series through
[2026-07-10j](validation/2026-07-10j/VALIDATION_RECORD.md) carried them
across mechanism replacement, corpus growth, and contract recognition to
labeled numbers on a 15-repository corpus. The 2026-07-10k
through 2026-07-11n series then closed every named residual family —
composition fragments (composer chains), content surfaces
(conversational, prose-deliverable), judge rubrics (score output specs),
and the carried mid-template LLM row (template-scope gate) — landing at
**1.000 / 1.000** (FORMULA) and **0.941 / 1.000** (STRUCTURED, the two
open rows being aider's runtime-composed prompts, closable per-repo via
`prompt_surfaces` declarations since
[2026-07-11d](validation/2026-07-11d/VALIDATION_RECORD.md)). Note:
records 07-10b through 07-10i described these rules as "experimental and
opt-in" — that phrasing is correct only for the LLM-backed reviewer
behind `--enable-llm-rules`; the deterministic rules were always
default-on (corrected in 07-10j).

The last two legacy families paid their retroactive obligation in the
2026-07-11h–11m arcs: `AI_PROMPT_WITHOUT_VALIDATOR` (default-on since
v0.4; the [11h record](validation/2026-07-11h/VALIDATION_RECORD.md)
initially mislabeled it provisional, corrected in 11i) went first
denominator **0.242** (n=33) → scoping **0.800** → MetaGPT growth
**0.435** (n=46, the small-n collapse the method predicts) →
consumer-gate recognition **0.917**; `TEST_GAP_DETECTED` went **0.261**
(n=23) → layer scoping **1.000** → growth-hardened **0.895** (n=38) →
declaration-only doctrine **1.000** over a robust n=31. Their corpora
live beside the benchmark ledger in each record's
`baseline_labeling.csv`, and both stories demonstrate the ladder's core
property: a number that has not survived corpus growth is not yet a
number.

The security families closed their obligation in
[2026-07-12c](validation/2026-07-12c/VALIDATION_RECORD.md), and the
measurement demanded a fix rather than a footnote: `HARDCODED_CREDENTIALS`
first labeled at **0.243** (17 TP / 53 FP) and `UNSAFE_EVAL_USAGE` at
**0.524** (11 TP / 10 FP) — two default-on security rules shipping at
sub-precision that a real-project audit had already hit. Every FP class
was a mechanical bug (eval member-access/definitions, credential
identifier-values, placeholder example keys, `__tests__` fixtures,
local-server defaults), so all were closed in the same arc at full recall
(29/29 TP), landing both at **1.000**. `SHELL_EXECUTION` measured 1.000
at n=1. The boundary families and the AI agent/state rules fire zero
corpus rows; their retroactive obligation stays open against a
denominator that does not yet exist (one self-audit `AI_AGENT_SHELL`
false positive is registered).

**Update 2026-07-14r: the agent/shell denominator now exists.**
`AI_AGENT_SHELL_WITHOUT_APPROVAL` was censused on the injection corpus
(where the agent surface acquired at 12h lives): **precision 0.167
(1 TP / 5 FP, n=6)** — both FP classes mechanical and registered as
correctness pendings (RegExp.exec matched as a Shell tool; examples/
passing the governance runtime gate), one cross-file FN registered
(MetaGPT's `terminal.py`, the 12d uses-graph gap). `SHELL_EXECUTION`
added n=30 as detection (risk-classed per row). The retroactive
obligation is PAID for the shell arm; `AI_STATE_WRITE_WITHOUT_ROLLBACK`
still awaits a denominator. The default-on-at-0.167 decision went
**fix-forward** (Juan, 2026-07-14) and completed same-day: the
RegExp.exec class closed at 14s (matcher lookbehind, removal-only), and
the "examples-scope" class dissolved at 14t — the labeled boundary
(1,110 examples-path model-call TPs) says example code IS governance
surface, so those two rows were label errors, corrected TP. Final:
**1.000 (n=3, thin), 1 registered cross-file FN.** Risk modulation for
example-role findings is TODO 23.

## The v0.6 injection rules: the first full-ladder walk

`PROMPT_INJECTION_UNTRUSTED_BLENDING` and `PROMPT_INJECTION_SECRECY_POLICY`
are the first rules to traverse the entire ladder under this discipline,
newest state last:

- **proposed → provisional**
  ([2026-07-11u](validation/2026-07-11u/VALIDATION_RECORD.md)): two rules
  land opt-in with a corpus baseline of n=4 true positives and fixtures
  for direct, indirect, and retrieval injection.
- **provisional → validated**: three censuses sharpened the boundary —
  cross-file blending deferred
  ([12d](validation/2026-07-12d/VALIDATION_RECORD.md)), sanitizer
  recognition found already-satisfied by design
  ([12e](validation/2026-07-12e/VALIDATION_RECORD.md)), and a corpus
  expansion to five real RAG/agent products
  ([12h](validation/2026-07-12h/VALIDATION_RECORD.md)) demonstrated
  **zero false positives over 5,592 files** with no genuine false
  negative. A candidate refinement (the weak-delimiter doctrine) was
  measured and **rejected** at ~0.06 precision
  ([12i](validation/2026-07-12i/VALIDATION_RECORD.md)).
- **validated → default-on**
  ([2026-07-12j](validation/2026-07-12j/VALIDATION_RECORD.md), registry
  **1.6.0**): promoted on the evidence above. The true-positive
  denominator stays n=4 — genuine injection *violations* are rare in
  well-engineered products — but the negative denominator (five large
  products, zero FP) is what promotion requires. The
  [policy_change.md](validation/2026-07-12j/policy_change.md) records the
  decision. No provisional rules remain.

`PROMPT_INJECTION_CROSSFILE_BLENDING` is the second rule to walk the full
ladder, newest state last:

- **proposed → provisional**
  ([2026-07-12l](validation/2026-07-12l/VALIDATION_RECORD.md)): the cross-
  file frontier — external retrieved content that arrives as a function
  parameter, invisible to the same-file rules — lands opt-in, its volume
  justified by the 12k census (~7–24 genuine sites).
- **provisional → validated**: recall gaps closed
  ([12m](validation/2026-07-12m/VALIDATION_RECORD.md), 17 → 21 sites), the
  labeled baseline grown to n=25 with recall measured against an
  adjudicated FN census ([12n](validation/2026-07-12n/VALIDATION_RECORD.md):
  21 TP / 0 FP / 4 FN, precision 1.000, recall 0.840), and a false
  positive found at promotion review — a RAG-indexing `chunk` firing on
  instruction purpose-vocabulary — **rooted out**
  ([12o](validation/2026-07-12o/VALIDATION_RECORD.md), detector 1.4.0,
  precision 0.955 → 1.000).
- **validated → default-on**
  ([2026-07-12p](validation/2026-07-12p/VALIDATION_RECORD.md), registry
  **1.8.0**): promoted on 21 TP / 0 FP over six real products. The 4 known
  misses are prompt-composition shapes owned by the promptComposition
  doctrine, not this rule. The
  [policy_change.md](validation/2026-07-12p/policy_change.md) records the
  decision. **No provisional rules remain** — every registered rule is
  default-on.
- **post-promotion recall closure**
  ([2026-07-12q](validation/2026-07-12q/VALIDATION_RECORD.md), detector
  1.5.0): recall **0.840 → 0.960** (21 → 24 TP, still 0 FP) via composed
  instructions, an instruction-vocabulary twin, and url slots. Two
  candidate mechanisms were measured and rejected — promotion does not end
  a rule's measurement, and a default-on rule earns each recall point the
  same way it earned its precision.

**v0.6 closes** at [2026-07-12r](validation/2026-07-12r/VALIDATION_RECORD.md):
sanitizer recognition, the category's last item, was **censused and closed
as unmotivated rather than built**. An exoneration can only remove
findings, and the rule is at precision 1.000 — so it needed a corpus site
where external content is sanitized before a prompt, and there is none:
across twenty repos, ~200 sanitizer calls defend filesystems, databases,
encodings, secrets and XSS, never prompt content. Real products defend
prompts by delimiting and role separation, both already exonerated (the
12e finding, now explained). A doctrine's safe scope measured as a no-op
and its natural scope zeroed the rule's recall — so nothing shipped. The
ladder's discipline runs in both directions: a rule earns its promotion by
measurement, and a mechanism earns its existence the same way.

## Broken access control (TODO 0d) — the ladder's newest rung

`ACCESS_CONTROL_UNSCOPED_OBJECT_LOOKUP` is the **only rule currently at
provisional**, and it is the first rule of a new CATEGORY: the registry had
no authorization rule at all until 2026-07-13j.

- **census, before any detector**
  ([2026-07-13i](validation/2026-07-13i/VALIDATION_RECORD.md)): the honest
  first question was whether the corpus could even measure such a rule. It
  can — 188 object-id handlers reaching a store in the labeled corpus — and
  the census overturned its own prior (a corpus-acquisition arc was expected
  and proved unnecessary). It also produced the rule's hardest design
  constraint as a *measured number*: a same-file rule fires **19 false HIGHs
  against langfuse**, the corpus repo with the best authorization design,
  because its guard is bound to the procedure TYPE in another file.
- **proposed → provisional**
  ([2026-07-13j](validation/2026-07-13j/VALIDATION_RECORD.md), registry
  **1.9.0**): labeled baseline n=11 (**11 TP / 0 FP**, precision 1.000,
  recall 1.000 against the adjudicated census), with langfuse's 156 subjects
  cleared as the negative set. The predicted 19 false HIGHs did not happen.
- **the exoneration sweep**
  ([2026-07-13k](validation/2026-07-13k/VALIDATION_RECORD.md), reviewer
  **1.1.0**): a precision measurement cannot see a false negative. Every one of
  the 336 handlers the rule CLEARED was dumped with the exact call that cleared
  it, and read. `publish_event(request, EVENTS.CHANNEL_DELETED, actor=user)` —
  an event publish, enforcing nothing — was clearing 16 handlers, among them a
  channel delete. **An authorization check can DENY (401/403); a publish cannot.**
  Four false negatives closed, all four of which the 13i census had also called
  guarded. Baseline 11 → 13, precision still 1.000.
- **provisional → VALIDATED**
  ([2026-07-13l](validation/2026-07-13l/VALIDATION_RECORD.md)): the category
  corpus. The repos that carry the authorization surface enter a corpus of their
  own — `npm run compare -- --corpus access-control` — rather than the benchmark,
  because those six repos fire **8,685 rows from other rules** (8,151 of them
  TEST_GAP) and folding them in would inject that many UNLABELED rows in a single
  stroke. Baseline **n=19, 19 TP / 0 FP, precision 1.000** over 349 subjects, 330
  cleared and swept. The rule is VALIDATED; it stays **provisional in the
  registry** until a policy change promotes it, which gets its own record.
- **validated → DEFAULT-ON**
  ([2026-07-13m](validation/2026-07-13m/VALIDATION_RECORD.md), registry
  **1.10.0**): promoted on the evidence above, with every fire in BOTH corpora
  reconciled against the labeled baseline (19 fires, 19 labeled, 0 unlabeled —
  the invariant a prose count violated at 12n) and every other rule
  byte-identical. The promotion required closing one more cross-file guard class
  first: FastAPI's **mount-time router dependency**
  (`include_router(chats.router, dependencies=[Depends(get_verified_user)])`),
  the framework's documented idiom, which leaves the handler file with no visible
  authorization at all. It has ZERO corpus instances — so it is warranted by the
  framework's semantics, not by measurement, and the record says so. Its failure
  mode is bounded: it can only CLEAR a handler, never fire one.
  [policy_change.md](validation/2026-07-13m/policy_change.md) records the decision.
  **No provisional rules remain.**

Two of the three candidate rules the census proposed are deliberately NOT built.
The **sibling-guard signal** on Express route tables (rule 2) stays DEFERRED with
a measured design rather than a guess (13l): its 107 object-id routes are a real
denominator, but its precision hinges on two cross-file resolutions —
mount-time middleware (`app.use(path, requireJwtAuth, router)`, langfuse's lesson
in Express) and a guard predicate that reuses 13k's "can DENY" index, because a
name list fails on Flowise's `requireFlowEdit` and passes on anything called
`authFoo`. Its true-positive population in this corpus is **one route**. The
**default-admin-credential** rule was **closed unbuilt** for want of a denominator
(5 subjects, all one dev-compose default, already LOW under 12t).

The rule detects the **code-shaped half** of an IDOR and is named for it.
McHire's root cause was `123456` on a live account — a deployment fact, in
no repository. The applicability envelope says so in the report, and the
category's name does not imply coverage it lacks.
