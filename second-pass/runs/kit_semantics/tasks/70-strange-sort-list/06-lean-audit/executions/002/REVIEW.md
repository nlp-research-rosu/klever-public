# Independent Stage 3–5 audit: `70-strange-sort-list`

## Result and scope

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, in
launcher-recorded mode `CLASSIFICATION_AND_PROOF`. I did not rely on the prior
Stage 2 verdict, the protected Stage 3 rationales, prior PASS records, or
candidate comments as authority. The trusted Stage 6 input contract verifies
the recorded resolution hash
`962739feff9e82e3a15b9e75f5f053e8d43b3e1f8a235f8a432be795ad2b013b`
and resolves this problem and mode exactly.

The Stage 3 classification is complete and mathematically correct; Stage 4
has a one-to-one, non-vacuous obligation for the sole true domain lemma; and
Stage 5 proves that exact frozen obligation using operationally faithful map
definitions. The audit therefore passes as legitimate.

Raw commands are indexed in [evidence/COMMANDS.md](evidence/COMMANDS.md).

## Producer and immutable-input gate

I hashed the two mounted producer sources before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `c1a3c7a8d3fb3925fb03fbdb217eeecdd7b31c084cecf5d9afb8c24b93545ec6` |

Each observed value equals both `source-manifest.json` and
`generator-manifest.json`. The immutable image ID is consistently
`sha256:3e7ccb537ad6ba1c0b15c4a9b801549cf1f28b9781690cdd67bfdf5f0e243b32`
in the source manifest, generator manifest, and the producer-bundle path
bound by `/audit-input.json`. The trusted pipeline tree hash of the complete
producer bundle is
`e088a6bbd1959c58a124c61579dc475a5f63eb76cdf9babdb7edf21bad27c5e9`,
exactly the launcher-recorded value. There is no producer-source
infrastructure error.

The independent frozen hashes also all match `/audit-input.json`:

| Artifact | Observed and expected hash |
|---|---|
| Stage 1 pipeline tree | `e5ddc1c29390fe36f2c23bb6435be13695327077c320ba472673effb8c171095` |
| Stage 1 export tree | `3889ec0c36d526de15251d7690e792b3f83a0f885c053e43e0fe6bed6c272592` |
| Stage 3 manifest file | `183a50894c3eb4eb5ff272bc412f8e02e61c262d190368d018b9d370868f8e3f` |
| Stage 4 selected tree | `750678eac8045437e1dd0e62d4e9bba83a5f39a8bf1cdd926f6f90250f71491d` |
| Generated project export tree | `c5b68d488a3c9ab8f2600e6aacf2aeb4de17f757b80e8c8e7cc210b45aad8484` |
| Stage 5 candidate tree | `c6a1732b139ab0a0e87cbf9bd5c13fd1c6b06574d1fbdafa4372e44b16f9ad58` |

The complete computation is in
[independent-hash-inventory-target-checks-final.log](evidence/independent-hash-inventory-target-checks-final.log).

## Inventory reconstruction and bijection with Stage 3

I ran the trusted canonical inventory code on the frozen
`/reference/k-proof`, not on a copied classification. `prove.sh` selects
`VERIFICATION`, whose local verification-module closure contains only that
module. The frozen `verification.k` SHA-256 is
`9f73cfd957a04680900778f933a846b44dc9f8e4fb2e28425a15e10ce6e23b80`.

The reconstructed ordered inventory has six unique entries and whole-inventory
hash
`da706790352d45b069c499d73417d4bd7022226e9a5a51632c2825c9366b3364`:

| Lines | Normalized SHA-256 / `source_rule_id` suffix | Independent class | Judgment |
|---|---|---|---|
| 8 | `8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` | Empty case of the newly named total predicate `allInts`. |
| 9 | `bb65aed9f318cb650e6f3aaeb61b929864859d3dc05404f2b4a53b0d1f2058d0` | `DEFINITION` | Structural recurrence of `allInts` over the strict tail. |
| 15–16 | `7e05d593a11ac1688b57228d1e3402caa7bde6bf8a21122047627bf83e3662d2` | `DEFINITION` | Crossed-bounds case of the new summary `strangeAcc`. |
| 17–19 | `e5cf5fe356747eca4563d29d41d439e5617c1c39a5f5f46120ed36322a8c30f3` | `DEFINITION` | Singleton-interval equation of `strangeAcc`. |
| 20–26 | `ec00b8b164e1c0f6d16eef935ec05c2166e772018597863b95e7d0f0326eada7` | `DEFINITION` | Recursive alternating-endpoints equation of `strangeAcc`, shrinking the interval. |
| 31–33 | `565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503` | `DOMAIN_LEMMA` | Existing K Map operations satisfy a guarded deletion identity; this is not a definition. |

The first five rules introduce and exhaustively define named predicates or
summaries. They do not rewrite a source-program operation, and they assert no
independent fact about an existing symbol. `strangeAcc` directly models the
source loop: after sorting, it appends the left endpoint, then the right
endpoint, and recurs inward, with a singleton and crossed-bounds case. Its
appearance in the loop invariant and postcondition does not turn its defining
equations into domain lemmas.

