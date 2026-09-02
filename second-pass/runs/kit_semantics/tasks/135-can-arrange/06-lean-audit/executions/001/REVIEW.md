# Independent audit: HumanEval 135 `can-arrange`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Result

The protected Stage 3 classification is structurally complete and
mathematically correct: the local verification closure has 22 definitions and
one relevant domain lemma. Deterministic Stage 4 preserves the selected rule,
guard, equation, and target hashes, and the trusted preflight passes.

The overall result is nevertheless not legitimate for two independent reasons:

1. Stage 4's generated `SortStr` is empty even though the frozen K semantics
   has the inhabited constructor `str(IntSeq)` and the sole domain lemma covers
   string/string comparisons. Thus the Lean target cannot express one of the
   ten satisfiable guarded cases of the frozen rule.
2. The Stage 5 definition of the `applyCmp` target parameter does not implement
   the frozen operational symbol. It returns `false` for every operator other
   than `>=`, and for `>=` it simply calls the candidate's `orderGe`—the exact
   right-hand side of the theorem. This is circular. The theorem still builds
   after replacing `orderGe` by constant `false`, and it also builds after
   replacing `orderablePair` by constant `false`.

The clean build and empty axiom list are genuine, but they prove only the fixed
equation under convenient candidate interpretations, not the frozen
operational bridge.

## Input integrity and producer provenance

The launcher mode in `/audit-input.json` and `AUDIT_MODE` is
`CLASSIFICATION_AND_PROOF`. The immutable producer provenance gate passed
before Stage 4 was judged:

| Item | Observed SHA-256 | Required value |
|---|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` | same in `generator-manifest.json` and `source-manifest.json` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` | same in both manifests |
| Generator image | `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7` | same in both manifests and the launcher-resolved producer path |
| Producer bundle, pipeline tree hash | `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e` | same in `/audit-input.json` |

The similarly named Klean `tree_digest` is a different hashing algorithm; the
launcher records the trusted pipeline `sha256_tree` for the producer bundle.
Using that prescribed algorithm gives the exact launcher value.

All other mounted launcher hashes were recomputed with their corresponding
trusted algorithms. The Stage 1 workspace, Stage 2 audit, Stage 3 manifest,
Stage 4 generation, generated project, producer bundle, and Stage 5 workspace
all match. The 835-entry Stage 1 source-hash map has no missing, extra, or
mismatched file. See
[recorded hash verification](/audit-output/evidence/38_recorded_hash_verification.log)
and [producer provenance](/audit-output/evidence/02_producer_manifest_contents.log).
There is no producer-source infrastructure `AUDIT_ERROR`.

## Stage 3 inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. It selected `VERIFICATION` from the final `kompile`
command in `prove.sh` and reconstructed its local source closure in source
order:

1. `VERIFICATION-BASE`
2. `VERIFICATION`

The frozen `verification.k` SHA-256 is
`e67f2b057b77184651c67f8fc12a9646e58483fd881ba0ec8ced3df979e493f3`.
The reconstruction contains 23 rules and has canonical inventory hash
`f5b69f74b12f0505988375faf85089ef4d83ccca0e2946d2e4e09f482da52564`.

For every rule, the trusted inventory independently reconstructed its module,
start/end line, comment-insensitive normalized text hash, and
`source_rule_id = "rule-" + normalized_sha256`. The ordered identities match
`lemma-discovery.json` bijectively: no omission, duplicate, extra entry,
reordering, changed span, or changed hash. Full reconstructed records are in
[the canonical inventory](/audit-output/evidence/07_reconstructed_inventory.json.log);
the independent contract comparison is in
[Stage 3 validation](/audit-output/evidence/08_discovery_contract_validation.log).

### Independent classification

The classification was redone from the source bodies and fixed MPY dispatch,
not from the Stage 3 rationales.

