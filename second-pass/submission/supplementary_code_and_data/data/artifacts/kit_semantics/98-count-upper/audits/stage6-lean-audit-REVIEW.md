# Independent Stage 3–5 audit: `98-count-upper`

## Decision

I independently audited condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`, in launcher mode `CLASSIFICATION_AND_PROOF`. I did not
accept the selected Stage 2 result, the protected Stage 3 classifications, the
recorded Stage 4 preflight, or the successful Stage 5 build as conclusions.
They were used only as read-only evidence and were checked again.

The Stage 3 classification is complete and correct. The one true domain lemma
is relevant to the frozen program proof. Stage 4 generates exactly the
corresponding, unchanged associativity obligation. Stage 5 proves that fixed
target with an operationally faithful implementation of K integer addition and
has no unaccounted trust escape.

## Producer-source authentication

I performed this gate before judging Stage 4.

The mounted producer bundle contains exactly:

- `klean_export.py`
- `klean.py`
- `source-manifest.json`

The observed producer hashes are:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07` |
| `klean.py` | `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d` |

Both values agree exactly with `source-manifest.json` and
`generator-manifest.json`. The producer-bundle tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
which agrees with `/audit-input.json`. The immutable image ID is
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`;
it agrees among the source manifest, generator manifest, and the image-key
component of the launcher-recorded producer path.

Evidence: `01_producer_authentication_inputs.txt`,
`02_producer_manifests.txt`, `04_producer_tree_and_launcher_target.txt`, and
`50_producer_authentication_assertions.txt`.

## Frozen-input and rule-inventory reconstruction

Using the trusted `/reference/tools/k_rule_inventory.py` implementation, I
reconstructed the local module closure of frozen `verification.k`. The selected
verification module and the complete local closure are both exactly
`VERIFICATION`. The byte hash of `verification.k` is
`da8f82c1ca4c4e6fbdc97e453a664af0373a7ed8fcf04d8b296d69e9271d8c45`.
The freshly computed inventory hash is
`8f5de4345417a8095331e88a362aedcf63567db12bd5e59a3e717b2b1f960037`.

The complete inventory, in source order, is:

| Lines | `source_rule_id` | Attributes | Independent class |
|---|---|---|---|
| 8 | `rule-696c1fa8e2517781ece04e7a5c6625a8196ade913ec6b9596f7c7dafd66ed095` | none | `DEFINITION` |
| 9–21 | `rule-d15a2cae4392a54744c0a40798a805f226e2ebb158b68d3c6b74f95f088ef09d` | `simplification` | `DEFINITION` |
| 24–26 | `rule-53698f5d4516a68cfad0b5d035a1d78bc9b46c118a3c2e541a4a6ef1be0683a4` | `simplification` | `DOMAIN_LEMMA` |

The protected Stage 3 file has the same inventory hash and exactly the same
three ordered identities. Both identity lists are duplicate-free and there
are no omissions, additions, or reorderings. Because each rule ID incorporates
the normalized source hash, and the inventory hash incorporates the complete
rule records, this also binds the recomputed spans, normalized text, hashes,
attributes, and module.

All 774 launcher-recorded Stage 1 regular-file hashes were recomputed:
774 files were present, with no missing, extra, or mismatched entry. The
launcher whole-workspace tree, frozen export tree, selected Stage 2 tree,
Stage 4 tree, generated tree, producer tree, discovery file, and candidate
workspace hashes also match their mounted artifacts. The launcher records a
host-side `lean_invocation` selection directory that is not one of the
supplied mounts; it was not used as audit evidence. The mounted candidate
matches the recorded `lean_workspace_sha256`.

Evidence: `05_reconstructed_rule_inventory.txt`,
`10_inventory_bijection_check.txt`, and
`30_independent_all_hash_and_target_checks.txt`.

## Independent classification judgment

### `countUpperEven(.IntSeq) => 0`

This is the base equation of a newly named mathematical summary. It does not
match a program configuration, invoke a source closure, skip source execution,
or rewrite any operational cell. It is therefore a `DEFINITION`.

### Guarded `countUpperEven(CODES)` recurrence

This is also a `DEFINITION`. On a nonempty `IntSeq`, it tests whether the
one-code-point head occurs in `AEIOU`, adds either zero or one, and recursively
summarizes the slice starting at offset two. The supplied semantics establish:

- string truthiness is nonemptiness;
- string indexing at zero returns the one-code-point head;
- string membership uses `strContains`;
- the slice `[2:]` is `buildIS` from `min(2, length)` to `length`; and
- the recursive input is strictly shorter for every nonempty sequence.

Thus the rule truthfully and exhaustively defines the requested count. It
names the postcondition summary but does not assume that source execution
returns the summary: the separate K reachability claims execute the actual
closure, assignments, while condition, indexing, membership, slicing, and
return. Its `simplification` attribute is allowed because the rule is a
definition.

### Integer-addition associativity

The rule

```k
rule (A:Int +Int B:Int) +Int C:Int
  => A +Int (B +Int C)
  [simplification]
