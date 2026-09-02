# Independent Stage 3–5 audit: `143-words-in-sentence`

## Scope and result

The launcher binding validates as problem `143-words-in-sentence`, condition
`kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, and audit mode
`CLASSIFICATION_ONLY`. The selected Stage 4 status is
`KLEAN_NO_OBLIGATIONS`. There is no `/candidate`, Stage 5 result, Lean
workspace, Lean invocation, or generated target. I therefore audited Stage 3
and Stage 4; the conditional Stage 5 proof checks do not apply.

I did not rely on the selected Stage 2 verdict or any prior classification.
The command ledger is in [evidence/COMMANDS.md](evidence/COMMANDS.md), and the
complete raw results are in the adjacent evidence logs.

## Input integrity and producer provenance

The trusted Stage 6 input contract validated with binding digest
`3cbcbb3d6f0c1cdd96b94c3e51afddc2adaa3496f77ff252123b108ea3563445`.
Independent recomputation matched every launcher-recorded digest:

| Binding | Recomputed SHA-256 |
|---|---|
| Stage 1 workspace, pipeline tree format | `e8adec0aa7c3a087b2ea2c613e1909913e51502770343a8273444ef3776dde1c` |
| Stage 1 workspace, deterministic-export tree format | `8e20f6e838f0390c0a7e0cfcd290ec5153328c5d41ddc9468bc7fde1133be54f` |
| Stage 3 discovery manifest | `c7f208a6406d99316290eb058fb6e6adcdbb1a5a3bd48c9696f224b86446f634` |
| Selected Stage 2 tree | `b24084709052226aa22198074fd9415ac7895ba7b49fd501138285703ef29811` |
| Selected Stage 4 tree | `c3b9fca715b8be34fd4feb9695022611dabf21cdb52e5b425da7d6cd44b12c8e` |
| Generated project tree | `dc822c9e9fa7f3abd19662a5138c81d0551b805360975a8ac1f42b0ed84f00ec` |
| Producer-source bundle tree | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` |

All 794 recorded Stage 1 per-file names and hashes also matched, with no
missing, extra, linked, or mismatched entry. See
[evidence/07-independent-hash-and-inventory-checks.log](evidence/07-independent-hash-and-inventory-checks.log).

Before accepting Stage 4, I hashed the exact generation-time producer sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Those values exactly match both `source-manifest.json` and the exporter/Klean
fields in `generator-manifest.json`. The producer bundle contains exactly
those two files and the source manifest. Its source manifest, generator
manifest, and the image-key component of the audit-input producer path all
bind the same immutable image ID:
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
Thus there is no producer-provenance `AUDIT_ERROR`. Raw hashes are in
[evidence/06-producer-source-hashes.log](evidence/06-producer-source-hashes.log).

## Canonical rule-inventory reconstruction

I invoked the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen Stage 1 workspace and also independently re-normalized and re-hashed
each returned source span. The selected local verification-module closure is
exactly `VERIFICATION`; its imported supplied-semantics module is external to
the local `verification.k` module set. The frozen `verification.k` SHA-256 is
`3a62f8d48b5acddb813cc3b2e22e191e1ea1f23a5afe92ca3df8fde2a2119e71`.

The reconstruction contains 18 unique rules and has canonical inventory hash
`2da0b74c0f727c025741ac5cb91807cc58ba40be9a2dbd5600b8df75788bc112`.
That hash matches the protected Stage 3 manifest. The manifest also contains
exactly 18 unique IDs in the canonical order. There are no omitted, extra,
duplicated, reordered, or changed identities. For every entry, the independently
computed normalized SHA-256 equals the inventory hash field, and
`source_rule_id` is exactly `rule-<normalized-sha256>`.

The following table records my independent classification. The ID column is
the leading portion of the normalized digest; full IDs, complete source text,
spans, attributes, and recomputed hashes are in
[evidence/07-independent-hash-and-inventory-checks.log](evidence/07-independent-hash-and-inventory-checks.log).

