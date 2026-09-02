# Independent audit: HumanEval `35-max-element`, `kit-semantics`

## Result

The Stage 3 classification and deterministic Stage 4 generation pass the
independent checks. The Stage 5 Lean project clean-builds and proves exactly the
fixed generated target without proof holes or candidate-created axioms.

The proof is nevertheless not legitimate. Its definitions of both
`maxFOpaque` and K's `maxFloat` parameter use a Float helper with the wrong NaN
behavior. The supplied K 7.1.293 semantics returns the non-NaN operand from
`maxFloat(NaN, 1.0)` and `maxFloat(1.0, NaN)`; the candidate returns NaN in
both cases. These are represented Float inputs covered by the frozen Stage 1
claims. Moreover, replacing both parameter definitions with the constant
function `fun _ _ => 0.0` still proves `Proof.final`. The Lean theorem therefore
establishes only that two conveniently identical definitions are equal, not
that either implements the frozen operational symbol.

The recorded mode in both `AUDIT_MODE` and `/audit-input.json` was
`CLASSIFICATION_AND_PROOF`.

## Input and producer integrity

Before judging generation, I hashed the exact mounted producer sources:

| Producer input | Recomputed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

Both values match `source-manifest.json` and `generator-manifest.json`. Those
manifests record generator image
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`;
the same image identifier is the terminal component of the immutable producer
source path recorded in `/audit-input.json`. The producer-source tree digest is
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`,
also exactly matching the audit input.

Every mounted tree/file digest recorded in `/audit-input.json` was recomputed
with its specified hash algorithm and matched: K workspace, Stage 1 export,
Stage 2 audit, discovery manifest, Stage 4 generation, producer sources,
generated tree, and Lean workspace. All 810 individually recorded Stage 1
source hashes also matched, with no missing files. The separately recorded
Stage 5 invocation directory is not an audit mount, so its tree digest cannot be
independently recomputed; the mounted candidate workspace digest did match.
Raw results are in [00_provenance.out](/audit-output/evidence/00_provenance.out)
and [03_recorded_hashes.out](/audit-output/evidence/03_recorded_hashes.out).

## Stage 3 inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` against the
frozen `/reference/k-proof`, not against any earlier review. The local module
closure selected by `prove.sh` is exactly the single module `VERIFICATION`.

- Frozen `verification.k` SHA-256:
  `cad7035d9ebd863f4d75692b08d03413204df13a74ebcb52e4cda1bfb35e6c10`.
- Reconstructed rule count: 55.
- Recomputed whole-inventory hash:
  `a2523def47030dccad31ef8683dd617cfc620e1f05b3fe7f963639ba8eee7c2f`.
- Every source span, normalized source hash, and `source_rule_id` was
  independently recomputed. All IDs were unique.
- Comparison with `lemma-discovery.json` was bijective and order-sensitive:
  55 versus 55, no omissions, no extras, no duplicates, and identical ordered
  identities and inventory hash.

The complete reconstructed source text and per-rule hash calculation are in
[01_inventory.out](/audit-output/evidence/01_inventory.out).

## Independent classification judgment

The 55 frozen rules independently classify as 40 `DEFINITION` and 15
`DOMAIN_LEMMA`; there are no `OPERATIONAL_RULE` or
`PROVED_DERIVED_LEMMA` entries.

The 40 definitions are all new-symbol-headed guarded equations, exhaustive
cases, structural recurrences, or named max/projection summaries. The 15 domain
lemmas are exactly:

- four partial-cast definedness characterizations and four reverse projection
  facts for Int, Float, Bool, and Str;
- the dynamic-Val/static-Int `applyCmp(">", ...)` fact;
- the `maxFloat = maxFOpaque` symbolic bridge;
- dynamic numeric and string `applyCmp(">", ...)` facts; and
- three Int/Float/Bool sort-disjointness facts.

None was first proved as the exact same rule against a module omitting it.
Every Stage 1 claim module imports `VERIFICATION`, which already contains the
rule, so no entry qualifies as a proved derived lemma. Every rule bearing a
`simplification` or `simplification(...)` attribute is classified as either a
definition or a domain lemma.

