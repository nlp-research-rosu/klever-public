# Independent audit: 149-sorted-list-sum

## Scope and result

I audited HumanEval `149-sorted-list-sum`, condition `kit-semantics`,
semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed
`/audit-input.json` select `CLASSIFICATION_AND_PROOF`. I treated the mounted
Stage 1–5 artifacts, prior audit, prose, comments, and logs as untrusted
evidence. I did not rely on the earlier Stage 2 verdict or the selected Stage 4
status for any semantic judgment.

The reconstructed Stage 3 classification is correct, Stage 4 deterministically
exports the exact one genuine domain obligation, and the Stage 5 proof uses
honest operational definitions and proves exactly the immutable target without
axioms.

## Producer and input integrity

Before judging Stage 4, I hashed the exact generation-time producer sources:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`

Both hashes match `generator-manifest.json` and
`generation-tools/source-manifest.json`. The immutable generator image ID is
`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`
in both manifests and in the final component of the producer-source path signed
by `/audit-input.json`. The producer bundle contains exactly those two sources
and `source-manifest.json`; its recomputed tree hash
`bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`
matches the launcher.

The signed resolution digest recomputes to
`3239317c1c2e9706dc0dde6503fff37fa6c84603a1463815bc08401778f99cd4`.
All 771 recorded Stage 1 regular-file hashes match bijectively, with no missing,
extra, or changed file. The independently recomputed mounted hashes also match:

- Stage 1 pipeline tree:
  `b70f0aabd7ac8b07c6ccf2a73d60e42ed067b4ffb5ebbae4a40e829d0b15f693`
- Stage 1 deterministic-export tree:
  `a89571f518e348bdbf6eaf5ea83a47a29a7444f6677824730a73ce30bb023c0b`
- Stage 3 discovery file:
  `6e73e5973131dee3591add9d5bc2de4474071d0c29df6596a8162579048d5da2`
- selected Stage 2 tree:
  `f4eba754ac862c0a2c288af3a20c920af6f8a48590f6698983e414351b664efb`
- selected Stage 4 tree:
  `5345a05eab946b149630527433ed3933d34d48b980912d0b9299bc41e8074a51`
- generated project:
  `4e0d0cbf6199207d31f5c438357d2b61728adc6351de26e1b74289eeb9b3aa95`
- mounted Stage 5 candidate:
  `d07a85dac98c351c96bc4b77f79c82180aaf61649d153cfe6225910bc99991f7`

The separate Stage 5 invocation tree is not mounted as an audit input; its
signed hash was therefore not substituted with or inferred from the candidate
workspace. All hashes that bind the mounted classification, generation,
target, and proof candidate were recomputed.

Evidence: `evidence/producer-file-sha256.txt`,
`evidence/producer-recorded-values.txt`, and `evidence/hash-audit.json`.

## Inventory reconstruction

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation against
the frozen Stage 1 workspace. `prove.sh` selects `VERIFICATION`; its local
closure consists of `VERIFICATION-SYNTAX` and `VERIFICATION`. The reconstruction
found nine rules, all in `VERIFICATION`, in this order:

| Lines | Rule ID prefix | Attributes | Independent class |
|---:|---|---|---|
| 18 | `rule-91f437c4` | none | `DEFINITION` |
| 19–20 | `rule-0e7dac14` | none | `DEFINITION` |
| 23 | `rule-cd5c2076` | none | `DEFINITION` |
| 24–30 | `rule-858547b3` | `simplification` | `DEFINITION` |
| 31–35 | `rule-134ac8fc` | `simplification` | `DEFINITION` |
| 36–38 | `rule-bbdcfa64` | none | `DEFINITION` |
| 41–43 | `rule-1136bead` | `simplification` | `DOMAIN_LEMMA` |
| 45–64 | `rule-136aef47` | none | `DEFINITION` |
| 66–71 | `rule-b75f2055` | none | `DEFINITION` |

For every rule I independently rejoined the recorded source span, normalized
whitespace, recomputed SHA-256, and reconstructed `source_rule_id`. Every span,
normalized hash, and ID matches. The canonical inventory hash is
`b08ce0100e0f2d9b83fee2942ff1b1067ccf724a2358ff8bfa0ff65457250849`.
The protected discovery manifest has exactly the same nine IDs, exactly once,
in exactly the same order, with no omission or extra entry.

Evidence: `evidence/inventory-audit.json`.

## Independent classification judgment

`stringsOnly` is a declared total predicate with base and constructor-recursive
equations. `scanEven` is a declared total summary with a base case and three
constructor-recursive cases. The two string cases partition defined integer
remainder into equality and inequality with zero; the non-string case is
disjoint, and all recursive equations consume the tail. Its two
`simplification` rules are defining equations, not asserted result properties.

`sortedListSumBody` and `sortedListSumModule` are named macro/proof-term
definitions. Constructor-by-constructor, the body is the translated source:
initialize the result and word, retain strings of even length, then apply the
two stable sorts. None of these eight rules is an ordinary operational rule or
an unproved human-facing domain fact.

The remaining rule is:

```k
rule #Ceil(seqLen(V:Val)) => #Top
  requires isStrV(V)
  [simplification]