| Rule | Lines | ID prefix | Attribute | Independent class | Reason |
|---|---:|---|---|---|---|
| `#primeTuple` | 8–14 | `954b26aeba5f` | — | `DEFINITION` | Compile-time macro for the exact tuple-expression AST in the frozen solution. |
| `#emitSelected` | 17–23 | `2756591a03f0` | — | `DEFINITION` | Compile-time macro for the exact output assignment AST. |
| `#maybeEmit` | 26–32 | `96f70e5bce38` | — | `DEFINITION` | Compile-time macro for the source conditional AST. |
| `#scanBody` | 35–42 | `1e3e5c700057` | — | `DEFINITION` | Compile-time macro for the source loop-body AST. |
| `#wordsBody` | 45–51 | `2a7151753289` | — | `DEFINITION` | Compile-time macro for the complete function-body AST. |
| `#solutionModule` | 54–59 | `7a194de92301` | — | `DEFINITION` | Compile-time macro for the module/function AST. |
| `primeLength`, selected case | 65–75 | `e1b7497bc52e` | simplification | `DEFINITION` | Guarded equation defining the new Boolean summary on the listed lengths. |
| `primeLength`, complement | 76–87 | `ff3a022d72a4` | simplification | `DEFINITION` | Complementary equation completing the new Boolean summary. |
| `emitWord` | 90–94 | `4f6f4f7a1d19` | — | `DEFINITION` | Defines the accumulator update chosen by `primeLength`. |
| `scanOutput`, empty | 101–102 | `b0e46aae182d` | simplification | `DEFINITION` | Base recurrence for the output accumulator. |
| `scanOutput`, space | 103–105 | `0de54d4e1425` | simplification | `DEFINITION` | Separator recurrence: emit, clear the word, and descend. |
| `scanOutput`, non-space | 106–109 | `9dd9f5c09e83` | simplification | `DEFINITION` | Complementary recurrence: append the character and descend. |
| `scanWord`, empty | 113–114 | `c145da943a4b` | simplification | `DEFINITION` | Base recurrence for the current-word accumulator. |
| `scanWord`, space | 115–117 | `1b54f4c5464e` | simplification | `DEFINITION` | Separator recurrence clearing the word. |
| `scanWord`, non-space | 118–121 | `54cbe954b93a` | simplification | `DEFINITION` | Complementary recurrence extending the word. |
| `scanLast`, empty | 125 | `d3bd506233a3` | simplification | `DEFINITION` | Base recurrence returning the prior character. |
| `scanLast`, nonempty | 126–128 | `22406af886e3` | simplification | `DEFINITION` | Structural recurrence recording the head and descending. |
| `sentenceResult` | 131–138 | `d17705a59e34` | — | `DEFINITION` | Defines the final result as loop summaries, final emission, and supplied `strip`. |

All ten `simplification` rules are therefore `DEFINITION`; none is mislabeled
as an operational or merely asserted derived lemma.

## Classification judgment from the frozen program and K semantics

The first six rules are syntactic macros, not execution shortcuts. A fresh
Haskell-backend compile followed by independent `kast --expand-macros` runs
gave the same KORE hash for `solution.mpy` and `#solutionModule`,
`2f72eb135b5c7e2ce9a067f25246eebedd818a6337f52b6b67eb9ca1dcf6f84a`,
and an empty diff. See
[evidence/22-fresh-expanded-ast-identity.log](evidence/22-fresh-expanded-ast-identity.log).

The remaining rules introduce and define proof-local mathematical functions.
They do not rewrite a `<k>` configuration, select a binding, skip a call, pop a
frame, mutate an operational cell, or otherwise replace ordinary execution.
The supplied semantics iterates a string one character at a time, binds the
loop target, evaluates the `If`, and updates the current scope. Its `len`,
tuple-membership, string concatenation, and `strip` rules have exactly the
operations used by these recurrences. Relevant frozen rules are preserved in
[evidence/08-relevant-operational-semantics.log](evidence/08-relevant-operational-semantics.log)
and [evidence/09-more-operational-semantics.log](evidence/09-more-operational-semantics.log).

The recurrence cases are total, disjoint where guarded, and descending:

- `primeLength` has a finite selected guard and its exact Boolean complement.
- `scanOutput` and `scanWord` cover empty, leading-space, and leading-non-space
  sequences; recursive calls consume one constructor.
- `scanLast` covers empty and nonempty sequences and consumes one constructor.
- `emitWord` and `sentenceResult` are nonrecursive compositions of these
  summaries and supplied string functions.

The name `primeLength` does not turn its equations into a domain lemma. It is a
fresh symbol whose equations define membership in the exact finite tuple used
by the frozen source. No rule asserts that an independently defined predicate
is prime, or derives a primality theorem. Under the formal length bound of 100,
an independent trial-division check nevertheless confirmed that the tuple is
exactly the mathematical primes from 0 through 100.

There is also no `PROVED_DERIVED_LEMMA`: none of the 18 exact rules is first
proved against a module excluding it and later installed. The separately
proved `scan-loop` item is a reachability claim in `spec.k`, not an inventory
rule. There is no ordinary `OPERATIONAL_RULE` in this proof-local closure.

As supplementary sensitivity evidence, a fresh K compile and proof produced
`#Top` for both the exact loop claim and the complete claim set. Changing only
the source body’s emitted separator from code 32 to code 120, while leaving the
summaries intact, made the proof fail with a residual comparing the two
distinct accumulator updates. Appending code 120 to the required final result
also failed with a stuck implication. See
[evidence/23-fresh-kprove-loop.log](evidence/23-fresh-kprove-loop.log),
[evidence/24-fresh-kprove-full.log](evidence/24-fresh-kprove-full.log),
[evidence/26-body-mutation-kprove.log](evidence/26-body-mutation-kprove.log),
and [evidence/27-false-postcondition-kprove.log](evidence/27-false-postcondition-kprove.log).

