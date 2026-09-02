# Independent audit: HumanEval 62-derivative

## Scope and decision

This audit covers Stage 3 lemma classification and deterministic Stage 4
generation for condition `kit-semantics` in `SUPPLIED_SEMANTICS` mode.
`AUDIT_MODE` and `/audit-input.json` both select `CLASSIFICATION_ONLY`.
The selected Stage 4 status is `KLEAN_NO_OBLIGATIONS`; the recorded Lean
workspace and invocation hashes are null, and `/candidate` is absent.
Accordingly, the Stage 5 candidate-proof checks are not applicable.

I treated the mounted Stage 1/2/3/4 artifacts, their prose, and their earlier
verdicts as untrusted evidence. The conclusion below does not rely on the prior
Stage 2 review or any prior PASS label.

## Producer-source authentication

The producer-source gate passed before Stage 4 was judged:

| Producer | Observed SHA-256 | Recorded SHA-256 |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both hashes match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The producer directory contains
exactly those two files plus `source-manifest.json`; its tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
matching `/audit-input.json`. The generator manifest, source manifest, and the
producer-bundle path recorded in `/audit-input.json` all identify image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
There is no producer-provenance mismatch.

## Rule-inventory reconstruction and bijection

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`. The local verification-module closure is exactly
`VERIFICATION`; its selected main module imports no other module defined
locally in `verification.k`.

- `verification.k` SHA-256:
  `4b8ad62368366efc2fc25468c32786a872c3fc53d6187c883e5e6c44624cbe63`
- Reconstructed rule count: 5
- Reconstructed whole-inventory SHA-256:
  `0d47ff2367ef2c6bf87c730b4ca6f2d2c6d07dfa5c78f5d7fc08aad9fbf67f69`

For each rule, I independently recomputed `sha256(" ".join(text.split()))`;
each digest equals both `normalized_sha256` and the suffix of its
`source_rule_id`. Physical text line counts agree with every reconstructed
source span.

| Span | Normalized SHA-256 / source identity | Attributes |
|---|---|---|
| 9 | `82fd85d7d877438e349407a829d1e35806842c5943d9c0f294aa58ed3173779c` | `simplification` |
| 10-13 | `51a3749a6415a476a599f9f4b4d86298466c83cbf2e19efd98a63953ec251c03` | `simplification` |
| 14-20 | `699bb53c2b20d45244efa55313af6891bd44df240c352ce9088ca451eccca62c` | `simplification` |
| 25 | `69d164c2333b75d39789a2087d0efc8310446075e2ed8ca85aaa99880622898f` | none |
| 26-27 | `cdffeaf04d811ef623fa1b34b1412c6bea8d70a043f5ca0aa93d9bec48680e9a` | none |

The protected Stage 3 document has the same inventory hash and exactly these
five IDs in exactly this order. Both ID lists are duplicate-free, and their
sets and lengths are equal. Thus there are no omissions, additions,
duplicates, reorderings, span changes, or normalized-source changes. The
Stage 3 schema stores classification metadata keyed by `source_rule_id`; the
whole-inventory hash binds the omitted source text and metadata.

## Independent Stage 3 classification

I independently classify all five entries as `DEFINITION`, agreeing with the
protected document.

The first three equations define the fresh proof-summary function
`derivAcc(ACC, remaining, I)`:

1. An empty remaining sequence returns `ACC`.
2. For a nonempty sequence with `notBool (I >Int 0)`, the head is skipped and
   recursion continues on the structurally smaller tail with `I +Int 1`.
3. For `I >Int 0`, the recurrence appends
   `applyBin("*", I, V)` and continues on the smaller tail.

These guards are disjoint and exhaustive for `Int`, and the recursion descends
on `REST`. This is a definition of a named summary, not a fact asserted about
an already defined symbol. It also matches the frozen source and supplied
operational semantics: the source iterates over the list, tests `i > 0`,
appends `i * x` to a mutable result list, and increments `i`; the supplied K
rules implement list iteration, the append heap update, binary-operator
dispatch, and integer multiplication in those same terms. For the prompt
example `[3, 1, 2, 4, 5]` at index zero, the recurrence skips `3` and yields
`[1, 4, 12, 20]`.

The final two equations define the fresh, total structural predicate
`noRefsVS`: the empty sequence is true, and a constructor is accepted exactly
when its head is not a supplied-semantics `ref` and its tail is accepted. They
define a named precondition proof term; they do not assert that an arbitrary
input satisfies it. The predicate is relevant to the frozen claims because it
excludes operational heap handles from their read-only input sequence.

Neither fresh symbol appears on an operational `<k>`-cell left-hand side.
Outside `verification.k`, the symbols occur only in Stage 1 claim
preconditions/postconditions. No rule skips or preempts fixed execution. A
counterfactual guard admitting index zero would incorrectly append the
constant coefficient; a constant appended value would fail when `I` or `V`
changes; and a constant-true `noRefsVS` would incorrectly admit `ref(H)`.

Independent counts are therefore:

- `DEFINITION`: 5
- `OPERATIONAL_RULE`: 0
- `PROVED_DERIVED_LEMMA`: 0
- `DOMAIN_LEMMA`: 0

All three `simplification` rules are definitions. There is no hidden or
mislabeled domain lemma, and no derived-lemma claim for which the required
earlier bridge-free proof would need to be established. The true domain set is
genuinely empty.

## Recorded-hash reconciliation

I recomputed the pipeline tree hashes, deterministic-export tree hashes,
protected-manifest hash, verification-file hash, inventory hash,
obligation-map hash, trust-inventory hash, and producer-file hashes. I also
recomputed all 774 Stage 1 per-file hashes and compared their exact path set.
Every value matches `/audit-input.json` and the applicable Stage 4 sidecars;
there are no missing, extra, or changed Stage 1 files. The trusted
`verify_stage6_audit_input` contract also accepts the mounted audit input and
recomputes resolved-input digest
`5d461ef8884793827c2d253bff882886a75e408533b570cc907d2d81d1d7e6b5`.

Important reconciled values include:

- Stage 1 pipeline tree:
  `41751d5d09bb6247a34e650b0920e8e1efd7a4b3f2055247e91668a7fc301664`
- Stage 1 deterministic-export tree:
  `ae3b6f950d5e6fd8a8a6ae9c6de36e303a53a1f6c97260105afd0271c90de23a`
- Stage 3 discovery file:
  `c3248818330bb9f59fff37f43f7ab3e60abacb8a08c55cba4cc8849aaa1f8c56`
- Selected Stage 4 generation tree:
  `52ad8da738aa04182383f899f8eac366335e6e04b190d0242e1c45f657260393`
- Generated project export tree:
  `e341931d0934bc45b96a7a5a074c6e61059b461ba49ffb4e20b31620db317dfa`
- Obligation map:
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`

