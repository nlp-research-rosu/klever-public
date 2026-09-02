# Independent audit: HumanEval `51-remove-vowels`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

## Result

The protected Stage 3 classification is complete and mathematically correct.
The selected Stage 4 generation is authenticated, structurally exact, and
contains the one obligation required by the independently identified domain
lemma. The Stage 5 candidate clean-builds from a fresh copy, proves exactly the
fixed generated theorem, has an acceptable axiom report, and supplies honest
operational definitions for both target parameters.

I did not rely on the earlier Stage 2 verdict, prior reviews, logs, comments, or
candidate instructions.

## Input and provenance integrity

`AUDIT_MODE` and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF`. The signed resolution envelope recomputes to
`13d3339302be981130ccdf4fe2077e1652248f040d417974fdaf56435dc6a045`.
All 35 frozen Stage 1 source paths and hashes match exactly.

Every mounted resolution object recomputes to its recorded hash:

- Stage 1 workspace tree:
  `a6af721cd4f96f6fd53edcff3816bda999b9a54b6fb1d6bc3132b5ac88028226`
- Stage 1 deterministic-export tree:
  `a9655562b67df3ca69f35ec08efcf74e31a5e0c8734e9bdca289c220ca689c4f`
- Stage 2 selected audit:
  `9c1c0fc553a9b2cd7f198d7cbc7d1e524ea806d2c145a1368d388f97aaee1d6c`
- Stage 3 manifest:
  `c3a1bfce6e3ebb217514c8c4369511f42ea7d9898ba63e3724ac9211d9b9f978`
- Stage 4 generation:
  `6f58f078bd997330915f31d95c4da3b2ae4a6ad01c97832c90cc43b9adb3434d`
- Generated project:
  `a6b730bf4113ad5eb4ec163e920c9517488ee297ebefc837da5648aeec193418`
- Producer-source bundle:
  `55e6319f2271365637d561f055caa2f6187aa98b0216ec39cc79e0cce33b867c`
- Stage 5 workspace:
  `8b4203bfa6aa081e69bbb8a6bc15e1d6cadff08e05f57a881fc461b9e44449de`

The audit input records a separate Stage 5 invocation-evidence hash, but no
invocation tree is mounted; `/candidate` is the separately hashed workspace
and matches its recorded workspace hash. All hashes with mounted
counterparts, all Stage 4 sidecar hashes, the Stage 1 per-file map, and the
signed audit-input digest were independently recomputed.

### Stage 4 producer authentication

This gate passed before judging generated content:

- `klean_export.py`:
  `0c18ea7997ddd34d3cabbeb0f271e17eb8a01cd03342319facf749ba92df18f0`
- `klean.py`:
  `af70e08a1c91156f9fb5a2492647a2fda2b5a1040cbbc0180e6f03816ddf5ef1`

Those exact values agree with `source-manifest.json` and
`generator-manifest.json`. Both manifests identify
`sha256:dc996159ebb6df707cd5366ab83c500be5bbd2b842eda971e55ade57e5dda000`,
which also equals the immutable bundle key recorded by `/audit-input.json`.
The bundle contains exactly the two producer files and its source manifest.
There is no producer-source infrastructure error.

## Stage 3 inventory reconstruction

I ran the trusted canonical inventory code on the frozen
`/reference/k-proof`. `prove.sh` selects `VERIFICATION`, and the only local
module in its `verification.k` closure is `VERIFICATION`.

The reconstruction found exactly 10 rules. For every rule it recomputed the
source span, normalized SHA-256, and `source_rule_id`. The canonical ordered
inventory hash is:

`c4fd0605482dfebcb250ed7885603895e25bb645f5f8ad33e615302289632c82`

The protected manifest also contains exactly 10 unique IDs in the same order.
There are no omissions, additions, duplicates, reordered identities, changed
spans, or changed hashes. The trusted Stage 3 boundary validator passes.

## Independent classification judgment

The independent totals are 9 `DEFINITION`, 0 `OPERATIONAL_RULE`, 0
`PROVED_DERIVED_LEMMA`, and 1 `DOMAIN_LEMMA`, exactly matching Stage 3.

The nine definitions are:

- `vowelCodes` at lines 7–9: a named macro for the ten vowel codes.
- `isVowelCode` at lines 12–16: a named total Boolean predicate.
- `removeVowelCodesAcc` at lines 26–34: its base, vowel, and non-vowel
  recurrence clauses.
- `removeVowelCodes` at lines 37–38: the initialized summary.
- `removeVowelsLoopBody`, `removeVowelsBody`, and `removeVowelsProgram` at
  lines 41–56: named macros for the exact loop, function, and module AST.

Each therefore defines a summary, recurrence, or macro. None is an ordinary
execution/observation rule, and no exact rule was first proved in a module
omitting it and only later used, so there is no valid
`PROVED_DERIVED_LEMMA`.

The sole domain lemma is:

`rule-94d2fdc35d3fdf3c396f6195fb860162747c2dc403f48fae46276855a3075f93`
(lines 21–23):

```text
strContains(iCons(C, .IntSeq), vowelCodes) => isVowelCode(C)
```

It does not define either side: `strContains` already belongs to supplied
`MPY-STR`, and `isVowelCode` is already defined above it. Stage 1 did not prove
this exact rule against a module omitting it. It is therefore a
`DOMAIN_LEMMA`, not a definition, operational rule, or proved derived lemma.

The lemma is relevant. Source line 5 performs
`char not in "aeiouAEIOU"`, which supplied semantics lowers through
`applyCmp("not in", ...)` to `notBool strContains(...)`. The loop claims split
on `isVowelCode(C)`. The lemma is precisely the bridge between those forms.

It is also true over every K `Int`: supplied `strPrefix` and `strContains`
scan for the singleton sequence `[C]` in the fixed sequence
`[97,101,105,111,117,65,69,73,79,85]`; that succeeds exactly for the ten
equalities defining `isVowelCode(C)`.

No inventoried rule has a `simplification` attribute. The domain lemma has
only `priority(40)`, so the simplification-class restriction is satisfied.

## Stage 4 deterministic generation

I reran:

```text
tools.klean_preflight.check_generation(
  /reference/k-proof,
  /reference/lemma-discovery.json,
  /reference/klean-generation,
  toolchain_lock=/reference/klean-toolchain.lock.json)
