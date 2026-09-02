# Independent audit: `22-filter-integers`

## Scope and result

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, in
launcher mode `CLASSIFICATION_AND_PROOF`. I treated the mounted Stage 1–5
artifacts, logs, comments, and earlier verdicts as untrusted evidence. The
judgment below is based on a fresh rule inventory, source-level and
operational-semantic classification, deterministic-generation checks, and an
isolated Lean rebuild.

The protected Stage 3 classification is complete and correct. Stage 4 contains
the one required, exact, non-vacuous domain obligation. The submitted Lean
definitions implement the frozen operational meanings, and `Proof.final`
proves exactly the immutable generated target without axioms or trust escapes.

## Producer and input integrity

Before judging generation I hashed the mounted generation-time producer
sources:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`
- complete producer-source tree:
  `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`

The file hashes match both `source-manifest.json` and
`generator-manifest.json`. The immutable generator image is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`
in both manifests and in the basename of the producer-source path recorded by
`/audit-input.json`. The complete producer-source tree hash also matches the
audit input.

Every other accessible recorded tree or file hash matched, including both
Stage 1 tree encodings, the selected Stage 2 tree, the Stage 3 manifest, the
Stage 4 tree, the generated project, and the Stage 5 candidate tree. All 795
per-file Stage 1 source hashes recorded in `/audit-input.json` matched with no
missing or unsafe entries. See `evidence/01_producer_integrity_inputs.txt`,
`evidence/03_producer_crosscheck.txt`, and
`evidence/16_all_hash_crosschecks.json`.

## Inventory reconstruction and Stage 3 classification

I ran the trusted `tools.k_rule_inventory.inventory_verification` against
`/reference/k-proof`, not against the discovery manifest. It selected
verification module `VERIFICATION` and its local closure
`[VERIFICATION-SYNTAX, VERIFICATION]`. The reconstructed values are:

- `verification.k` SHA-256:
  `7047c29c93f99a396cf3ea700cfac5bf99914b160badbc07578419c6ba512bdd`
- inventory SHA-256:
  `ffdd03dae916c92bbeabedc0a48396bb3bec96dd06d1b7dedba0533f4cd5d4ae`
- ordered rule count: 5

The protected manifest has exactly the same five identities in the same order,
with no omission, duplicate, extra rule, reordered identity, changed span, or
changed normalized hash. The trusted trust-boundary validator also accepts the
bijection. Raw reconstruction and comparison are in
`evidence/14_inventory_reconstruction.json`,
`evidence/15_manifest_bijection_validation.json`, and
`evidence/16_all_hash_crosschecks.json`.

My independent classifications are:

| Span | Normalized hash prefix | Classification | Judgment |
|---:|---|---|---|
| 17–27 | `7a8aefa8…` | `DEFINITION` | `filterLoopBody` is a fresh macro expanded to the exact source loop-body AST. |
| 29–35 | `8e8f01b5…` | `DEFINITION` | `filterBody` is a fresh macro expanded to the exact source function-body AST. |
| 39 | `55b672e7…` | `DOMAIN_LEMMA` | The simplification adds a symbolic characterization of the pre-existing `isIntV`; Stage 1 never first proves this exact rule in a module omitting it. |
| 42 | `577aa383…` | `DEFINITION` | Empty-input base equation for the fresh `filterAcc` result summary. |
| 43–49 | `f78e3bc6…` | `DEFINITION` | Structurally descending `vCons` recurrence for `filterAcc`; with the base rule it covers all `ValSeq` constructors. |

There are no ordinary operational rules and no proved-derived lemmas. The only
`simplification` rule is correctly a `DOMAIN_LEMMA`. It cannot be relabeled as
a definition or proved-derived lemma: `isIntV` already exists in the supplied
semantics, and `prove.sh` compiles the new equation before any proof.

The domain lemma is relevant. The source executes
`isinstance(value, int)`; supplied semantics routes this to `isIntV`; and both
the loop summary and final heap result branch on `isIntV`. The supplied rules
make Int and Bool values true (Python Bool is modeled as an Int subtype) and
all other `Val` constructors false. Thus the lemma is neither unrelated nor a
postcondition smuggled in as another category. Full classification reasoning is
also recorded in `evidence/97_independent_classification.md`.

