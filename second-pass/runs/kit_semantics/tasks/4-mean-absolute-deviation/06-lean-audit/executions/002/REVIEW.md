# Independent audit: 4-mean-absolute-deviation

## Result

The Stage 3 classification is independently supported, producer provenance is
authentic, the Stage 4 manifests are structurally self-consistent, and the
Stage 5 submission clean-builds and proves exactly the declaration selected by
the manifest without an unrecorded axiom escape. The overall artifact is not
legitimate, however, because Stage 4 silently narrows the frozen K `Val`
carrier when generating Lean. Its purportedly universal obligations omit all
frozen string values, so the generated target is a weakened translation of the
classified source rules.

Audit mode was independently read as `CLASSIFICATION_AND_PROOF` from both
`AUDIT_MODE` and `/audit-input.json`. The condition is `kit-semantics` and the
semantics mode is `SUPPLIED_SEMANTICS`.

## Input and producer integrity

The audit-input tree hashes and all 780 recorded Stage 1 file hashes were
recomputed. There were no missing, extra, or mismatched Stage 1 files. The
recorded hashes for the selected K audit, Stage 4 generation, candidate, Stage
1 export, discovery manifest, and generated tree also match their mounted
artifacts. The absent original launcher-side Lean invocation path could not be
rehash-checked; it is not one of the mounted evidence inputs and is not needed
for the verdict. Full results are in `evidence/14-audit-input-hash-verification.txt`.

The required producer check passed before judging generation:

- `klean_export.py`: `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`: `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`
- immutable generator image: `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`

Both file hashes agree with `source-manifest.json` and
`generator-manifest.json`; the image ID agrees with both manifests and the
producer path recorded by `/audit-input.json`. The generation-producer tree
hash `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`
also matches audit input. Thus the later semantic failure is a proof verdict,
not a missing-source or producer-provenance `AUDIT_ERROR`. See
`evidence/01-producer-provenance.txt`,
`evidence/01b-producer-tree-hash.txt`, and
`evidence/18-generation-projection-cause.txt`.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` logic over
the local verification-module closure of frozen `verification.k`. The closure
is exactly `VERIFICATION-SYNTAX`, `VERIFICATION`; the source file SHA-256 is
`9a7f57e12ed6af64c001eb42b7de732ed57cc4f5e027d9363abe57b82068b5d4`.
The reconstruction has 15 rules and whole-inventory hash
`3c1cfab2818be9154689f36432c8453a37abe25c1ae0c194f49ab53a863ede11`.

For every entry, the source span, normalized source text hash, and
`source_rule_id = "rule-" + normalized_sha256` were recomputed. The protected
manifest has the same 15 identities in the same order. Both sides have zero
duplicate IDs; there are no omissions, extras, reordered identities, changed
hashes, or unaccounted classifications. The reconstructed order and independent
classifications are:

| # | Lines | Normalized hash / source rule ID suffix | Class |
|---:|---:|---|---|
| 1 | 26–44 | `0b30d37fcb1fa6f2e9d5602fd000c7184e19e2179cc09da8efcca1f73abb811e` | `DEFINITION` |
| 2 | 47 | `78f2a049ece805815d21e9063a74aff75f3d53f22a84a77fea64ffc91042a363` | `DEFINITION` |
| 3 | 48–49 | `2a5f59dcc54d654448c496b86879b657233ccdf91d38545bb4c06ceb1ed40871` | `DEFINITION` |
| 4 | 54–56 | `97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e` | `DOMAIN_LEMMA` |
| 5 | 57–59 | `f394e6869605ba695d3a1ee914ff52207c3f62e8e1c3c99caa25ea85dac2403e` | `DEFINITION` |
| 6 | 60–62 | `004b77064d41c5296c2b9a4939f9183460b9b84c088f3d578b78745808abb257` | `DEFINITION` |
| 7 | 63 | `bd643f181b65c0fe3a82e3f5d4c2d3ba4e8c80c16d39267cbbeb88b6371fbbea` | `DEFINITION` |
| 8 | 67–70 | `92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7` | `DOMAIN_LEMMA` |
| 9 | 71–74 | `6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f` | `DOMAIN_LEMMA` |
| 10 | 77 | `07e38f1df5e81d6a854903024c0a7ce85cdf237fa93efbb509e769c262f3bdac` | `DEFINITION` |
| 11 | 78–79 | `c262061ba80c2445257ddcd2f041f47b796a7c356c25ccd0abdc0c61f65a8ab4` | `DEFINITION` |
| 12 | 81 | `e05dfca0da35f598226b9eaa3edd9657b842c4ca648929840531db77d9a1cc03` | `DEFINITION` |
| 13 | 82–86 | `86b9970d9f7bc47527162d9e7b2d0edf29e0222f21c615a73606be510fae2a55` | `DEFINITION` |
| 14 | 88–89 | `64fc7fe46c4d3d4cba6d1895cec98deeda5e2d85a8aa58929c5d686628e20725` | `DEFINITION` |
| 15 | 90–99 | `07a3b4455e03279c9c5f1321b884035b05b44559041506e96c2b2c8559a8ca52` | `DEFINITION` |

The raw reconstruction is in
`evidence/02b-inventory-reconstruction-success.txt`.

## Independent Stage 3 judgment

The correct totals are 12 `DEFINITION`, zero `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and three `DOMAIN_LEMMA`.