The final rule is a `[simplification]` rule over pre-existing hooked Map
symbols:

```k
rule (M:Map K:Int |-> _V:Scope) [K <- undef] => M
  requires notBool K in_keys(M)
  [simplification]
```

It says that adding a fresh binding and deleting that key leaves the original
map. It is mathematically true for K maps, but it is an additional fact, not a
definition. Stage 1 compiles `VERIFICATION` containing the rule before every
`kprove`; there is no earlier claim proving this exact rule against a module
that omits it. Thus it is not `PROVED_DERIVED_LEMMA`. It is relevant to this
program's operational proof because the supplied function-call semantics'
`#pop` rule removes the callee location from the `scopes` map when returning;
the source function necessarily enters and exits that call frame. It is not an
irrelevant generic lemma.

The protected Stage 3 manifest contains these same six unique identities in
this exact order, with no omission, duplicate, extra identity, span change, or
hash change. Its classes are five `DEFINITION`, zero `OPERATIONAL_RULE`, zero
`PROVED_DERIVED_LEMMA`, and one `DOMAIN_LEMMA`. The sole simplification is
therefore classified in one of the two permitted categories.

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`
and the required three inputs plus the pinned toolchain lock. The first run
exposed an audit-sandbox issue: `getpid()` returned a nested PID while the
read-only `/proc` mount was keyed by host PIDs, so Lean could not locate its
application. That raw failure is retained in
[stage4-preflight-rerun.log](evidence/stage4-preflight-rerun.log). I used the
source-recorded [hostpid_shim.c](evidence/hostpid_shim.c), which changes only
`getpid()` to the numeric `/proc/self` target. With that environment repair,
the pinned Lean 4.22.0 commit and Lake 5.0.0 report correctly, and the unchanged
trusted preflight returns `PASS`. The rerun's Lake build output hash
`150d65c7bbf9a0cb35c2ad76eb23daa448eb7daa0b15d6bb67164684340be9a9`
also exactly reproduces the recorded Stage 4 preflight. See
[stage4-preflight-rerun-with-hostpid.log](evidence/stage4-preflight-rerun-with-hostpid.log)
and [lean-environment-shim.log](evidence/lean-environment-shim.log).

The independent domain set is nonempty and has exactly one entry, so this is
correctly a normal `PASS`, not `KLEAN_NO_OBLIGATIONS`. The obligation map has
one unique source rule and one unique obligation, both
`rule-565182bf10d31fb24d96318e023c71c80005ab90c1b99978f05bb734ef394503`,
in the same position. The source span, normalized hash, inventory hash,
discovery hash, and conjunct hash all match. The conjunct SHA-256 is
`beb982d3d676f090b6f62a6e6ffa723b3556ba6ce0e5d72a9d3f65992e7942f2`.

Mathematically, the generated conjunct is exactly the frozen K rule: for an
integer key `K`, scope `_V`, and map `M`, if `K` is absent from `M`, remove `K`
from the union of `M` with the singleton `K |-> _V`, obtaining `M`. The K sort
injections are present on both key and scope. The hypothesis is satisfiable
(for example, an empty `M`) and load-bearing in the candidate proof. The
conjunct is neither `True`, duplicated, weakened, nor irrelevant.

The fixed generated target agrees byte-for-byte and structurally across the
generated project, generator manifest, and `/audit-input.json`:

- declaration: `Klean70StrangeSortList.Lemmas.targetStatement`;
- statement: `Klean70StrangeSortList.Lemmas.targetStatement _Map_ «_in_keys(_)_MAP_Bool_KItem_Map» «_[_<-undef]» «_|->_» notBool_`;
- statement SHA-256: `59c6a8cdae0d53bb890487b0c988dc380ed0e04d779f5cf1b2d696ba0b2a0bfc`;
- definition SHA-256: `e2d8cb7b8fa23a1e8872dd6d1378d6460238926e5481ed82eb51e9ef1cd39171`.

The raw `Lemmas.lean` file SHA-256 in the generated project and fresh proof
copy is `dd5939284efa10c64e40b92c6801db71d1994fcedcdeee02c13d4a8609424307`;
`cmp` reports equality. See
[proof-target-file-identity.log](evidence/proof-target-file-identity.log).

## Fresh Stage 5 build, theorem identity, and forbidden constructs

I created `/tmp/audit-work/proof-audit`, copied the candidate, and populated
its `Base/` only from the selected generated project. To defeat the generated
Base project's absolute shared build directory as a source of stale artifacts,
I first ran `lake clean` in `Base`, then ran `lake clean` and `lake build` in
the proof project. All three commands exit 0; the complete build ends with
`Built Proof` and `Build completed successfully`. Evidence:
[proof-base-lake-clean.log](evidence/proof-base-lake-clean.log),
[proof-lake-clean.log](evidence/proof-lake-clean.log), and
[proof-lake-build.log](evidence/proof-lake-build.log).

The candidate contains exactly one definition for each target parameter and
exactly one `theorem final`. Outside the frozen `Base`, no Lean source contains
`sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. It neither declares nor
shadows `Klean70StrangeSortList.Lemmas.targetStatement`; `Proof.final` names
the frozen declaration with the five candidate bindings. The trusted Stage 5
mechanical gate independently copies the candidate, replaces `Base` from the
generation, performs a clean build, type-checks the exact target, and returns
`PASS`. See [candidate-source-audit.log](evidence/candidate-source-audit.log)
and [proof-mechanical-gate.log](evidence/proof-mechanical-gate.log).