## Stage 4 obligation and target identity

The independently validated Stage 3 classification produces an empty ordered
domain-source list. The Stage 4 input manifest contains the exact five
validated definitions and empty operational, derived-lemma, and source-rule
lists. `generated/obligation-map.json` contains exactly:

- `source_rules: []`
- `obligations: []`
- `trust_parameters: []`

The source-ID and obligation-ID sequences are therefore exactly bijective and
duplicate-free at cardinality zero. Both the generator manifest and export
result record obligation count zero. There are no conjuncts that could be
irrelevant, weakened, duplicated, or vacuous.

The trusted target parser returns no generated target. The expected target
definition from the empty obligation map is also absent, and
`generator-manifest.json` plus `/audit-input.json` both record `target: null`.
`Klean62Derivative/Lemmas.lean` has an empty namespace and declares no target
proposition. Thus the actual, generated-manifest, and audit-input target
identities agree exactly at `null`; there is no target change or shadow.

## Trusted preflight rerun

I invoked `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required frozen Stage 1, protected Stage 3, selected Stage 4, and pinned
toolchain paths.

The first invocation exposed a sandbox defect before Lean read any source:
Lean 4.22 calls `readlink("/proc/<getpid()>/exe")`, while this audit sandbox
exposes only `/proc/self/exe`. I preserved that exact failed output. I then
used a narrowly scoped compatibility shim that maps only numeric
`/proc/<pid>/exe` reads to `/proc/self/exe`, together with a synthetic Lake
layout pointing to the unchanged pinned installation. `lean --version` then
reported the required 4.22.0 commit.

With that environment compatibility in place, the unchanged trusted preflight
returned exit code zero and `KLEAN_NO_OBLIGATIONS`. Its internal fresh-copy
commands produced:

```text
lake clean: exit 0, empty output
lake build: exit 0
Built Klean62Derivative.Prelude
Built Klean62Derivative.Sorts
Built Klean62Derivative.Inj
Built Klean62Derivative.Lemmas
Built Klean62Derivative.Func
Built Klean62Derivative.Rewrite
Built Klean62Derivative
Build completed successfully.
```

The rerun result is exactly equal as JSON to both the mounted
`preflight.json` and the `stage4_preflight` object in `/audit-input.json`,
including diagnostic output hashes. It reports zero obligations, target null,
zero designated sorries, and 42 allowlisted non-propositional generated trust
declarations. With no proposition target and no Stage 5 proof, those boilerplate
declarations do not create a proof obligation or a route to proving a hidden
variant.

## Stage 5

Stage 5 proof auditing is correctly omitted. This is not proof mode, there is
no generated target to prove, `/candidate` is absent, and the audit input
records no Lean workspace or invocation. Creating `Base`, checking
`Proof.final`, printing its axioms, or auditing target parameters would invent
a candidate outside the selected audit mode.

## Evidence index

Principal raw evidence is under `evidence/`, especially:

- `03_reconstructed_inventory.json`
- `15_klean_preflight_command_and_result.txt`
- `17_focused_operational_semantics.txt`
- `18_stage4_independent_bijection_and_target.txt`
- `19_inventory_independent_hash_checks.txt`
- `22_independent_classification.md`
- `23_preflight_exact_reproduction.txt`
- `24_manifest_hash_reconciliation.txt`
- `COMMANDS.md`

The Stage 3 classification is complete and mathematically appropriate, the
true domain-lemma set is empty, and deterministic Stage 4 generation faithfully
represents that empty set with no generated target and no proof candidate.

VERDICT: PASS
LEGITIMACY: LEGIT