```

It does not define either symbol and is not an execution rule. No earlier Stage
1 claim proves the exact statement against a module without it. It is therefore
`DOMAIN_LEMMA`, not `DEFINITION`, `OPERATIONAL_RULE`, or
`PROVED_DERIVED_LEMMA`.

It is true and relevant. Frozen `isStrV` is true exactly on
`str(IntSeq)`; frozen `seqLen(str(IS))` rewrites to `isLen(IS)`; and `isLen`
has exhaustive total base and recursive equations. The source program calls
`len(word)`, and the Stage 1 `scanEven` summary uses `seqLen` in its even/odd
guards. Thus the lemma is neither unrelated nor an assumed final sorting/filter
property. Every `simplification` rule is classified as either `DEFINITION` or
this `DOMAIN_LEMMA`.

Evidence: `evidence/classification-judgment.md`,
`evidence/operational-symbol-rules.txt`, and
`evidence/derived-lemma-search.txt`.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
on `/reference/k-proof`, `/reference/lemma-discovery.json`, and
`/reference/klean-generation`, using the pinned toolchain lock. It returned
`PASS`, one obligation, zero sorries, 41 generated trust declarations, and
successful clean/build diagnostics.

This sandbox hides `/proc/<pid>/exe` while exposing `/proc/self/exe`, which
initially prevented Lean/Lake from locating their installed application.
`evidence/preflight-without-proc-shim.log` records that environment failure. I
used the narrow, recorded `readlink` compatibility shim in
`evidence/proc_exe_compat.c`; it rewrites only `/proc/<digits>/exe` to
`/proc/self/exe`. With it, the pinned toolchain reports K/pyk 7.1.293 and Lean
4.22.0 at commit `ba2cbbf…`. It does not alter Lean sources, declarations,
proof terms, or input trees. The successful returned preflight is
`evidence/rerun-preflight.json`.

There is one independently classified domain rule, one source-rule record, and
one obligation, all with the exact ID `rule-1136bead…`. Counts in the generator
manifest and export result are also one. Source span 41–43, normalized rule
hash, inventory hash, discovery hash, and order all match. The obligation map
hash is `3d8c58e91a20c7e271fc6683b3339003f3c90f995206b0a535b7ae9594aff117`.

The generated conjunct is exactly:

```lean
∀ (V : SortVal)
  (h : («isStrV(_)_MPY-BUILTINS_Bool_Val» V) = true),
  ((«seqLen(_)_MPY-BUILTINS_Int_Val?» V).isSome = true) ↔ True
```

Under `h`, `P ↔ True` requires `P`; it does not erase the definedness goal. A
model with `isStrV V = true` and `seqLen? V = none` falsifies it. This is the
faithful option-valued translation of K `#Ceil(seqLen(V)) => #Top` under the
same guard. There are no irrelevant obligations, duplicates, omitted domain
rules, weakened guards, extra conjuncts, or vacuous generated conjuncts.

The immutable target is
`Klean149SortedListSum.Lemmas.targetStatement` in
`Klean149SortedListSum/Lemmas.lean`. Its exact definition hash is
`d8ff8342a0d2114a544eef12fc9d2d869abd34b5e56e793c46294a78fdf0edae`;
its applied statement hash is
`26b5132a059d3d0a86e262c8674efdab91545c4c1e238a2e484e60b2dd6e314b`.
The extracted source, generator manifest, preflight, and signed audit input all
agree. Both parameter binding hashes also recompute exactly.