The definitions introduce the `madBody` summary, the `allFloatVS` predicate,
the guarded `projectFloat` proof term, the sum and deviation recurrences, and
the `madResult` summary. They meet the required definition category. The three
domain lemmas are:

1. Lines 54–56: definedness of the pre-existing Val-to-Float projection is
   characterized by `isFloat`.
2. Lines 67–70: guarded symbolic-Val restatement of the supplied Float
   addition dispatch.
3. Lines 71–74: the analogous guarded subtraction dispatch.

They are not ordinary execution rules and are relevant to projecting symbolic
float-list elements and to the two loops in the source solution. Stage 1
compiles all verification rules before its only `kprove spec.k`, so none was
first proved against a module lacking it and later used; none qualifies as a
proved-derived lemma. Every rule marked `simplification` is either one of
these definitions or domain lemmas. Detailed rule-by-rule reasoning is in
`evidence/03-independent-classification.md`.

## Stage 4 structural checks and fixed target

I reran the required `tools.klean_preflight.check_generation` call with
`PYTHONPATH=/reference`, using `/reference/k-proof`, the protected discovery
manifest, and `/reference/klean-generation`. It returned `PASS` with three
obligations. Its `lake clean` and `lake build` diagnostics both exited zero.
The complete returned evidence is in
`evidence/04d-check-generation-success.txt`.

Independent checks confirm the ordered one-to-one mapping
`97b321…`, `92241e…`, `6f2599…`; all source spans, normalized hashes,
inventory/discovery bindings, and conjunct hashes match, with no duplicate or
extra obligation. The Stage 1 export hash, discovery hash, generated-tree hash
`98194a8fd31a8434562a813813028f8505a87be75300080306c91a42113592e6`,
and obligation-map hash match all recorded values.

The target is exactly the manifest and audit-input target:

- declaration: `Klean4MeanAbsoluteDeviation.Lemmas.targetStatement`
- definition hash: `5c021c8f0c4cb38fc323789aa10d96159c82d20b4b6f7cabf3d22516570efdda`
- instantiated-statement hash: `829c649b0060f54c7ee13f26fa9341bb89624cacc397ec3953fddee7b14ae783`

At the displayed-conjunct level, the projection-definedness equivalence and
the guarded addition/subtraction equalities retain the source operators,
operand order, guards, and results. The `True` inside the first equivalence is
the lowering of `#Ceil(V)` for an already sorted K `V : Val`; it is not by
itself a separate vacuous top-level obligation. These checks establish only
structural self-consistency, not semantic identity.

## Fatal Stage 4 carrier weakening

Frozen supplied semantics defines:

```text
str(IntSeq) : Str
Str < Iterable
Iterable < Val
```

The compiled frozen definition correspondingly reports `SortStr` as a
subsort of both `SortIterable` and `SortVal`, with constructor
`Lblstr...IntSeq`. The selected generated Lean project instead declares
`SortVal` with Bool, Float, Int, and Iterable injections, but declares no
`SortStr`; generated `SortIterable` has no Str injection. There is no `str`
constructor and no injection by which a frozen string value can inhabit the
generated `SortVal`.