## Deterministic Stage 4 generation

I reran the required call:

```text
PYTHONPATH=/reference python3
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

The audit container initially prevented Lean from locating its executable:
numeric process IDs were absent from the mounted `/proc`, while the Lean
runtime queried `/proc/<pid>/exe`. I diagnosed this independently and used a
narrow `LD_PRELOAD` compatibility shim that redirects only numeric
`/proc/.../exe` `readlink`/`readlinkat` requests to `/proc/self/exe`. The shim
does not read or alter K, generated, or candidate sources. With it, Lean
reported the pinned version and commit
`4.22.0 / ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unchanged trusted
preflight returned `PASS`. The failed environmental attempt, diagnosis, shim
source and hashes, and passing rerun are preserved in
`evidence/19_rerun_check_generation.json`,
`evidence/20_lean_environment_diagnostic.txt`,
`evidence/67_proc_shim_build_and_test_success.txt`,
`evidence/68_rerun_check_generation_pass.json`, and
`evidence/98_proc_shim_source_and_hashes.txt`.

The passing rerun clean-built the generated project and reported:

- Stage 1 generator tree:
  `a460211bb5af3a32fb264c965121d7ad830b741bf1f87634bd2e296475bf42fc`
- Stage 3 manifest:
  `3b24b0b445d85628d427422bfe82b0c2c4d1435e11ec9a4ec421c43b1878d417`
- generated tree:
  `4373e7ecf5560f93d9da38ba10756c9b83b02a836b4b351fa23bc8f2bcf711db`
- obligation count: 1
- target declaration:
  `Klean22FilterIntegers.Lemmas.targetStatement`

The independently reconstructed domain set contains exactly
`rule-55b672e7…`, so one obligation—not `KLEAN_NO_OBLIGATIONS`—is required.
The obligation map has the same singleton rule in its source-rule and
obligation lists, in order, with unique identity, matching source span,
normalized hash, inventory hash, and discovery-manifest hash. Its SHA-256 is
`a435a376d565bac0e6939815cce9cc71880981697f714d13af1faa71768bf0a9`.
All four parameter-binding hashes and the conjunct hash
`4f89c4bcddfaf98aaa5e83e3a16d2713cfa329cb4f68bd3559584f364707cc95`
recomputed exactly.

The generated conjunct is the literal universal translation:

```text
∀ (V : SortVal),
  isIntV V =
    _orBool_
      (isInt (kseq (inj V) dotk))
      (isBool (kseq (inj V) dotk))
```

It is a direct equality over every `SortVal`, with no premise, implication,
`False`, extra conjunct, weakened sort, or fixed example. `SortVal` is
nonempty and has 17 constructors. This exactly matches frozen rule 39 and its
KORE lowering.

There is exactly one generated `def targetStatement`. Its complete definition
is the exact conjunction of the singleton obligation. Its recomputed record
matches the generator manifest, the passing preflight, and
`/audit-input.json`, including:

- definition SHA-256:
  `208fd7eec009785667504098beb9f5ef6869502db88292b54dcc009efecb4e54`
- fixed statement SHA-256:
  `fbdd687c6be919b8c205fedd33cc791e09cbb6fe05ccc5e72b1e627ae8578e64`

The independent bijection, hash, target, and non-vacuity checks are in
`evidence/69_generated_project_full.txt`,
`evidence/70_generated_target_focused.txt`, and
`evidence/79_independent_stage4_bijection_target.json`.

## Isolated Stage 5 rebuild and proof identity

I created `/tmp/audit-work/lean-proof-audit` without copying candidate build
artifacts. I copied only the candidate source/metadata files and copied the
immutable generated project to `Base`. Before building, `Base` had generated
tree hash `4373e7ec…`, exactly as recorded.

Because generated `Base` uses an absolute build directory, I first ran
`lake clean` in `Base`, then ran the required top-level commands:

```text
lake clean
lake build
```