| Source lines | Rules (normalized-hash prefixes, in inventory order) | Classification and reason |
|---|---|---|
| 7–8 | `f447e6c1…` (`isNumericVal`) | `DEFINITION`: names a total sort predicate. |
| 11–13 | `c196375d…` (`orderablePair`) | `DEFINITION`: names the numeric-pair/string-pair proof domain. |
| 20–32 | `8bbe4232…`, `e853c61f…`, `aff0eb37…`, `213846a9…` | `DEFINITION`: the complete empty/zero/positive/negative recurrence for `scanDefined`. |
| 38–68 | `fa5cd7c4…`, `40c2c4ba…`, `b4535bb0…`, `a4635f5f…`, `0f84f0ef…`, `e54bea80…`, `374dd39e…`, `cfe48f98…`, `9629b5e3…`, `29e2cbda…`, `fe239a33…` | `DEFINITION`: ten disjoint numeric/string equations plus the guarded complement totalize the named `orderGe` summary. |
| 76–98 | `f55e5b0e…`, `9a868dd4…`, `daae1cb9…`, `b84c57cd…`, `2cfe1b33…` | `DEFINITION`: the complete structural recurrence for the returned-index summary `arrangeSeq`. |
| 106–108 | `rule-2fd1883e1dbbdfd9717b1321447ac996a4962a56a877371e6e1bee92b5b19050` | `DOMAIN_LEMMA`: it equates the pre-existing operational observation `applyCmp(">=", V, W)` with the new `orderGe` summary under the proof-domain guard. |

There are no ordinary execution rules in this local proof-module closure and
no valid `PROVED_DERIVED_LEMMA`. Stage 1 first proves ten statically typed
claims against `VERIFICATION-BASE`, but it does not first prove the exact
guarded polymorphic rule at lines 106–108 and then use that exact rule later.
Consequently the final rule cannot be promoted to
`PROVED_DERIVED_LEMMA`. It is relevant: the source loop performs exactly this
`>=` observation, and the result branch determines the returned index.

All 21 `[simplification]` rules are either definitions (20) or the sole domain
lemma (one), as required.

## Stage 4 structural generation audit

The exact requested call to `tools.klean_preflight.check_generation` was rerun
with `PYTHONPATH=/reference`, the frozen K workspace, the protected Stage 3
manifest, the selected generation, and the pinned toolchain lock.

The first invocation exposed an executor-specific PID namespace issue: Lean
4.22 uses `/proc/<getpid()>/exe`, while this executor's local PID is absent
from the externally mounted `/proc`. A compiled probe reproduced `ENOENT`.
A narrow preload shim redirected only such executable-path reads to
`/proc/self/exe`; with it, Lean reported version 4.22.0 and pinned commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`. The shim source and hash are
recorded in
[the environment workaround evidence](/audit-output/evidence/19_lean_pid_namespace_workaround.log).
It does not alter source files, elaboration, or proof checking.

The rerun returned:

- status `PASS`;
- Stage 1 tree
  `1b3dd0a9969538031ffe5ae120ffe22df07388f253b5e6234def725583cb4dbf`;
- Stage 3 manifest
  `aafc91d063f2bf10a1025b189e023aa40814f6c46eaa293b97bc1e6e67cb1beb`;
- generated tree
  `3385ac6364d0b8e9436c7956e6dc7dec10fcb838ccb0c447cd8075cf70622641`;
- one obligation and 44 generated trust declarations;
- internal `lake clean` exit 0 and `lake build` exit 0.

The complete returned document is
[the rerun preflight evidence](/audit-output/evidence/20_rerun_check_generation_shimmed.log).

### Source-rule/obligation bijection and fixed target

Independent inspection confirms:

- Stage 3 has exactly one true domain lemma.
- `input-manifest.json` has exactly that one `source_rules` entry.
- `obligation-map.json` has exactly one source rule and one obligation.
- The source ID, lines 106–108, normalized hash, inventory hash, and discovery
  hash agree in all locations.
- The Lean conjunct is exactly
  `∀ W V, orderablePair V W = true → applyCmp ">=" V W = orderGe V W`.
  Reversing the binder order from the source metavariable presentation changes
  no domain or meaning.
- There is no duplicate, missing conjunct, extra conjunct, weakened guard,
  changed operator, or changed equality.
- `obligation-map.json` hashes to
  `b810ff3614a4b526554d9bb44e08fe759df914b1ed3ddbc557acf857d9be45ae`.
- The fixed target definition hash is
  `29c9d56b6c41f072e1ffbf7a268135fe25c7df1e7221ad70d5f8d0796d516fc3`.
- Its applied statement hash is
  `f6546a0c884ecb415a7b6dffde624a2418ff099073c317144ff6bc9b0d5340d0`.

The generator manifest, launcher target, trusted parser result, and actual
`Lemmas.lean` agree exactly; see
[target identity](/audit-output/evidence/23_target_identity.log).
Because the independently classified domain set is nonempty, status `PASS`
with a target and Stage 5 candidate is structurally appropriate; this is not a
`KLEAN_NO_OBLIGATIONS` case.

### Mathematical Stage 4 weakening

The structural bijection does not preserve the full value domain. Frozen
`core.k` declares the inhabited constructor:

```k
syntax Str ::= str(IntSeq)
```

`orderablePair` admits string/string pairs, frozen `orderGe` has its
string/string equation, and fixed `str.k` has the corresponding operational
`applyCmp(">=", str(A), str(B))` rule. In contrast, generated `Sorts.lean`
contains:

```lean
inductive SortStr : Type
```

with no constructor. `SortVal.inj_SortStr` therefore has no realizable
argument. A fresh Lean check proves `SortStr → False` by `nomatch`; see
[the empty-domain check](/audit-output/evidence/35_generated_string_domain_empty.log)
and [the frozen/generated source comparison](/audit-output/evidence/36_string_domain_omission_sources.log).

Thus the target's surface conjunct is exact, but its generated carrier omits a
satisfiable source-rule case. This is a material weakening of the frozen
program's guarded domain, not merely a candidate proof issue.

## Stage 5 proof audit

### Fresh build and immutable target

A fresh project was created at `/tmp/audit-work/lean-proof-audit`. Only the
candidate's `Proof.lean`, `lakefile.lean`, and `lean-toolchain` were copied;
the exact selected generated project was copied separately as `Base`. Before
building, `Base` had the required generated tree hash
`3385ac6364d0b8e9436c7956e6dc7dec10fcb838ccb0c447cd8075cf70622641`.

Both required commands succeeded:

```text
LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake clean
exit_code=0