```

is not a definition, ordinary execution rule, or previously proved derived
lemma. The frozen `prove.sh` compiles it before every proof and contains no
earlier proof of the exact rule against a module without it. It is an
unconditional mathematical fact about the K `INT.add` hook and is correctly
classified as `DOMAIN_LEMMA`.

It is materially relevant. I freshly compiled the exact frozen source and the
loop invariant proved as `#Top`. In a second fresh copy I removed only this
rule. The same loop-invariant claim exited 1 and stuck on precisely:

```text
ACC +Int head +Int countUpperEven(tail)
  = ACC +Int (head +Int countUpperEven(tail))
```

This is the associativity normalization needed to align the operational
accumulator update with the recursive summary. It is neither an unrelated
fact nor a disguised statement of the whole source postcondition. Its
`simplification` attribute is allowed because the rule is a domain lemma.

Evidence: `07_frozen_program_spec_and_relevant_semantics_index.txt`,
`08_operational_semantics_details.txt`, `09_control_and_call_semantics.txt`,
`46_k_without_assoc_loop_invariant_probe.txt`, and
`49_k_assoc_baseline_loop_invariant.txt`.

## Stage 4 deterministic generation

The required fresh call to
`tools.klean_preflight.check_generation`, with `PYTHONPATH=/reference` and the
three specified inputs, returns `PASS`. Its clean and build subprocesses both
exit 0.

The first invocation exposed an audit-container PID-namespace issue: Lean
looked up `/proc/<namespace-pid>/exe`, while the mounted `/proc` belonged to a
different namespace. A diagnostic interposer showed the failed lookup
directly. I reran with a narrowly scoped shim that only retries a failed
`/proc/<digits>/exe` lookup as `/proc/self/exe`. This changed no Lean source,
generated source, target, or proof term; it only restored executable
self-location. The shim source and both the failed and successful runs are
preserved.

Important recomputed Stage 4 bindings are:

| Item | SHA-256 |
|---|---|
| Frozen Stage 1 export | `e2e1e1781b634d66288f0f4cc28474ba866d290c6376b5e6fe1aa7270bf08d93` |
| Stage 3 discovery file | `22eb090fb9b6d7587ac651f35dd1d783be25640acbd318a7a217547f6fed89a1` |
| Generated tree | `8fd7f84b91c613be8d938281dec6575109502fb5e73552d3c216b6c09c62cb23` |
| Obligation map | `1e1d481edbda3e54913e619af92afe5266b83814c7dff6e185e3243420d1344d` |
| Trust inventory | `c0a1916343f14c47fa5e34444e229f9eeab7f46631864047af60bbe847d7bbff` |

The independent domain set contains exactly one rule. The input manifest,
obligation-map source list, obligation list, generator count, export count,
and target parameter binding all contain exactly that same rule, once and in
the same position. The generated conjunct is:

```lean
∀ (C : SortInt) (B : SortInt) (A : SortInt),
  «_+Int_» («_+Int_» A B) C = «_+Int_» A («_+Int_» B C)
```

This is the exact unguarded K associativity rule. Reversing the order in which
universally quantified variable names are introduced does not alter it.
`SortInt` is definitionally Lean `Int`, so the domain is inhabited and the
conjunct is not vacuous. There is no weakened premise or conclusion.

The fixed target extracted from the generated source agrees byte-for-byte and
field-for-field with `generator-manifest.json` and `/audit-input.json`:

- declaration:
  `Klean98CountUpper.Lemmas.targetStatement`;
- file: `Klean98CountUpper/Lemmas.lean`;
- definition hash:
  `0ca8cccf1ec33bcf55bf657256a1364f49fa2b6ba7c9c0ca1c94059ed9b94ce0`;
- statement:
  `Klean98CountUpper.Lemmas.targetStatement «_+Int_»`;
- statement hash:
  `04052eeb707dfe90546c4c2bef53927adc78d2dfac6d380e44717f8a74da75f9`;
- parameter binding hash:
  `0d30130435d464e3ce13cbaa675d4c1cc0ec6cd895227779ff29e869332e2417`;
- parameter KORE symbol: `Lbl'UndsPlus'Int'Unds'`; and
- parameter source rule: the sole associativity rule above.

The frozen compiled KORE declares that exact KORE symbol as a hooked, total
function with hook `INT.add`. Therefore the generated parameter is neither
irrelevant nor detached from the source rule. The selected status is correctly
`OK` with one obligation, not `KLEAN_NO_OBLIGATIONS`.