```

with `PYTHONPATH=/reference`. It returned `PASS`, clean-built its fresh
generated-project copy, found one obligation, zero designated sorries, and 47
generated trust declarations. Its returned JSON exactly equals the
`stage4_preflight` object in `/audit-input.json`, including build-output
hashes.

The first shell attempts exposed a sandbox-only toolchain issue: Lean 4.22
reads `/proc/<current-pid>/exe`, while this sandbox exposes only
`/proc/self/exe`. A recorded, narrowly scoped compatibility shim redirects
only that exact self-executable `readlink`. Under it, Lean reports locked
commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`; no proof, source, theorem, or
kernel behavior is changed.

### Obligation bijection and mathematical content

The independent domain set has one ID, and `obligation-map.json` has one
unique obligation with that same ID and order. Its source span is exactly
21–23; normalized rule hash, inventory hash, discovery hash, and conjunct hash
all recompute. `input-manifest.json`, `obligation-map.json`, and
`generator-manifest.json` agree. The obligation-map file hash is
`35de87600a058ff68ef784f0e780fe53881e171fadbfb50ab104ea965fd57304`.

The generated conjunct is exactly:

```text
∀ C : SortInt,
  strContains([C], [97,101,105,111,117,65,69,73,79,85])
    = isVowelCode(C)
```

This is the frozen domain rule after expanding only `vowelCodes`. It retains
the universal integer domain and both sides of the equality. It is relevant,
not weakened, not duplicated, and not a tautological conjunct. Mutating either
bridge alone is rejected at `C = 97`.

The parameterized equation would admit coordinated dishonest definitions
(for example, making both functions constantly false). That does not make the
source obligation vacuous, but it makes the required Stage 5
operational-bridge audit essential. The submitted definitions pass that audit
below.

### Fixed target identity

The generated project contains exactly one target:

- Declaration: `Klean51RemoveVowels.Lemmas.targetStatement`
- File: `Klean51RemoveVowels/Lemmas.lean`
- Definition SHA-256:
  `7ce1bdc42e243b03a3397edba12b4e7765eaae268c82dc12e69d38d5436e4ec1`
- Applied statement SHA-256:
  `cbfee13241725618eb3cb2b6a06c828930018b582cb2e45b576deb8cff734e4c`

The independently extracted definition equals the deterministic conjunction
reconstructed from `obligation-map.json`. The declaration, definition hash,
statement, statement hash, parameter types, KORE symbols, source-rule
bindings, and binding hashes exactly match `generator-manifest.json` and
`/audit-input.json`.

## Stage 5 Lean proof

I created fresh workspace
`/tmp/audit-work/stage5-proof-audit.ya9zyF`, copied the candidate proof files,
and copied the authenticated generated project into it as `Base`. Before and
after the build, `Base` hashes to the recorded generated-tree hash
`a6b730bf4113ad5eb4ec163e920c9517488ee297ebefc837da5648aeec193418`.

The required commands both succeeded:

```text
lake clean
# exit 0

lake build
# Built Prelude, Sorts, Inj, Lemmas, and Proof
# Build completed successfully.
# exit 0
```

The candidate defines each exact trust binding once. Outside generated `Base`,
there are zero `sorry`, `admit`, `unsafe`, `axiom`, or `opaque` tokens. It
declares no `targetStatement` and no generated target namespace, so it neither
changes nor shadows the target.

`Proof.final` has exactly the fixed applied target type:

```text
Klean51RemoveVowels.Lemmas.targetStatement
  Proof.«isVowelCode(_)_VERIFICATION_Bool_Int»
  Proof.«strContains(_,_)_MPY-STR_Bool_IntSeq_IntSeq»
```

It is not a duplicate or weakened theorem.

### Axiom accounting

The exact Lean result is:

```text
'Proof.final' depends on axioms: [propext, Quot.sound]
```

There is no `sorryAx`. `propext` and `Quot.sound` are the standard Lean
foundational dependencies explicitly permitted by the trusted final gate.
Neither is a candidate declaration. None of the 47 generated trust-boundary
declarations listed by `trust-inventory.json` is used by `Proof.final`, and
there is no unrecorded proof trust escape. The trusted independent final
mechanical gate also returns `PASS`.

### Operational-bridge audit

Both `target.parameters` entries are bound to
`rule-94d2fdc35d3fdf3c396f6195fb860162747c2dc403f48fae46276855a3075f93`,
the exact domain rule that relates the two symbols. Their binding hashes are
respectively
`b940eba695e685f9d3a0c2d3f584346d3a3e77c1c5b74a3ef6191f39896a365a`
and
`dd68759ee498f0f23d41f169d1c119b1ab6b9c339774efbcb2c97d888f3856de`.

The first parameter is bound to KORE symbol
`LblisVowelCode'LParUndsRParUnds'VERIFICATION'Unds'Bool'Unds'Int`. Its
exact candidate `def` is at `Proof.lean` lines 6–8. It returns true for exactly
`65,69,73,79,85,97,101,105,111,117`. This is the exact total meaning of frozen
`verification.k` lines 12–16 over Lean `Int`, which is the generated
`SortInt`. It is neither constant nor hard-coded to only the theorem witness;
it implements the full predicate.

The second parameter is bound to KORE symbol
`LblstrContains'LParUndsCommUndsRParUnds'MPY-STR'Unds'Bool'Unds'IntSeq'Unds'IntSeq`.
Its exact candidate `def` is at `Proof.lean` lines 19–28, supported by the
private prefix definition at lines 10–16. The candidate `strPrefix` has the
same three constructor cases as supplied `semantics/str.k` lines 32–35. Its
`strContains` returns that prefix result for an empty haystack and, for a
nonempty haystack, returns true on a matching prefix or recursively searches
the tail. This is exactly the three guarded supplied rules at lines 37–41,
including empty-needle, empty-haystack, interior-match, and no-match behavior.
Recursion strictly decreases the haystack.

This full implementation is stronger than a convenient special case for the
fixed vowel list and preserves the operational meaning used by source
`char not in "aeiouAEIOU"`.

Machine-checked adversarial evaluations produced:

```text
isVowel at [-1,64,65,66,97,117,118,1000000]
  = [false,false,true,false,true,true,false,false]

strContains for empty, boundary, interior, absent, ordered, reversed,
and overlong cases
  = [true,true,true,true,false,true,false,false]
```

Counterfactual checks prove that dropping code 117 changes the result and that
a prefix-only substring implementation misses the interior code 101.
Changing either bridge alone to constant false makes the target false at
`C = 97`. A coordinated-constant pair can satisfy the equation, but the actual
candidate definitions are the full frozen operations, so that adversarial
escape is not present.

## Evidence

Raw commands, complete build output, reconstructed inventories, hash matrices,
the exact axiom report, audit sources, and bridge tests are under
`/audit-output/evidence/`. The principal files are:

- `04_reconstructed_inventory.json`
- `05_inventory_bijection_check.json`
- `07_stage4_producer_provenance_verdict.json`
- `22_rerun_check_generation_pass.json`
- `29_lake_clean_complete.txt`
- `30_lake_build_complete.txt`
- `31_print_axioms_proof_final_exact.txt`
- `34_axiom_reconciliation.json`
- `35_target_identity_and_candidate_integrity.json`
- `39_trusted_final_mechanical_gate.json`
- `40_independent_obligation_bijection.json`
- `41_independent_classification.md`
- `42_comprehensive_recorded_hash_matrix.json`
- `44_operational_bridge_and_nonvacuity_tests_pass.txt`

VERDICT: PASS
LEGITIMACY: LEGIT