LD_PRELOAD=/tmp/audit-work/lean_proc_exe_shim.so lake build
Build completed successfully.
exit_code=0
```

Complete outputs are in
[lake clean](/audit-output/evidence/28_lake_clean.log) and
[lake build](/audit-output/evidence/29_lake_build.log).

The built Base target file is byte-identical to the selected generated file,
and the declaration/definition/statement hashes remain exact. The candidate
does not redefine or shadow `Klean135CanArrange.Lemmas.targetStatement`.
Candidate-owned Lean sources contain no `sorry`, `admit`, `unsafe`, `axiom`,
or `opaque`, and the trusted declaration scanner finds no candidate trust
declaration. See
[candidate target/trust checks](/audit-output/evidence/31_candidate_target_and_trust_static.log).

### Proof identity and axiom accounting

Lean prints the exact type:

```lean
Proof.final :
  Klean135CanArrange.Lemmas.targetStatement
    Proof.«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
    Proof.«orderGe(_,_)_VERIFICATION-BASE_Bool_Val_Val»
    Proof.«orderablePair(_,_)_VERIFICATION-BASE_Bool_Val_Val»
```

It is the fixed target instantiated by the three required candidate
definitions, not a duplicate theorem or a separately weakened statement.
Exact `#print` output is in
[the final theorem evidence](/audit-output/evidence/30_print_axioms_and_final.log).

`#print axioms Proof.final` reports:

```text
'Proof.final' does not depend on any axioms
```

The dependency set is therefore empty. It is a subset of the Stage 4 trust
inventory without using any of its 44 allowlisted generated axioms. In
particular there is no `sorryAx` and no recorded or unrecorded proof trust
escape.

### Operational meaning of every target parameter

The exact candidate definitions and inferred types are recorded in
[parameter printing](/audit-output/evidence/39_print_candidate_parameters.log).

#### `orderablePair`

