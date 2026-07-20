# LUMEN — Validation Evidence

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Produced by `npm run evidence` from the labeled CSVs under docs/validation/.
     `npm run evidence -- --check` fails if this file drifts from the data. -->

Every number below is **computed from hand-labeled data at build time**. None is
transcribed by a human, and the build fails if this file drifts from the labels.
That is not a stylistic choice: prose *did* drift here once, and it hid a real
false positive (see the negative record below).

Dossier version **1.1.0** · **3823** hand-labeled findings · **20** real products.

## What this is

LUMEN is a static auditor for AI systems. This document is its evidence base: what
it detects, how well, on what, and — as importantly — **what it deliberately does
not claim**. Everything here is reproducible from a clean checkout.

## In plain terms

An AI system fails in ways ordinary code review does not catch. LUMEN reads a
codebase and finds those places **before they ship**. It is a static auditor: it
finds the exposure, it does not stop an attack — and every count below is what it
found in **real, shipping open-source products**, hand-labeled one by one.

### It can be steered by the content it reads

If your assistant summarizes a web page, a support ticket, or an uploaded document, whoever wrote that text can hide instructions inside it. LUMEN finds the places where outside text reaches the model's own instructions with nothing separating the two — the boundary that stops a retrieved document from talking to your agent as if it were you.

**Found 28** across **6** real products. Measured by `PROMPT_INJECTION_UNTRUSTED_BLENDING`, `PROMPT_INJECTION_SECRECY_POLICY`, `PROMPT_INJECTION_CROSSFILE_BLENDING` — precision **1.000**.

### Its answers are trusted without being checked

A model's output flows onward into a database write, a workflow, another API call — with nothing verifying it is even the right shape. LUMEN finds those unguarded hand-offs: the model calls and prompts whose result no schema, validator, or parser ever inspects.

**Found 1254** across **11** real products. Measured by `AI_MODEL_CALL_WITHOUT_VALIDATOR`, `PROMPT_MISSING_STRUCTURED_OUTPUT`, `AI_PROMPT_WITHOUT_VALIDATOR` — precision **0.991**.

### Business decisions are hiding inside prompts

Pricing thresholds, eligibility rules and scoring formulas written into a prompt are decided by a language model — differently each time, with no audit trail, and invisible to the tests that cover your code. LUMEN finds the rules that drifted out of your codebase and into English.

**Found 6** across **4** real products. Measured by `PROMPT_CONTAINS_DETERMINISTIC_FORMULA` — precision **1.000**.

### Ordinary exposure, ranked by what it actually costs you

Hardcoded credentials, unsafe evaluation, shell execution — the familiar risks, with the familiar problem: a scanner that shouts about every one of them trains your team to ignore all of them. LUMEN detects each, then classifies what kind it is, so a key your vendor publishes on purpose never arrives wearing the same red as a leaked one.

**Found 58** across **3** real products. Measured by `HARDCODED_CREDENTIALS`, `UNSAFE_EVAL_USAGE`, `SHELL_EXECUTION` — precision **1.000**.

Of the 17 credentials it found across these products, 0 are security incidents.

### Reading the numbers

The tables below use the vocabulary of detection measurement. It decodes to four ideas:

- **True positive (TP)** — the tool flagged something, and it was real.
- **False positive (FP)** — the tool flagged something that was *not* a problem. This
  is the number that decides whether your team trusts the tool or learns to ignore it.
- **False negative (FN)** — a real problem the tool *missed*.
- **Precision** — of everything it flagged, how much was real. **Recall** — of
  everything real, how much it caught. Both run 0 to 1; higher is better.

A tool can look perfect by flagging almost nothing (high precision, terrible recall)
or by flagging everything (perfect recall, unusable noise). Both numbers are published
here for every rule, which is the only way either one means anything.

## The corpus

**20 real open-source AI products.** Not synthetic fixtures — shipping
code with real users, chosen because they contain the surfaces the rules target
(model calls, prompt templates, retrieval pipelines, agent tool-use).

**Benchmark slice (15)** — the labeled ledger's lineage:

`aider`, `files-to-prompt`, `gpt-researcher`, `instructor`, `langfuse`, `mem0`, `MetaGPT`, `openai-node`, `openai-python`, `openai-structured`, `prompt-cleaner-mcp`, `prompt-file-examples`, `Prompt-Injection-Playground`, `screenshot-to-code`, `vercel-ai`.

**Acquired slice (5)** — RAG/agent products added to test the injection rules
at scale, pinned to exact commits:

| Product | Commit | Tracked files |
|---|---|---|
| [browser-use](https://github.com/browser-use/browser-use.git) | `68afe46456` | 476 |
| [Flowise](https://github.com/FlowiseAI/Flowise.git) | `bb773ffa71` | 2444 |
| [LibreChat](https://github.com/danny-avila/LibreChat.git) | `cf9a426d29` | 3588 |
| [open-webui](https://github.com/open-webui/open-webui.git) | `ecd48e2f71` | 4960 |
| [private-gpt](https://github.com/zylon-ai/private-gpt.git) | `bcadb418f3` | 885 |

## Measured detection quality

Precision and recall over the hand-labeled corpus. `n` is the labeled denominator
(true positives + false positives + false negatives). Public-tier rows link the arc
that established them — the labeled CSV is in that directory. Rows marked *bundle*
name their arc and ship their labels in the evaluator bundle
(see [Two tiers of evidence](#two-tiers-of-evidence)).

| Rule | TP | FP | FN | Precision | Recall | n | Evidence |
|---|---:|---:|---:|---:|---:|---:|---|
| `ACCESS_CONTROL_UNSCOPED_OBJECT_LOOKUP` | 19 | 0 | 0 | **1.000** | 1.000 | 19 | 2026-07-13l · [bundle](#two-tiers-of-evidence) |
| `AI_AGENT_SHELL_WITHOUT_APPROVAL` | 1 | 5 | 1 | 0.167 → **1.000** | 0.500 | 7 | 2026-07-14r · [bundle](#two-tiers-of-evidence) |
| `AI_MODEL_CALL_WITHOUT_VALIDATOR` | 1200 | 9 | 4 | **0.993** | 0.997 | 1213 | [2026-07-14u](validation/2026-07-14u/VALIDATION_RECORD.md) |
| `AI_PROMPT_WITHOUT_VALIDATOR` | 22 | 2 | 0 | 0.917 → **0.917** | 1.000 | 24 | 2026-07-13f · [bundle](#two-tiers-of-evidence) |
| `HARDCODED_CREDENTIALS` | 17 | 53 | 0 | 0.243 → **1.000** | 1.000 | 70 | [2026-07-12c](validation/2026-07-12c/VALIDATION_RECORD.md) |
| `PROMPT_CONTAINS_DETERMINISTIC_FORMULA` | 6 | 0 | 0 | **1.000** | 1.000 | 6 | [2026-07-14u](validation/2026-07-14u/VALIDATION_RECORD.md) |
| `PROMPT_INJECTION_CROSSFILE_BLENDING` | 24 | 0 | 1 | **1.000** | 0.960 | 25 | 2026-07-13n · [bundle](#two-tiers-of-evidence) |
| `PROMPT_INJECTION_SECRECY_POLICY` | 3 | 0 | 0 | **1.000** | 1.000 | 3 | 2026-07-12j · [bundle](#two-tiers-of-evidence) |
| `PROMPT_INJECTION_UNTRUSTED_BLENDING` | 1 | 0 | 0 | **1.000** | 1.000 | 1 | 2026-07-12j · [bundle](#two-tiers-of-evidence) |
| `PROMPT_MISSING_STRUCTURED_OUTPUT` | 32 | 2 | 0 | **0.941** | 1.000 | 34 | [2026-07-14u](validation/2026-07-14u/VALIDATION_RECORD.md) |
| `SHELL_EXECUTION` | 1 | 0 | 0 | **1.000** | 1.000 | 1 | [2026-07-12c](validation/2026-07-12c/VALIDATION_RECORD.md) |
| `SHELL_EXECUTION` | 30 | 0 | 0 | **1.000** | 1.000 | 30 | 2026-07-14r · [bundle](#two-tiers-of-evidence) |
| `TEST_GAP_DETECTED` | 51 | 0 | 0 | **1.000** | 1.000 | 51 | 2026-07-13f · [bundle](#two-tiers-of-evidence) |
| `TEST_GAP_DETECTED` | 75 | 0 | 0 | **1.000** | 1.000 | 75 | 2026-07-14q · [bundle](#two-tiers-of-evidence) |
| `TEST_GAP_DETECTED` | 144 | 5 | 0 | 0.966 → **1.000** | 1.000 | 149 | 2026-07-14v · [bundle](#two-tiers-of-evidence) |
| `TEST_GAP_DETECTED` | 800 | 6 | 0 | 0.993 → **0.999** | 1.000 | 806 | 2026-07-14y · [bundle](#two-tiers-of-evidence) |
| `TEST_GAP_DETECTED` | 158 | 26 | 0 | 0.859 → **1.000** | 1.000 | 184 | 2026-07-14ab · [bundle](#two-tiers-of-evidence) |
| `TEST_GAP_DETECTED` | 799 | 49 | 0 | 0.942 → **1.000** | 1.000 | 848 | 2026-07-14ah · [bundle](#two-tiers-of-evidence) |
| `TEST_GAP_DETECTED` | 229 | 27 | 0 | 0.895 → **0.947** | 1.000 | 256 | 2026-07-16b · [bundle](#two-tiers-of-evidence) |
| `UNSAFE_EVAL_USAGE` | 11 | 10 | 0 | 0.524 → **1.000** | 1.000 | 21 | [2026-07-12c](validation/2026-07-12c/VALIDATION_RECORD.md) |

### The arrows are the point

Rows with an arrow are rules whose false positives **we found in our own tool and
fixed**. The left number is what the rule actually scored when we labeled it; the
right is what it scores after the fix. We publish both, because a product that only
ever shows you its final number is asking you to trust that it looked.

- `AI_AGENT_SHELL_WITHOUT_APPROVAL`: **5 false positives** found and eliminated at 2026-07-19b (evaluator bundle) — precision 0.167 → 1.000 over 1 surviving true positives.
- `AI_PROMPT_WITHOUT_VALIDATOR`: **2 false positives** found and eliminated at 2026-07-17a (evaluator bundle) — precision 0.917 → 0.917 over 22 surviving true positives.
- `HARDCODED_CREDENTIALS`: **53 false positives** found and eliminated at [2026-07-12c](validation/2026-07-12c/VALIDATION_RECORD.md) — precision 0.243 → 1.000 over 17 surviving true positives.
- `TEST_GAP_DETECTED`: **5 false positives** found and eliminated at 2026-07-14x (evaluator bundle) — precision 0.966 → 1.000 over 144 surviving true positives.
- `TEST_GAP_DETECTED`: **6 false positives** found and eliminated at 2026-07-14aa (evaluator bundle) — precision 0.993 → 0.999 over 800 surviving true positives.
- `TEST_GAP_DETECTED`: **26 false positives** found and eliminated at 2026-07-14ae (evaluator bundle) — precision 0.859 → 1.000 over 158 surviving true positives.
- `TEST_GAP_DETECTED`: **49 false positives** found and eliminated at 2026-07-16a (evaluator bundle) — precision 0.942 → 1.000 over 799 surviving true positives.
- `TEST_GAP_DETECTED`: **27 false positives** found and eliminated at 2026-07-17a (evaluator bundle) — precision 0.895 → 0.947 over 229 surviving true positives.
- `UNSAFE_EVAL_USAGE`: **10 false positives** found and eliminated at [2026-07-12c](validation/2026-07-12c/VALIDATION_RECORD.md) — precision 0.524 → 1.000 over 11 surviving true positives.

### Detection is not risk

`HARDCODED_CREDENTIALS` detects credentials. Whether a credential is an *incident*
is a **second question**, and answering only the first is how security tools earn
their reputation for noise. A PostHog project key IS a hardcoded credential — and
the vendor publishes it on purpose, to be embedded in client code. Reporting that
as CRITICAL is not a detection error; it is a **risk-classification** error.

So every credential is classified. Across the corpus's **17** detected credentials:

| Severity | Class | Count |
|---|---|---:|
| **LOW** | development_credential | 5 |
| **INFO** | public_by_design_identifier | 12 |

**0** of them are security incidents.

The rest are true findings that require no action, and they are still reported —
with their class — because deleting them would destroy traceability. What they are:

- PostHog Project API Key × 11
- Default Development Credential × 3
- Development Credential × 2
- Mixpanel Project Token × 1

An unrecognized credential is **never** quietly demoted: it stays CRITICAL as
`unclassified`, and a recognized secret format (an AWS key, a GitHub PAT) beats any
dev-looking location — a leaked key in a CI file is still a leaked key.

Full classification: [2026-07-12t/credential_classification.csv](validation/2026-07-12t/credential_classification.csv).

## The negative record — what we measured and refused to ship

This is the section most detection products cannot write, because writing it
requires having measured something and then thrown it away. Each of these was a
plausible improvement that a reasonable engineer would have shipped on intuition.

**2026-07-12i (record in the evaluator bundle) — Weak-delimiter refinement — treat quote-delimited untrusted text as undefended**

Measured at ~0.06 precision on the corpus and rejected. It would have turned a clean rule into a noise generator.

**2026-07-12o (record in the evaluator bundle) — Promotion of the cross-file rule on a claimed precision of 1.000**

The promotion review re-adjudicated every fire against the labeled baseline and found an unlabeled false positive (a RAG-indexing chunk). Real precision was 0.955, not 1.000. The promotion was STOPPED, the false positive was rooted out, and only then did the rule ship.

**2026-07-12q (record in the evaluator bundle) — Dataset dict-field provenance — close the last false negative by trusting a ["context"] subscript**

Rejected: it resurrected the false positive 12o had just closed, by laundering a weak signal through the gate that trusts genuine ingestion. The false negative stays registered instead.

**[2026-07-12t](validation/2026-07-12t/VALIDATION_RECORD.md) — Exonerating PostHog keys — silence the analytics-key credential findings**

Rejected as the wrong axis. The DETECTION was right; the RISK CLASSIFICATION was wrong, and an exception list neither scales (Segment, Sentry, Amplitude, LogRocket, Bugsnag are the same shape) nor keeps traceability. Built a classification LAYER instead: the rule still detects every credential, and a taxonomy decides what kind it is. Detection moved by zero findings.

**2026-07-12r (record in the evaluator bundle) — Sanitizer recognition — treat an escape/strip step before a prompt as exculpatory**

Censused across all 20 products and closed as UNMOTIVATED. Not one sanitizer in the corpus defends prompt content; they defend filesystems, databases, encodings, secrets and XSS. Measured, a file-scoped exoneration is a no-op and a repo-scoped one destroys every true positive.

## What the auditor finds in real products

The cross-file injection rule's true positives are **exposure surfaces in shipping
OSS products**: external retrieved content (scraped pages, fetched documents, RAG
results) reaching a prompt instruction with no instruction/data boundary.

**These are architectural observations, not vulnerability reports.** For a research
agent, blending scraped text into a prompt *is* the product; the finding names the
boundary that is missing, and the exposure that follows from its absence. We make no
exploitability claim, ship no proof-of-concept, and have not filed these as security
issues. They are here because they are **reproducible**: pin the commit, run the
auditor, get the same findings.

**The access-control rule is a different matter, and we treat it as one.** A missing
authorization check on an object-id handler *is* a vulnerability class (IDOR), not an
architectural style — so its number on the table above is reported as a **measurement
of the rule**, over a corpus adjudicated for precision, and nothing here names a file,
a line, or a route in any product. We have **not** assessed exploitability against any
deployment and have **not** notified maintainers, so this page does not identify the
handlers. The rule sees the code-shaped half only — the absence of a check in a
repository, never a live deployment; the other half of the breach that motivated it
(a real product's admin account with the password `123456`) is invisible to any static
scan, and the page says so under *What it cannot see*.

## Did it generalize? (the overfitting test)

A rule can score beautifully on the code its author was staring at while writing
it. The only honest test is code the rule has **never seen** — so five products
were acquired *after* the same-file rules were built, and those rules met them cold.

| Rule | Designed on | Benchmark TP | Acquired TP | Acquired FP | What the acquired slice tests |
|---|---|---:|---:|---:|---|
| `PROMPT_INJECTION_SECRECY_POLICY` | the 15 benchmark products | 3 | 0 | 0 | specificity — silence, verified correct |
| `PROMPT_INJECTION_UNTRUSTED_BLENDING` | the 15 benchmark products | 1 | 0 | 0 | specificity — silence, verified correct |
| `PROMPT_INJECTION_CROSSFILE_BLENDING` | all 20 products | 16 | 8 | 0 | nothing — in-sample by construction |

**What this proves.** Run cold against 5 unfamiliar products and **5,592 files**, the
same-file rules raised **5 false positives** — and a manual source-to-prompt census
confirmed the silence was *correct*: those products defend their prompts properly,
delimiting untrusted text and carrying it in its own message role. The rules did not
overfit to noise. Pointed at unfamiliar, well-built code, they had the good sense to
say nothing.

**What this does not prove — and we will not pretend otherwise.** They also found
*nothing new* there. Zero true positives in the acquired slice makes this a test of
**specificity**, not of discovery. It shows the rules do not invent findings in code
they have never read; it does not show they would find real ones.

The cross-file rule *does* find real things across unfamiliar products — **8 of its
24 true positives** live outside the benchmark, at 1.000 precision, so it is plainly
not a two-product special case. But it was designed with all twenty products already
in view. **Its numbers are in-sample by construction, and it has not yet had a true
out-of-sample test.** Claiming one would be the cheapest lie in this document.

**The experiment that would settle it:** acquire products the cross-file rule has
never seen, run it cold, and label every fire by hand — the same way everything else
here was measured. Until that runs, the honest answer to *does it generalize?* is:
**the specificity half is proven; the discovery half is not.**

Across every rule, the acquired slice contributes **45** true positives and **5** false positives.

## What that costs a team

A security tool's real price is not its licence. It is the hours an engineer spends
triaging what it says — and a tool that shouts about everything teaches its users
to hear nothing.

| | Count |
|---|---:|
| Alerts it used to raise on this corpus | 122 |
| False alarms removed by measurement | 63 |
| Still detected today (nothing was lost) | 59 |
| **Actually require action** after classification | **42** |

A team triaging the security rules across these twenty products would have opened
**122** alerts. Today they open **42** — **66% fewer**, and every
true positive is still found.

**What this number is not.** It is measured against *this tool's own earlier
behaviour* — not against another vendor's scanner. We have never run one, so we do
not claim a ratio against one. And the number belongs to this corpus; what
generalizes is the mechanism, not the percentage.

## What it cannot see

Every detection vendor publishes what it catches. Here is one it does not — the
real code, the real reason, and the real attempt to fix it. A boundary a tool
*states* is worth more than a capability it *claims*, because only one of the two
can be checked.

### MetaGPT — metagpt/ext/aflow/benchmark/hotpotqa.py:53

Registered 2026-07-12q.

```python
paragraphs = [item[1] for item in problem["context"] if isinstance(item[1], list)]
context_str = "\n".join(" ".join(paragraph) for paragraph in paragraphs)
inputs = f"Context: {context_str}\n\nQuestion: {input_text}\n\nAnswer:"
```

**What it is.** Retrieved Wikipedia paragraphs — content the system did not write — are pasted straight into a prompt instruction with no boundary between them and the question. It is the same shape as the 24 sites the rule does catch.

**Why LUMEN misses it.** The rule fires on external content only when it can PROVE the content is external: a real fetch, a scrape, a retriever call, a document field, or a prompt that declares its own source. Here the text arrives from a dataset dictionary — `problem["context"]` — and the file makes no external call at all. The provenance gate, which is the thing holding this rule's precision at 1.000, has nothing to grab.

**Why it is still open.** We built the fix and measured it. Treating a `["context"]` subscript as ingestion closed this miss — and RESURRECTED the false positive that the previous arc had just paid to close, because it laundered a weak signal through the gate that trusts genuine ingestion. So the fix was rejected and the miss stays registered. It is not a limitation we suffer; it is a trade we chose, with the numbers in front of us: one known miss beats one unknown false alarm.

That is the shape of every boundary here. Not a gap we have not gotten to — a
**trade made with the numbers in front of us**: one known miss beats one unknown
false alarm, because the miss is registered and the false alarm is what teaches
your team to stop reading the output.

## Declared boundaries

What the auditor does **not** see. A finding's absence in these areas means nothing:

- **Languages**: TypeScript/JavaScript and Python only. Go, Java, Ruby, Rust are unsupported.
- **Notebooks** (`.ipynb`) are scanned but have **no labeled rows** — unmeasured.
- **Static analysis only**: no code is executed. Dynamic imports and framework-specific
  runtime wiring can escape the uses graph. Every audit report carries this in `uncertainty`.
- **Registered false negatives** are listed per rule in the support matrix, with the
  arc that measured each one.

The full, current boundary list — the support matrix — is maintained as a first-class
artifact, not an afterthought, and ships in the evaluator bundle
(see [Two tiers of evidence](#two-tiers-of-evidence)).

## Two tiers of evidence

Not every label behind this page is downloadable, and we would rather state the
split than let you discover it.

**The public tier** — the commodity detections: credentials, unsafe evaluation,
shell execution, and the model-call validator family — ships its full ground truth
in this repository: **1345 labeled findings**, every CSV beside the dated record
that produced it, recomputable by `verify.py`.

**The gated tier** — the differentiated detectors: the injection family, access
control, the test-gap and agent-shell rules — publishes its numbers, its boundaries
and its registered misses on this page, and ships its ground truth — **2478**
**labeled findings** — as an **evaluator bundle**, under NDA, on request. The bundle
carries the labels, the full dated records, the support matrix, and its own copy of
the verify script that recomputes every gated number the same way.

The reason is stated plainly rather than buried: the labeled corpus is the asset a
copy of this product would need most. Handing the commodity part to everyone costs
nothing; handing the differentiated part to anonymous readers is a disclosure
decision, and we made it the way this project makes every decision — recorded, with
the trade named (decision 004). An evaluator with a name gets everything.

**Evaluating LUMEN?** [Request the evaluator bundle](https://github.com/reoxb/lumen-evidence/issues) — say who
you are and what you are evaluating.

## Check it yourself

A measurement document that asks to be believed has failed. So here is everything
needed to disbelieve this one.

**The public tier's labeled data is in this repository.** Every finding behind the
public rows above — 1345 of them, each marked true positive, false positive or
false negative by hand — is committed as CSV beside the dated record that produced it.

**Recompute the numbers without taking our word for anything.** A dependency-free
script reads those CSVs and prints their table rows from scratch:

```bash
git clone https://github.com/reoxb/lumen-evidence
cd lumen-evidence
python3 verify.py          # recomputes the public tier's precision and recall from the labels
```

If its output disagrees with what you read above, the page is wrong and you should
say so.

**The gated tier is checkable the same way — by named evaluators.** The bundle
carries the remaining 2478 labeled findings and its own verify script. A number
you cannot recompute from this repository is marked *bundle* in the table, never
smuggled past you.

Every public-tier claim links to the dated record that grounds it; gated rows name
their arc. The corpus is pinned to exact commits, so the code we audited is the code
you would fetch.

## The engine is the product. Its homework is licensed reading.

LUMEN's detection engine is commercial and its source is closed, so **no, you cannot
run it from this repository.** That is the trade — stated in one sentence, rather than
buried in a footnote.

What we will not do is ask you to take the rest on faith. The commodity labels, the
public records, the pinned corpus, the doctrines we measured and threw away, and the
failures we cannot see are all here — and everything gated is one named request away,
checkable by the same script.

**A vendor confident in its product can afford to show its homework — and to say
which pages of it are licensed reading.** That is the argument of this page, and it
is the only one we intend to make.

**Want to see what it finds in your codebase?** Bring a repository — we will show you
the findings and the evidence behind each one, including the ones we get wrong.
[Get in touch](https://github.com/reoxb/lumen-evidence/issues).