Evidence: `evidence/stage4-integrity-audit.json` and
`evidence/mechanical-final-gate.json`. The trusted full mechanical gate passes;
as designed, its `semantic_classification` field says `NOT_EVALUATED`, so the
semantic conclusions above are my independent judgment.

## Fresh proof build and target identity

I copied the mounted candidate into
`/tmp/audit-work/proof-audit-clean` and copied the generated project contents
into its empty `Base` directory. Before building, `Base` had the exact recorded
generated-tree hash. I then ran both required commands:

```text
lake clean
EXIT_CODE=0

lake build
...
Built Proof
Build completed successfully.
EXIT_CODE=0
```

Complete output is in `evidence/lake-clean.log` and
`evidence/lake-build.log`. After the build, `Base` still has hash
`4e0d0cbf…`; the target file is byte-identical to the immutable generation.

The candidate source copy remains byte-identical to `/candidate`. Outside
`Base`, the only Lean sources are `Proof.lean` and `lakefile.lean`. They contain
no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. There is exactly one
definition for each required target parameter, no candidate declaration or
namespace shadows `targetStatement`, and `Proof.final` occurs once with the
exact generated applied statement as its type.

Lean's printed declaration begins:

```text
theorem Proof.final :
  Klean149SortedListSum.Lemmas.targetStatement
    Proof.«isStrV(_)_MPY-BUILTINS_Bool_Val»
    Proof.«seqLen(_)_MPY-BUILTINS_Int_Val?» := ...
```

Thus `Proof.final` is not a duplicated, weakened, or separately restated
theorem. Evidence: `evidence/proof-source-audit.json` and
`evidence/print-Proof-final.log`.

## Axiom accounting

The exact `#print axioms Proof.final` result is:

```text
'Proof.final' does not depend on any axioms
```

The command exited zero. The generated Base contains 41 axiom declarations,
and the actual name/kind/type map equals `trust-inventory.json` exactly, but
none is in `Proof.final`'s dependency closure. Therefore the dependency set is
the empty subset of the recorded trust inventory; there is no `sorryAx`, no
unrecorded axiom, and no candidate trust escape.

Evidence: `evidence/print-axioms-Proof-final.log`.

## Operational-bridge audit

The first parameter definition returns true exactly for
`SortVal.inj_SortStr` and false otherwise. This matches the direct frozen
`isStrV(str(_)) => true` rule plus its `owise` false rule and also the generated
operational equations. The generated `Inj SortIterable SortVal` instance
canonicalizes iterable-wrapped strings to the direct string constructor.

The second parameter is an honest option-valued implementation of every frozen
`seqLen` case:

- strings and sets recurse over `IntSeq`, matching total `isLen`;
- lists and tuples recurse over `ValSeq`, matching total `vsLen`;
- ranges use the same positive, negative, and empty guarded equations;
- step zero returns `none`, matching the absence of a frozen `rangeLen` rule;
- all unsupported `Val` constructors return `none`.

The nonempty range branches divide positive numerators by positive
denominators, so Lean integer division agrees with K `/Int` on the guarded
domains. The definitions are neither constant nor identity functions and do
not refer to the target theorem.

Adversarial evaluation covered empty and two-element strings; a non-string;
two-element list, tuple, and set; positive and negative nonempty ranges; both
empty-range directions; zero step; and a raw noncanonical nested string. The
observed results distinguish `true`/`false`, lengths `0`, `2`, and `3`, and
`none`.

Counterfactual Lean mutations demonstrate the risk the independent bridge check
must catch:

- constant-false `isStrV` with constant-`none` `seqLen?` proves the target
  vacuously;
- hard-coded `some 0` for every string also proves this definedness-only target;
- honest `isStrV` with constant-`none` `seqLen?` is refuted by the empty string.

All three counterfactual claims were machine-checked. The actual candidate is
not one of those convenient interpretations: source inspection and
distinguishing evaluations confirm it implements the complete frozen equations.

Evidence: `evidence/candidate-Proof-numbered.txt`,
`evidence/operational-bridge-adversarial.log`, and
`evidence/operational-bridge-judgment.md`.

## Final judgment

All classification, deterministic-generation, target-identity, clean-build,
proof-identity, axiom-accounting, and operational-bridge requirements pass.
There is no infrastructure producer mismatch and no semantic or legitimacy
defect.

VERDICT: PASS
LEGITIMACY: LEGIT