An independently implemented executable comparison exercised 9,960 boundary,
exhaustive-length, pair-length, repeated-space, and deterministic random
sentences. It found zero recurrence/direct-execution mismatches and zero
intent-oracle mismatches. Counterfactual separator, final-emission, and
select-every-length implementations each produced a concrete distinguishing
witness. This is finite corroboration, not a substitute for the universal K
claims. See
[evidence/31-summary-oracle-and-counterfactuals.log](evidence/31-summary-oracle-and-counterfactuals.log).

My independent classification is therefore exactly 18 `DEFINITION`, zero
`OPERATIONAL_RULE`, zero `PROVED_DERIVED_LEMMA`, and zero `DOMAIN_LEMMA`.
The true domain-lemma set is genuinely empty and every classified item is
relevant either to the exact source AST, loop state, or final result.

## Deterministic Stage 4 generation

I reran the required
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
specified frozen Stage 1 workspace, protected Stage 3 manifest, selected Stage
4 generation, and pinned toolchain lock.

The first invocation reached the clean-build step but the managed PID namespace
prevented Lean from resolving `/proc/<getpid>/exe`; Lean reported that it could
not detect its installation. The failure and environment diagnosis are kept in
[evidence/10-rerun-klean-preflight.log](evidence/10-rerun-klean-preflight.log)
through [evidence/16-lake-home-diagnosis.log](evidence/16-lake-home-diagnosis.log).
I resolved this infrastructure-only condition with the recorded
`proc_exe_shim.c`, which intercepts only `/proc/*/exe` reads and returns the
kernel-provided `AT_EXECFN`. With the shim, the pinned executables report Lean
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05` and the matching Lake.
The shim source and binary hashes and exact build command are in
[evidence/17-proc-exe-shim-build-and-test.log](evidence/17-proc-exe-shim-build-and-test.log).
It does not modify the generated project, theorem text, or evaluator.

The exact checker rerun then returned `KLEAN_NO_OBLIGATIONS`, with:

- `lake clean`: exit 0, empty output hash
  `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`;
- `lake build`: exit 0, successful nine-job build output hash
  `a2fa8b66a0c237a56c49734a78d777026ccbb046f9d2e2c77efb9dad4956d009`;
- Stage 1 export hash
  `8e20f6e838f0390c0a7e0cfcd290ec5153328c5d41ddc9468bc7fde1133be54f`;
- Stage 3 hash
  `c7f208a6406d99316290eb058fb6e6adcdbb1a5a3bd48c9696f224b86446f634`;
- generated tree hash
  `dc822c9e9fa7f3abd19662a5138c81d0551b805360975a8ac1f42b0ed84f00ec`;
- obligation count 0 and target `null`.

The complete returned evidence is
[evidence/18-rerun-klean-preflight-with-proc-shim.log](evidence/18-rerun-klean-preflight-with-proc-shim.log).
The checker’s before/after snapshots also establish that the mounted inputs did
not change during the run.

I separately checked the Stage 4 relationships instead of treating preflight
as mathematical approval:

- `input-manifest.json` contains the exact 18 ordered canonical definition
  records and exact empty operational, proved-derived, and domain sets.
- The independently determined domain IDs, input `source_rules`, obligation-map
  `source_rules`, and obligation IDs are all the same empty ordered list.
- `obligations` and `trust_parameters` are empty; all three recorded obligation
  counts are zero and IDs are unique.
- `obligation-map.json` hashes to
  `cf331f312938e04436a60d1dc49b5a1f6f60b03f3283415439a7c175e9812048`,
  exactly the generator-manifest binding.
- Stage 1, Stage 3, inventory, verification source, generated tree, trust
  inventory, producer, and pinned-toolchain hashes agree across the input,
  generator, export-result, preflight, source, and audit-input manifests.
- The expected target definition is `None`; trusted target reconstruction
  returns `None`; the generator manifest and audit input both record `null`;
  and no generated Lean file contains `targetStatement`.

The independent check reports every item passing in
[evidence/19-independent-stage4-checks.log](evidence/19-independent-stage4-checks.log).
Because the domain set is genuinely empty, omitting a generated target is the
required fixed output. No obligation was omitted or duplicated, and no
irrelevant, weakened, vacuous, or `True` conjunct was substituted for the
empty set.

## Stage 5 and final assessment

This is not proof mode. The audit input records a null target and null Stage 5
result, `/candidate` is absent, and the generated `Lemmas.lean` namespace has
no target declaration. Accordingly, no `Proof.final`, candidate clean build,
candidate trust-escape scan, `#print axioms`, or operational-bridge parameter
audit is applicable. The absence is documented in
[evidence/28-generated-project-inspection.log](evidence/28-generated-project-inspection.log)
and [evidence/29-stage5-absence.log](evidence/29-stage5-absence.log).

The protected Stage 3 classification agrees entry-for-entry with the frozen
source and supplied operational semantics, the resulting true domain set is
empty, and the deterministic Stage 4 no-obligation generation is structurally
and mathematically appropriate.

VERDICT: PASS
LEGITIMACY: LEGIT