The independent exact type and axiom command prints:

```text
Proof.final : Klean70StrangeSortList.Lemmas.targetStatement Proof._Map_ Proof.«_in_keys(_)_MAP_Bool_KItem_Map»
  Proof.«_[_<-undef]» Proof.«_|->_» Proof.notBool_
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

This is the fixed theorem, not a duplicate, weakened statement, or vacuous
variant. The exact output is in
[proof-identity-and-axioms.log](evidence/proof-identity-and-axioms.log) and
[proof-print-axioms.log](evidence/proof-print-axioms.log).

Trust reconciliation is clean. `trust-inventory.json` records 43 generated
axiom/opaque declarations, but `Proof.final` uses none of them. Its three
dependencies are the fixed trusted gate's explicit Lean logical baseline
(`propext`, `Classical.choice`, `Quot.sound`), not candidate declarations or
generated semantic oracles. `Classical.choice` is expected from the candidate's
classical decidable equality over `SortKItem`; the other two arise through
Lean's simplifier/equality infrastructure. `sorryAx` is absent, and there is no
unrecorded candidate or generated proof escape.

## Operational-bridge audit of all target parameters

All five parameters are bound to the sole domain-rule identity above. I
compared each exact candidate body with its manifest `kore_symbol`, the frozen
rule, the supplied semantics, and the deterministic generated map model:

| Candidate definition | Bound KORE symbol | Operational judgment |
|---|---|---|
| `_Map_ left right := ⟨left.coll ++ right.coll⟩` | `Lbl'Unds'Map'Unds'` | Implements disjoint Map concatenation by concatenating the list representation. The generated `Func.lean` model performs the same append after its disjointness check. The target premise makes `M` disjoint from the singleton, so the full use domain is in the defined branch. Append on overlapping maps is merely a totalization outside K's defined concat domain and cannot affect this theorem. |
| `_in_keys(_)_MAP_Bool_KItem_Map` | `Lbl'Unds'in'Unds'keys...` | Recursively scans keys with `SortKItem` equality and returns true exactly on membership, matching `MAP.in_keys`. |
| `_[_<-undef]` | `Lbl'UndsLSqBUnds-LT-'-undef'RSqB'` | Recursively removes entries with the key. K maps have unique keys, so this is exactly `MAP.remove` on every well-formed operational map. |
| `_|->_` | `Lbl'UndsPipe'-'-GT-Unds'` | Constructs the one-entry map `[(key,value)]`, exactly the K Map element hook. |
| `notBool_` | `LblnotBool'Unds'` | Lean Boolean negation, exactly K `notBool`. |

None is constant, identity, hard-coded to this theorem, or vacuous. The proof
itself establishes the general list fact that deleting an appended singleton
restores any key-absent prefix; it then derives key absence from the generated
hypothesis.

I explicitly tested the operational bridge rather than treating successful
type-checking as sufficient. The adversarial artifact
[operational_bridge_tests.lean](evidence/operational_bridge_tests.lean) defines
an intentionally false bundle (identity concat/delete, constant membership and
negation, empty element) and proves that the generated proposition alone still
admits that bundle. Concrete witnesses in the same file show those definitions
are operationally false. This confirms why body inspection is necessary. The
same artifact checks candidate concat, singleton, both Boolean-negation cases,
empty membership, and empty deletion and exits 0.

For nonempty present/absent membership and deletion, the recursive helpers are
private. In a separate inspection copy I removed only the two `private`
modifiers; [operational-inspect-only-diff.log](evidence/operational-inspect-only-diff.log)
shows no body change. After a clean successful build,
[operational_nonempty_tests.lean](evidence/operational_nonempty_tests.lean)
checks that a present key is found and deleted and a distinct key is reported
absent and preserved. All checks exit 0. These examples cover the decisive
branches and agree with the generic induction used by `Proof.final`.

The supplied source solution does not explicitly manipulate K maps, but its
function invocation necessarily allocates and later pops a K call frame. Thus
these five operations implement the exact map behavior supporting the frozen
rule used to restore the `scopes` map; they are not an unrelated convenient
interpretation.

## Final judgment

Stage 3 has a complete and correct ordered classification. Stage 4 is
producer-authentic, hash-bound, bijective, mathematically exact, and targets
the one genuine domain lemma. Stage 5 cleanly proves the unchanged target with
accounted Lean foundations and operationally faithful parameter definitions.

VERDICT: PASS
LEGITIMACY: LEGIT