I reconstructed the exact export definition and applied the authentic
generation-time dependency selection, the actual five `kxExport` rewrites,
and `_widen_projection`. The result independently reports:

```text
SortStr retained: False
str constructor symbol retained: False
SortVal subsorts: [SortBool, SortFloat, SortInt, SortIterable]
SortIterable subsorts: []
```

The producer computes retained sorts from the projected symbol set and then
filters every subsort edge to that set; it does not close the retained set over
subsorts. This deletes the Str carrier before Lean emission.

All three emitted conjuncts quantify `V : SortVal`, but that Lean type is a
strict subset of the source `Val`. In particular, the first source rule is
universal over the concrete frozen value `str(.IntSeq)`, whereas the generated
projection-definedness equivalence has no corresponding case. This is a
weakened obligation even if the missing case would be straightforward to
prove, and even though all IDs and hashes are internally consistent. It
violates the required exact source-rule/obligation identity and fixed-target
mathematical judgment. Complete commands and the concrete source/generated
comparison are in `evidence/17-stage4-carrier-projection.txt`; the producer
cause is in `evidence/18-generation-projection-cause.txt`.

## Stage 5 Lean proof audit

I created `/tmp/audit-work/stage5-audit`, copied the generated project into it
as `Base`, copied the candidate proof project, and ran both `lake clean` and
`lake build`. Both exited zero. The launcher environment exposed a PID-namespace
`/proc/<pid>/exe` mismatch to Lean 4.22, so the audit used a narrowly scoped
readlink shim that maps only numeric `/proc/<pid>/exe` requests to
`/proc/self/exe`; its source/binary hashes and behavior are recorded in
`evidence/00-lean-environment-shim.txt`. It does not alter any candidate or
provenance input. Complete clean-build output is in
`evidence/06-stage5-clean-build.txt`.

The candidate does not modify or shadow `targetStatement`. Its only `final`
declaration has exactly the generated instantiated statement and recomputes to
the manifest statement hash above. Source scanning found no `sorry`, `admit`,
`unsafe`, new `axiom`, or new `opaque`. The trusted Stage 5 mechanical checker
also returned `PASS`. See `evidence/08-stage5-mechanical-gate.txt`,
`evidence/09-candidate-source-scan.txt`, and
`evidence/10-proof-identity.txt`.

The exact Lean output requested for axiom accounting was:

```text
Proof.final : Klean4MeanAbsoluteDeviation.Lemmas.targetStatement Proof.addF
  Proof.«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» Proof.isFloat Proof.projectFloat Proof.subF Proof.«project:Float?»
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. The three dependencies are Lean's standard allowed
axioms in the trusted final gate. None of the 47 generated trust declarations
enumerated by `trust-inventory.json` is in `Proof.final`'s dependency set, and
there is no unrecorded candidate trust declaration. Exact output is in
`evidence/07-axiom-audit.txt`.

Each target parameter was compared to its KORE symbol, bound rule IDs, frozen
source rules, source solution, and supplied operational rules. On the emitted
carrier, `addF`/`subF` are Float addition/subtraction; `applyBin` performs the
matching typed dispatch; `isFloat` recognizes exactly the Float injection in
the required K sequence; `projectFloat` is identity on its guarded Float
domain; and `project:Float?` is the exact structural partial projection.
Adversarial examples exercised Float addition/subtraction, Int addition,
predicate, and projection cases. Disposable counterfactuals replacing `addF`
with zero and `isFloat` with constant true both fail the final proof. Thus the
candidate bridges are locally honest for the emitted types rather than
constant or vacuous conveniences. See
`evidence/11b-bridge-adversarial-examples-success.txt`,
`evidence/12-counterfactual-addF-mutation.txt`,
`evidence/13-counterfactual-isFloat-mutation.txt`, and
`evidence/15-operational-bridge-analysis.md`.

Those Stage 5 successes do not cure Stage 4: `Proof.final` proves exactly the
fixed generated theorem, but that theorem already quantifies over the narrowed
carrier and is not the exact frozen K obligation.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