Both exited 0. The build freshly compiled generated Prelude, Sorts, Inj,
Lemmas, and `Proof`, ending with `Build completed successfully.` Complete
outputs are in `evidence/84_fresh_base_lake_clean.txt`,
`evidence/85_fresh_proof_lake_clean.txt`, and
`evidence/86_fresh_proof_lake_build.txt`.

After the build:

- `Base` remained byte-identical to the immutable generated tree.
- Its target record still matched the generator manifest and audit input.
- No candidate source declared or shadowed `targetStatement`.
- Candidate sources contained no `sorry`, `admit`, `unsafe`, new `axiom`, or
  new `opaque`.
- The candidate added no trust declaration.

Lean's own type report is:

```text
Proof.final :
  Klean22FilterIntegers.Lemmas.targetStatement
    Proof._orBool_ Proof.isBool Proof.isInt
    Proof.«isIntV(_)_MPY-BUILTINS_Bool_Val»
```

Thus `Proof.final` has exactly the fixed generated theorem as its type; it is
not a copy, shadow, weakened theorem, or vacuous variant. `#print Proof.final`
shows a case proof covering all 17 `SortVal` constructors. The exact output is
in `evidence/91_print_check_Proof_final.raw.txt`.

## Axiom accounting

The exact requested Lean output from `#print axioms Proof.final` is:

```text
'Proof.final' does not depend on any axioms
```

The raw output is `evidence/87_print_axioms_Proof_final.raw.txt`. In
particular, there is no `sorryAx`.

The generated `trust-inventory.json` hash is
`dd470eb6068bf21535b72057568f743e72dc73d91b485fde2918f8cac1669b1f`,
matching `export-result.json`. Its 41 allowlisted data-level hook axioms match
the 41 generated declarations exactly. None is a dependency of `Proof.final`;
there are no unrecorded dependencies, and the candidate declares none.
Reconciliation is in `evidence/90_axiom_trust_reconciliation.json`.

## Operational-bridge judgment

The fixed target equation alone does not force honest parameter meanings. I
confirmed this adversarially: mutually constant-false definitions for all four
parameters prove the generated equation by reflexivity. Therefore the clean
build and theorem alone were not used as operational adequacy evidence.

I compared every submitted target parameter to its bound KORE symbol, frozen
rules, source program, and operational semantics:

- `_orBool_` / `Lbl'Unds'orBool'Unds'`: the K symbol is hooked to `BOOL.or`.
  Candidate `left || right` implements the complete Boolean truth table.
- `isBool` / `LblisBool`: K returns true exactly on
  `kseq(inj{Bool,KItem}(_), dotk)` and false `owise`. The candidate matches
  that exact shape and returns false on every other or longer K sequence.
- `isInt` / `LblisInt`: K returns true exactly on
  `kseq(inj{Int,KItem}(_), dotk)` and false `owise`. The candidate matches
  exactly.
- `isIntV` / the MPY-BUILTINS KORE symbol: supplied semantics returns true for
  injected Bool and Int values and false `owise`. The candidate has precisely
  those two true branches and one exhaustive false branch.

These meanings are also the operational bridge required by the source:
`isinstance(value, int)` retains both integer and Boolean values and rejects
the other modeled `Val` constructors.

I compiled independent witnesses for the complete Boolean truth table,
Bool/Int sort predicates, non-matching and multi-item K sequences, Bool and Int
`isIntV` cases, and non-integer `noneV`/`ref` cases. I also proved that
individual constant-false/constant-true mutations fail on concrete witnesses,
while the jointly convenient all-constant definitions can still satisfy the
bare equation. The test compiled successfully and printed
`(true, true, false, false)` for Bool, Int, `noneV`, and `ref`.
See `evidence/94_operational_bridge_adversarial_tests_pass.txt`. This rules out
the submitted definitions being constant, identity, hard-coded to an example,
or otherwise convenient substitutes for the frozen semantics.

## Final judgment

The classification is bijective and mathematically correct; deterministic
generation preserves the sole genuine domain obligation and exact target; the
fresh Lean proof establishes that target with no axioms; and every target
parameter implements its frozen operational meaning. I found no legitimacy
failure or residual concern.

VERDICT: PASS
LEGITIMACY: LEGIT
