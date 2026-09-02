# Independent Stage 3–4 Audit: HumanEval `126-is-sorted`

## Scope and result

The launcher environment and `/audit-input.json` both select
`CLASSIFICATION_ONLY` for condition `kit-semantics` in
`SUPPLIED_SEMANTICS` mode. Stage 4 is selected as
`KLEAN_NO_OBLIGATIONS`; `/candidate` is absent, as required. I did not rely on
the prior Stage 2 verdict, prior classification rationales, or recorded build
success.

The independent result is PASS. The frozen verification closure has exactly
15 rules, all 15 genuinely define proof-local functions or named summaries,
and none is a domain lemma. The consequently empty Stage 4 obligation set and
null generated target are exact.

## Input and producer integrity

I recomputed the launcher-recorded artifact hashes with the trusted tree-hash
implementations. The Stage 1 workspace, Stage 1 export, Stage 2 audit, complete
Stage 4 generation, producer-source tree, generated project, and Stage 3
manifest all match `/audit-input.json`. I also checked all 784 individually
recorded Stage 1 file hashes: 784 match, with no missing, mismatched, or
unrecorded files.

Before judging generation, I hashed the exact mounted producer files:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes equal the entries in `source-manifest.json` and
`generator-manifest.json`. The immutable generator image identifier also
agrees among the source manifest, generator manifest, and the basename of the
producer-source path recorded in `/audit-input.json`:
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The generator toolchain object equals `/reference/klean-toolchain.lock.json`.
There is therefore no producer-provenance `AUDIT_ERROR`.

Complete hash results are in
[`evidence/01-producer-and-hash-verification.txt`](evidence/01-producer-and-hash-verification.txt).

## Canonical rule inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`, not against any prior inventory report. It selected
module `VERIFICATION`; its local verification-module closure contains only
`VERIFICATION`. The reconstruction gives:

- `verification.k` SHA-256:
  `50ca32315206bd3a80238c32622abacb2de6fd416474f32ed23e3135d1d9c94b`
- canonical inventory SHA-256:
  `c5219c4f4f251272c52fa9684ad275eabd947f80b1e95afc4d2f7d773759af91`
- rule count: 15; unique identities: 15

The protected Stage 3 manifest has the same inventory hash and exactly the same
15 `source_rule_id` values in the same order. There are no omissions, extras,
duplicates, or reordered identities. Because each `source_rule_id` is
`rule-<normalized_sha256>`, the ordered comparison also binds every normalized
source hash. I independently retained every source span, normalized hash,
identity, attribute list, and classification in
[`evidence/02-inventory-reconstruction.txt`](evidence/02-inventory-reconstruction.txt).

The reconstructed span groups are lines 10–13 (three rules), 18–21 (two),
24–26 (two), 29–31 (two), 34–36 (two), 39–42 (two), 46–47 (one), and 53–56
(one). The only rule attribute is `[owise]` on line 13; there are no
`[simplification]` rules.

## Independent classification judgment

I classified by the frozen rule bodies and supplied MPY operational semantics,
not by names or Stage 3 rationales. All eight proof-local heads occur only in
`verification.k` and as summary terms in `spec.k`; none matches a `<k>` cell or
an MPY execution construct. Thus none is an execution/observation rule or an
operational bridge.

| Rule family | Count | Judgment |
|---|---:|---|
| `nonNegativeVals` | 3 | `DEFINITION`: exhaustive constructor definition of the theorem's nonnegative-integer input predicate. |
| `nextRepeated` | 2 | `DEFINITION`: complementary equality/inequality cases for one repetition-counter update. |
| `scanPrevious` | 2 | `DEFINITION`: base/step recurrence for the final previous value, descending on the sequence tail. |
| `scanRepeated` | 2 | `DEFINITION`: base/step recurrence for the final counter, descending on the tail. |
| `scanValue` | 2 | `DEFINITION`: base/step recurrence for the last loop-bound value. |
| `duplicateOK` | 2 | `DEFINITION`: base/step Boolean recurrence rejecting a step whose adjacent-run count exceeds two. |
| `scanDuplicates` | 1 | `DEFINITION`: named summary conjoining the prior result with `duplicateOK`. |
| `sortedWithAtMostTwo` | 1 | `DEFINITION`: guarded named contract predicate, not a proposition assumed about `sortVS`. |