All 15 domain lemmas are relevant to `return max(l)` and the frozen
postconditions: they support the Int and Float accumulators, mixed numeric
dispatch, string dispatch, guarded projections, or the mutually exclusive
numeric views. None is an unrelated theorem. The independent classifications
exactly match `lemma-discovery.json`. Exact spans and relevance are recorded in
[14_classification_assessment.md](/audit-output/evidence/14_classification_assessment.md).

## Stage 4 deterministic generation

I reran the required call to
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
three mounted inputs. The sandbox initially prevented Lean 4.22 from resolving
`/proc/<getpid()>/exe` because `/proc` exposes host PIDs while processes receive
namespace PIDs. I recorded that initial infrastructure failure, then used the
audited 27-line `LD_PRELOAD` shim in
[proc_pid_shim.c](/audit-output/evidence/proc_pid_shim.c), which only maps
`getpid()` to the host PID exposed by `/proc/self`. Lean then reported the exact
pinned version and commit. No candidate or provenance input was changed.

The rerun returned:

- status `PASS`;
- 15 obligations;
- zero designated sorries;
- 57 generated trust declarations;
- successful `lake clean` and `lake build`; and
- generated tree hash
  `6eedeca43fb0e6ce143a75bfc6ce3f08755dae826ef9b99b0a1fdaaf9bfe38f2`.

The returned evidence, including build output, is in
[02_preflight.out](/audit-output/evidence/02_preflight.out); the diagnosed first
attempt is preserved separately in
[02_preflight_initial_failure.out](/audit-output/evidence/02_preflight_initial_failure.out)
and the shim/version check in
[04_toolchain_shim.out](/audit-output/evidence/04_toolchain_shim.out).

I separately checked the obligation map rather than relying only on preflight:

- the independently classified domain set has 15 rules;
- its ordered IDs are exactly the 15 unique obligation IDs;
- every obligation's source span, normalized hash, inventory hash, discovery
  hash, and Lean-conjunct hash matches;
- `obligation-map.json` hash
  `7ac42c6c2159f7c38c01cf6258202fcb87088de42f63d70404315d04a93df17f`
  matches the generator manifest; and
- there are no omitted, duplicated, irrelevant, or reordered obligations.

The four definedness obligations contain `∧ True` because the source right side
contains `#Ceil(V)` where `V` is already a well-sorted `Val`. This is a faithful
translation of a trivially defined subterm inside a nontrivial equivalence, not
a standalone vacuous target conjunct or a weakening.

The selected status is `OK`, not `KLEAN_NO_OBLIGATIONS`, which is correct for
the nonempty 15-rule domain set.

## Fixed target identity

The fixed generated target is
`Klean35MaxElement.Lemmas.targetStatement` in
`Klean35MaxElement/Lemmas.lean`, with 27 parameters and 15 conjuncts.

- Statement SHA-256:
  `ac69b69a6eb9f68af8cead6d01b6704e4547ab28f72e9c18b14394004aeba7f1`.
- Definition SHA-256:
  `d278bfd415e4e5e8119d008f41e83c5fcbecad9d91a029c7d37edb0574ab8418`.

The reconstructed exact target, generator manifest target, audit-input target,
and target parsed from the fresh `Base` are identical. The candidate does not
declare or shadow `targetStatement`. `Proof.final` applies the fixed qualified
target to the same 27 parameters in the exact manifest order; it does not prove
a duplicate or weakened theorem. Structural details and the exact theorem print
are in [05_stage4_structure.out](/audit-output/evidence/05_stage4_structure.out),
[11_candidate_structure.out](/audit-output/evidence/11_candidate_structure.out),
and [12_print_final.out](/audit-output/evidence/12_print_final.out).

## Fresh Stage 5 build and trust accounting

