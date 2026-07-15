# Validation Record - 2026-07-12t (credential context classification: detection ≠ risk)

An audit of `HARDCODED_CREDENTIALS`' 17 true positives found that **12 of
them were analytics ingestion keys the vendor publishes on purpose** —
PostHog `phc_` project keys and a Mixpanel project token, write-only event
keys documented as safe to embed in client code. They were rated
**CRITICAL**.

The detection was **right**. The **risk classification** was wrong. Those
are different defects, and only the second one was ours to fix.

This arc separates **credential detection** from **credential risk
classification**. The rule still detects every credential; a second layer
answers *what kind of credential is it*, and severity follows from that.
Detection moved by **zero findings**.

## The fix that was rejected

The first proposal was to *exonerate PostHog keys*. It was rejected:

- **It does not scale.** Segment write keys, Sentry DSNs, LogRocket app
  IDs, Amplitude keys, Bugsnag keys, Stripe publishable keys, Google
  Analytics IDs — all the same shape. An exception list grows forever.
- **It destroys traceability.** A dropped finding cannot be reviewed. The
  goal is not to make the finding disappear; it is to make it *correctly
  calibrated*.

## What ships instead

```
Finding:         Embedded Analytics Project Key
Severity:        Info
Classification:  Public-by-design credential
Action:          None
```

That is still a finding. It has simply stopped being an incident.

| Class | Severity | Meaning |
|---|---|---|
| `private_credential` | **CRITICAL** | Secret material; leaking it is immediately exploitable |
| `production_credential` | **HIGH** | Bound to a live system, not a recognized secret format |
| `environment_dependent_credential` | **MEDIUM** | Risk depends on what fills it (templates, examples) |
| `development_credential` | **LOW** | Dev containers, CI fixtures, vendor default logins |
| `public_by_design_identifier` | **INFO** | The vendor publishes it on purpose |
| `unclassified_credential` | **CRITICAL** | Detected, not recognized — never demoted |

`Severity.INFO` is new, and it ranks **below LOW**: no `--fail-on`
threshold can reach it, so a public analytics key can never fail anyone's
build. It gets its own priority lane (`P4`) rather than sharing `P3` with
LOW — folding them together would put PostHog keys in the same backlog as
real dev-credential exposure, which is the exact conflation this layer
exists to end.

## Two safety properties, both load-bearing

**1. A recognized secret format beats context.** An `AKIA…` inside a CI
workflow is still a leaked AWS key. A dev-looking location never rescues
real secret material — otherwise the taxonomy becomes a laundering
machine. Pinned by test.

**2. Ignorance never downgrades.** A credential the taxonomy does not
recognize stays `unclassified` at **CRITICAL**. The count of unclassified
credentials is therefore a **quality metric**: it says exactly how much of
the credential surface the taxonomy actually understands, and every format
added moves findings out of it. It is a backlog, not a hiding place.

## Measurement

Detection is unchanged; only risk classification moved.

| | Before | After |
|---|---|---|
| Credentials detected | 17 | **17** (0 appeared, 0 disappeared) |
| Rated CRITICAL | 17 | **0** |
| Security incidents (CRITICAL/HIGH/MEDIUM) | 17 | **0** |
| INFO — public by design | 0 | **12** (PostHog ×11, Mixpanel ×1) |
| LOW — development | 0 | **5** (langfuse CI seed ×2, mem0 compose ×3) |

The corpus contains **zero live production secrets**. Nothing needs
rotation or disclosure — which is what made publishing the evidence
dossier safe, and what made its old credential row misleading.

## Why this mattered to the evidence dossier

`HARDCODED_CREDENTIALS: precision 1.000, 17 TP` was **true and
misleading**, and it was the weakest claim in
[docs/EVIDENCE.md](../../EVIDENCE.md). The dossier's greatest strength is
that it **reproduces** — the corpus is pinned, anyone can run it. That is
exactly what made the claim dangerous: a sharp engineer at aider or mem0
would have found their own public PostHog key flagged CRITICAL and
concluded the tool does not know what a secret is — and that conclusion
would have poisoned every *other* number in the document, including the
ones that are genuinely strong.

The dossier now reports the risk split beside the precision, derived from
the classifier's own output
([credential_classification.csv](credential_classification.csv) — coordinates
and classes only; **no credential material is stored**).

## Verification

- **321/321** tests (+7): the taxonomy, `INFO` below every gate threshold,
  a recognized secret format beating a dev context, ignorance not
  downgrading, and the assignment parser.
- Full batch: credential `finding_id`s **identical** — 17 before, 17 after,
  0 appeared, 0 disappeared. Detection is byte-stable.
- Flip-check vs the 1253-row ledger: **0 disappeared / 0 appeared**.
- SecurityReviewer 1.3.0 → **1.4.0**.

## Read

A detector that reports what it found is half a product. The other half is
telling you whether it matters — and a tool that calls a vendor's
public-by-design identifier a CRITICAL credential leak has answered the
first question correctly and the second one so badly that users learn to
ignore both. The taxonomy is the second half, and it scales the way an
exception list cannot: the next vendor's public key is a row, not a patch.

## Artifacts

[credential_classification.csv](credential_classification.csv) — all 17
detected credentials with their class, severity, label, and action.