Evidence: `27_fresh_klean_preflight_success.txt`,
`28_stage4_obligation_target_and_trust_sources.txt`,
`30_independent_all_hash_and_target_checks.txt`,
`31_kore_integer_addition_binding.txt`, and
`32_independent_obligation_bijection_and_math_check.txt`.

## Stage 5 Lean proof

I created `/tmp/audit-work/stage5-fresh-audit-98`, copied the candidate source
files into it, and copied the immutable generated project as `Base`. Before
building, the fresh `Base` tree hash was exactly
`8fd7f84b91c613be8d938281dec6575109502fb5e73552d3c216b6c09c62cb23`.
The fresh `Proof.lean` hash was exactly the mounted candidate hash
`62b52208adfe334665b8d0707eb472af9aeec03ac81eb982cae6d8e4310baecb`.

I then ran both required commands:

- `lake clean`: exit 0;
- `lake build`: exit 0, ending with `Build completed successfully.`

Because the fresh project did not copy the candidate's old `.lake` directory,
the result does not rely on stale compiled objects.

The candidate source:

- contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`;
- defines the one required target parameter exactly once;
- does not declare or shadow `targetStatement`;
- leaves the generated target file byte-identical to Stage 4; and
- states `Proof.final` as exactly
  `Klean98CountUpper.Lemmas.targetStatement «_+Int_»`.

The exact Lean printout is:

```text
def Proof.«_+Int_» : SortInt → SortInt → SortInt :=
fun x0 x1 => x0 + x1
theorem Proof.final : Klean98CountUpper.Lemmas.targetStatement Proof.«_+Int_» :=
fun C B A => Int.add_assoc A B C
'Proof.final' depends on axioms: [propext]
```

The trusted Stage 5 mechanical gate independently passes. `propext` is one of
the gate's three explicitly recognized Lean foundational axioms
(`Classical.choice`, `propext`, and `Quot.sound`). None of the 41 generated
allowlisted collection-hook axioms occurs in the dependency set. `sorryAx` is
absent, and the set of unexpected axioms is empty.

Evidence: `35_fresh_stage5_project_preparation.txt`,
`36_fresh_lake_clean_complete.txt`, `37_fresh_lake_build_complete.txt`,
`38_print_proof_final_and_axioms_exact.txt`,
`39_trusted_stage5_mechanical_gate.txt`, and
`43_candidate_target_shadow_token_and_axiom_reconciliation.txt`.

## Operational bridge for `«_+Int_»`

The target proposition alone characterizes associativity, not integer
addition. I explicitly tested this weakness: constant zero, left projection,
and right projection all prove the generated target by reflexivity. Thus a
clean proof would not by itself validate the parameter bridge.

The actual candidate passes the independent bridge check:

1. The manifest binds `«_+Int_»` to
   `Lbl'UndsPlus'Int'Unds'` and to the exact frozen associativity rule.
2. Frozen KORE binds that symbol to total hook `INT.add`.
3. The supplied operational semantics routes integer `+` and the
   integer-plus-Boolean accumulator update to `+Int`.
4. The source solution's `count += remaining[0] in "AEIOU"` therefore adds
   zero or one using that same K integer operation.
5. Generated `SortInt` is Lean `Int`.
6. The candidate definition is definitionally `fun x0 x1 => x0 + x1`, i.e.
   Lean integer addition, with no constant, projection, identity, table,
   conditional, or hard-coded special case.

Adversarial evaluations produced:

```text
(-7) + 5 = -2
0 + 0 = 0
12345678901234567890 + (-9876543210987654321)
  = 2469135690246913569
```

These exercise negative, zero, and beyond-machine-word integers. As a
counterfactual, subtraction failed the target with the expected residual that
`(A - B) - C` is not definitionally `A - (B - C)`. The convenient associative
countermodels demonstrate that the audit did not infer bridge fidelity merely
from target provability; fidelity comes from the exact candidate definition
and the `INT.add` binding.

Evidence: `31_kore_integer_addition_binding.txt`,
`38_print_proof_final_and_axioms_exact.txt`,
`41_operational_bridge_examples_and_convenient_countermodels_success.txt`,
and `42_nonassociative_counterfactual_rejected.txt`.

## Evidence integrity and conclusion

All audit-created probes, exact command transcripts, exit codes, and outputs
are under `/audit-output/evidence/`. In particular, the PID-namespace shim,
axiom query, operational countermodel probes, rejected mutation, candidate
snapshot, and the exact K source mutation are preserved there alongside their
hashes and the one-rule diff.

No Stage 3 classification defect, Stage 4 provenance or obligation defect,
target drift, Lean trust escape, proof-identity defect, or operational-bridge
failure was found.

VERDICT: PASS
LEGITIMACY: LEGIT