For representable values, the candidate implements numeric×numeric and
string×string exactly in the source shape, returning `false` for other pairs.
Adversarial evaluation returns `true` for an Int/Float pair and `false` for a
None/None pair. However, because generated `SortStr` is empty, the required
string/string part is unreachable and cannot implement the inhabited frozen K
case. Replacing the entire guard by constant `false` still cleanly builds
`Proof.final`; see
[the guard mutation](/audit-output/evidence/34_counterfactual_guard_constant_false_build.log).
This confirms that the Lean theorem alone does not establish guard fidelity.

#### `orderGe`

On the generated numeric inhabitants, the candidate's nine numeric branches
track frozen lines 38–62: Int/Bool comparisons use `boolAsInt`, Float/Float
uses `not floatLt`, and mixed comparisons use `not ltIF`/`not ltFI`. Tested
ordinary, large-integer, infinity, and NaN cases follow those frozen K
equations; the exact eight outputs are in
[numeric adversarial evaluations](/audit-output/evidence/40_numeric_bridge_adversarial_evaluations.log).
The string equation at frozen lines 63–65 is not implemented; the candidate
uses `nomatch` because Stage 4 made `SortStr` empty.

More decisively, replacing the entire `orderGe` function by constant `false`
while keeping the nonvacuous numeric guard unchanged still yields:

```text
Build completed successfully.
exit_code=0
```

See
[the `orderGe` mutation](/audit-output/evidence/33_counterfactual_orderge_constant_false_build.log).
The final proof is therefore insensitive to the mathematical meaning of its
right-hand-side summary.

#### `applyCmp`

This parameter fails the operational bridge check. Frozen `applyCmp` is the
MPY comparison-dispatch symbol. Even on integers, fixed `int.k` defines
independent `<`, `<=`, `>`, `>=`, `==`, and `!=` cases. Other fixed files add
Bool, Float, mixed numeric, string, identity, membership, list, tuple, set, and
dict cases.

The candidate instead defines:

```lean
if operator = ">=" then
  if orderablePair left right then orderGe left right else false
else
  false
```

Concrete counterexamples are:

| Input | Frozen operational result | Candidate result |
|---|---:|---:|
| `applyCmp("<", 1, 2)` | `true` by `int.k` | `false` |
| `applyCmp("==", 3, 3)` | `true` by `int.k` | `false` |
| `applyCmp(">", 3, 2)` | `true` by `int.k` | `false` |

The candidate outputs are recorded in
[adversarial evaluations](/audit-output/evidence/32_candidate_adversarial_evaluations.log).

Even restricted to the target's `>=` guard, the definition is not an
independent implementation of operational dispatch: it assumes the sought
equation by directly returning the candidate's `orderGe`. This is exactly why
arbitrarily falsifying `orderGe` leaves `Proof.final` provable. The clean
theorem is an equality by shared definition, not a proof that fixed MPY
execution has the summary's meaning.

Under the required operational-bridge criterion, this convenient and circular
definition is a mandatory proof failure.

## Evidence index

Raw commands and complete results are under `/audit-output/evidence/`.
The most relevant files are:

- [launcher and mounted inputs](/audit-output/evidence/00_launcher_and_inputs.log)
- [producer hashes](/audit-output/evidence/01_producer_provenance.log)
- [canonical rule inventory](/audit-output/evidence/07_reconstructed_inventory.json.log)
- [Stage 3 bijection validation](/audit-output/evidence/08_discovery_contract_validation.log)
- [frozen program and semantics](/audit-output/evidence/09_frozen_sources_and_semantics.log)
- [rerun Stage 4 preflight](/audit-output/evidence/20_rerun_check_generation_shimmed.log)
- [Stage 4 manifests and obligation map](/audit-output/evidence/21_stage4_manifests_and_map.log)
- [fresh Stage 5 project](/audit-output/evidence/27_fresh_lean_project.log)
- [clean build](/audit-output/evidence/29_lake_build.log)
- [exact theorem and axioms](/audit-output/evidence/30_print_axioms_and_final.log)
- [parameter counterexamples](/audit-output/evidence/32_candidate_adversarial_evaluations.log)
- [counterfactual builds](/audit-output/evidence/33_counterfactual_orderge_constant_false_build.log) and [guard mutation](/audit-output/evidence/34_counterfactual_guard_constant_false_build.log)
- [all recorded hash checks](/audit-output/evidence/38_recorded_hash_verification.log)

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