I created `/tmp/audit-work/35-max-element-proof-audit`, copied only the three
candidate source/configuration files, and copied the immutable generated project
as `Base`. Candidate `Proof.lean` and generated `Lemmas.lean` hashes matched
their mounted originals. I then ran both `lake clean` and `lake build`; the
build succeeded. Full output is in
[06_clean_build.out](/audit-output/evidence/06_clean_build.out).

The candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new
`opaque`, and it defines each target parameter exactly once with the manifest
type. It neither changes nor shadows the generated target.

The exact axiom query produced:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. None of the 57 generated declarations in
`trust-inventory.json` occurs in the dependency list. The three reported names
are pinned Lean core axioms, not candidate-created or generated declarations;
`Classical.choice` comes from the candidate's classical decidable equality
helpers. This accounting is clean and is detailed in
[07_print_axioms.out](/audit-output/evidence/07_print_axioms.out) and
[16_axiom_reconciliation.md](/audit-output/evidence/16_axiom_reconciliation.md).

## Operational-bridge audit of all target parameters

All 27 exact candidate definitions, KORE bindings, source-rule IDs, types, and
line numbers are listed in
[11_candidate_structure.out](/audit-output/evidence/11_candidate_structure.out).
I compared each with the corresponding frozen source rules and operational K
equations.

The following 25 implement the meaning used over the complete source-obligation
domain: `_andBool_`, `_orBool_`, `«_>Int_»`, the numeric/string-domain cases of
`applyCmp`, `codesOf`, `isBool`, `isFloat`, `isInt`, `isNumericV`, `isStr`,
`numericGt`, `numericView`, the four partial projections, the four total
projections, `strLt`, and the four option-valued projections.

The two Float-max parameters fail:

```lean
private def floatMaxImpl (a b : SortFloat) : SortFloat :=
  if a.isNaN then a
  else if b.isNaN then b
  ...

def maxFOpaque := floatMaxImpl
def «maxFloat(_,_)_FLOAT_Float_Float_Float» := floatMaxImpl
```

The pinned K `FLOAT.max` uses `BigFloat.max`; its own K 7.1.293 test oracle
returns the other operand when either argument is NaN. I compiled and executed
a fresh K LLVM witness. Both frozen evaluations returned `1.0`:

```text
maxFloat(NaN, 1.0) = 1.0
maxFloat(1.0, NaN) = 1.0
```

The actual frozen `max_element` program also terminates normally and satisfies
assertions that both `[NaN, 1.0]` and `[1.0, NaN]` produce `1.0`. By contrast,
all four corresponding candidate calls (`maxFOpaque` and `maxFloat`, both
argument orders) report `.isNaN = true`.

Evidence is in
[09c_k_adversarial_complete.out](/audit-output/evidence/09c_k_adversarial_complete.out),
[13_frozen_program_adversarial.out](/audit-output/evidence/13_frozen_program_adversarial.out),
and [08_lean_adversarial.out](/audit-output/evidence/08_lean_adversarial.out).

This discrepancy is inside the formal Stage 1 domain: `allNumericVS` accepts
every represented Float and the Float-head claim has no finite or non-NaN
precondition. It directly affects the source program's returned value.

Finally, I changed only the two public Float-max bindings in a separate copy to
the constant `fun _ _ => 0.0`. `lake clean`, `lake build`, and the same axiom
query still succeeded. That counterfactual is recorded in
[10_counterfactual.out](/audit-output/evidence/10_counterfactual.out). It proves
that the fixed equality obligation and `Proof.final` do not constrain the
operational meaning of either parameter. The required independent parameter
audit therefore detects a genuine convenient-definition failure that the clean
build and clean axiom list cannot detect.

A concise per-parameter semantic table is in
[15_parameter_semantics_assessment.md](/audit-output/evidence/15_parameter_semantics_assessment.md).

## Conclusion

Stage 3 is correctly classified and Stage 4 is deterministic, complete, and
target-preserving. Stage 5 proves exactly that target in Lean, but the proof is
not a proof of the frozen operational lemma because two load-bearing parameter
definitions implement the wrong Float-max behavior. Under the required
operational-bridge gate, this is fatal.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