The final rule deserves particular scrutiny. It unfolds a new Boolean symbol to
`VS ==K sortVS(VS)` conjoined with the duplicate scan. It does not assert that
`sortVS` is ordered, a permutation, or equal to some separately characterized
value; no proposition is installed as a simplifier. The Stage 1 reachability
claim must still show that program execution returns this named summary. It is
therefore a definition under the requested definition/domain-lemma boundary,
not a disguised domain lemma.

There are no `PROVED_DERIVED_LEMMA` entries, so the special earlier-proof/later-
use criterion is not invoked. The independent partition is exactly:

- `DEFINITION`: 15
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

The definitions are relevant. On the formal nonnegative-integer domain, the
source first computes whether the list equals its supplied-semantics sorted
value. It then increments or resets an adjacent-run counter and permanently
sets the result false at the third equal adjacent value. For a sorted list,
equal values are contiguous, so the run condition is exactly the at-most-two-
occurrences condition. For an unsorted list, the sorting conjunct is already
false. Independent examples and counterfactual mutations confirm that the
sorting conjunct, equality increment, threshold, and false-result accumulator
are all load-bearing; see
[`evidence/08-adversarial-examples.txt`](evidence/08-adversarial-examples.txt).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
against the required three inputs and the pinned lock file. The first invocation
exposed a sandbox PID-namespace defect before project inspection: Lean 4.22
looked for `/proc/<inner-pid>/exe`, while the mounted `/proc` exposes outer
PIDs. A narrowly scoped preload shim redirected only that exact self-executable
lookup to `/proc/self/exe`. It did not alter any mounted input or the trusted
checker. Both the initial diagnostic and shim source are retained in
[`evidence/04-preflight-initial-error.txt`](evidence/04-preflight-initial-error.txt)
and [`evidence/05-lean-proc-self-shim.c`](evidence/05-lean-proc-self-shim.c).

With that environment repair, the trusted checker returned exit 0 and:

- status `KLEAN_NO_OBLIGATIONS`
- Stage 1 hash `4e26e53af8776d28921938d383f5b264950b59c09cd48a3a2d06c2b4ad9fc7ce`
- Stage 3 hash `03fce957d0811ad8e1762c8ffc680c055e09e728b62be8fa60d266d32a9242e2`
- generated-tree hash `e78bf0ff4ee7a86c4582048e44ad52c83c42d28ca69341ab92723a0ee90f17c5`
- zero obligations and null target
- successful `lake clean` and `lake build`

The rebuild output hash is
`e54eec49cc5ffbf035369028fe9c104ecffbe124507173a0f34e15c31075159b`,
exactly the recorded output hash. The full returned evidence is
[`evidence/06-preflight-rerun.json`](evidence/06-preflight-rerun.json).

## Obligation bijection and fixed target

The independently classified true domain set is empty. Independently reading
and reconstructing the generation gives:

- `input-manifest.source_rules = []`
- `obligation-map.source_rules = []`
- `obligation-map.obligations = []`
- `obligation-map.trust_parameters = []`
- generator and export obligation counts are both 0
- the obligation-map file hash is
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`
- `klean_export.expected_target_definition(...)` returns `None`
- `klean_export.target_statement(...)` returns `None`
- `generator-manifest.target` is null

Thus the source-rule/obligation correspondence is an exact empty bijection.
There is no obligation that could be irrelevant, weakened, duplicated, omitted,
or made vacuous, and no generated target whose declaration or statement could
have changed. The generated `Lemmas.lean` contains only its import and empty
namespace. Detailed evidence is in
[`evidence/07-target-obligation-audit.txt`](evidence/07-target-obligation-audit.txt).

## Stage 5

Stage 5 proof checks do not apply. The launcher mode is
`CLASSIFICATION_ONLY`, the genuine domain set is empty, the generated target is
absent, Lean workspace/invocation hashes are null, and `/candidate` is absent.
Running candidate clean builds, printing `Proof.final` axioms, or auditing
target parameters would contradict the selected no-obligation mode rather than
add evidence.

## Final judgment

The protected Stage 3 classification agrees with an independent semantic
classification, and deterministic Stage 4 faithfully represents the genuinely
empty domain-lemma set. All producer, source, inventory, sidecar, target, and
tree identities are intact. The no-obligation result is legitimate.

VERDICT: PASS
LEGITIMACY: LEGIT
