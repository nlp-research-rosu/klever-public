# Independent Stage 3–5 audit: `4-mean-absolute-deviation`

Audit mode: `CLASSIFICATION_AND_PROOF`  
Condition: `kit-semantics`  
Semantics mode: `SUPPLIED_SEMANTICS`

I treated every candidate file, prior review, log, comment, and claimed prior
success as untrusted evidence. The judgments below come from the frozen
sources, trusted inventory/preflight code, recomputed hashes, and direct
semantic comparison.

## Input and producer provenance

The environment and `/audit-input.json` both select
`CLASSIFICATION_AND_PROOF`. The audit-input resolution digest recomputes to
`4a9f68eed1774874736c8a7968facdf668de0fa477b364e085d46eae907da4ea`,
exactly its recorded value. The trusted mounted-input binding gate passed.
All 780 recorded Stage 1 per-file hashes matched the mounted workspace with no
missing, extra, or changed file.

The Stage 4 producer provenance is intact:

- `klean_export.py`:
  `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`
- `klean.py`:
  `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`
- generator image:
  `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`
- producer-source tree:
  `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`

Each file hash matches `generator-manifest.json` and
`source-manifest.json`; the image ID matches those manifests and the basename
of the producer-source path recorded in `/audit-input.json`. The producer
files are also byte-identical to the corresponding trusted `/reference/tools`
files. There is no producer-source `AUDIT_ERROR`.

## Independent rule inventory

Using the trusted `tools.k_rule_inventory.inventory_verification` on the
frozen `/reference/k-proof` reconstructed the local closure
`VERIFICATION-SYNTAX`, `VERIFICATION`, with:

- `verification.k` SHA-256:
  `9a7f57e12ed6af64c001eb42b7de732ed57cc4f5e027d9363abe57b82068b5d4`
- 15 rules
- inventory SHA-256:
  `3c1cfab2818be9154689f36432c8453a37abe25c1ae0c194f49ab53a863ede11`

For every entry, the normalized source was independently rehashed and
`source_rule_id` was confirmed to be `rule-<normalized_sha256>`.

| Lines | Normalized SHA-256 | Independent class | Role |
|---:|---|---|---|
| 26–44 | `0b30d37fcb1fa6f2e9d5602fd000c7184e19e2179cc09da8efcca1f73abb811e` | `DEFINITION` | `madBody` macro |
| 47 | `78f2a049ece805815d21e9063a74aff75f3d53f22a84a77fea64ffc91042a363` | `DEFINITION` | `allFloatVS` base |
| 48–49 | `2a5f59dcc54d654448c496b86879b657233ccdf91d38545bb4c06ceb1ed40871` | `DEFINITION` | `allFloatVS` recurrence |
| 54–56 | `97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e` | `DOMAIN_LEMMA` | projection definedness |
| 57–59 | `f394e6869605ba695d3a1ee914ff52207c3f62e8e1c3c99caa25ea85dac2403e` | `DEFINITION` | named `projectFloat` equation |
| 60–62 | `004b77064d41c5296c2b9a4939f9183460b9b84c088f3d578b78745808abb257` | `DEFINITION` | reverse normalization for that helper |
| 63 | `bd643f181b65c0fe3a82e3f5d4c2d3ba4e8c80c16d39267cbbeb88b6371fbbea` | `DEFINITION` | helper identity case |
| 67–70 | `92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7` | `DOMAIN_LEMMA` | guarded float `applyBin("+",…)` |
| 71–74 | `6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f` | `DOMAIN_LEMMA` | guarded float `applyBin("-",…)` |
| 77 | `07e38f1df5e81d6a854903024c0a7ce85cdf237fa93efbb509e769c262f3bdac` | `DEFINITION` | sum-fold base |
| 78–79 | `c262061ba80c2445257ddcd2f041f47b796a7c356c25ccd0abdc0c61f65a8ab4` | `DEFINITION` | sum-fold recurrence |
| 81 | `e05dfca0da35f598226b9eaa3edd9657b842c4ca648929840531db77d9a1cc03` | `DEFINITION` | deviation-fold base |
| 82–86 | `86b9970d9f7bc47527162d9e7b2d0edf29e0222f21c615a73606be510fae2a55` | `DEFINITION` | deviation-fold recurrence |
| 88–89 | `64fc7fe46c4d3d4cba6d1895cec98deeda5e2d85a8aa58929c5d686628e20725` | `DEFINITION` | empty `madResult` branch |
| 90–99 | `07a3b4455e03279c9c5f1321b884035b05b44559041506e96c2b2c8559a8ca52` | `DEFINITION` | nonempty `madResult` branch |

The reconstructed and discovery lists have identical length, order, and
unique IDs. There are no omissions, extras, or duplicates, and the inventory
hash matches `/reference/lemma-discovery.json`.

## Classification judgment

The twelve `DEFINITION` entries genuinely introduce a macro, recursive
predicate, projection helper, fold summary, or result summary. They do not
assert an independent human-facing property.

The other three rules are genuine `DOMAIN_LEMMA`s:

1. Lines 54–56 characterize definedness of the pre-existing partial
   Val-to-Float projection.
2. Lines 67–70 lift the supplied typed float-add dispatch through a symbolic
   `Val` under `isFloat`.
3. Lines 71–74 do the analogous work for subtraction.

They are relevant: the source program folds float addition, computes
`number - mean`, and needs the projection from symbolic list elements. They
are neither definitions of fresh symbols nor ordinary execution rules.
`prove.sh` compiles them into the only verification definition before running
the claims; it does not first prove any exact rule against a module omitting
that rule. Thus none qualifies as `PROVED_DERIVED_LEMMA`.

Every rule carrying `simplification` is classified as either `DEFINITION` or
`DOMAIN_LEMMA`, as required. I therefore accept the protected Stage 3
classification.

## Deterministic Stage 4 generation

The independent domain set contains exactly the three rules above. The
generated source-rule list and obligation list contain those same three
unique IDs in the same order, with exact spans, normalized hashes, inventory
hash, discovery hash, and conjunct hashes. There is a true 3↔3 bijection.

The obligations preserve the frozen statements:

- optional Float projection is defined iff `isFloat` is true;
- guarded float addition dispatches to `addF(A, projectFloat(V))`;
- guarded float subtraction dispatches to
  `subF(projectFloat(V), M)`.

The `∧ True` in the first Lean conjunct is the exact reduction of source
`#Ceil(@V)` where `@V` is already typed `Val`; it is not an injected
standalone obligation and does not weaken the projection equivalence. I found
no irrelevant obligation, omitted condition, duplicate, or target change.

Identity checks all passed:

- obligation-map SHA-256:
  `7b040d50402752de783e6f37d7e583b52a9385b218f8da62598b57fd6cbd00d5`
- generated tree SHA-256:
  `98194a8fd31a8434562a813813028f8505a87be75300080306c91a42113592e6`
- target definition SHA-256:
  `5c021c8f0c4cb38fc323789aa10d96159c82d20b4b6f7cabf3d22516570efdda`
- target statement SHA-256:
  `829c649b0060f54c7ee13f26fa9341bb89624cacc397ec3953fddee7b14ae783`

The generated target reconstructed by the trusted exporter is identical to
the generator manifest and audit input, including all six parameter bindings.
The fixed theorem is the conjunction of the three obligations.

I invoked `tools.klean_preflight.check_generation` exactly as requested. Its
manifest, bijection, target, trust-declaration, and import checks completed,
but its temporary build failed because the audit image's pinned
`/opt/elan/.../bin/lean` itself exits with `error: failed to locate
application`. Supplying the explicit pinned Lake/Lean home fixed Lake's own
installation detection but not the broken Lean executable. This independent
run did not return a passing evidence object; the exact errors are preserved
under `evidence/03-stage4-preflight.txt`. The earlier recorded Stage 4 PASS
was not used as a substitute.

## Stage 5 mechanical and theorem-identity checks

I created `/tmp/audit-work/lean-audit`, copied the candidate source and
metadata, and copied the exact generated project into it as `Base`. The fresh
`Base` tree has the expected generated-tree hash.

`lake clean` exited 0. `lake build` then failed while building the first Base
module because the same pinned Lean executable reported `failed to locate
application`. Consequently an independent `#print axioms Proof.final` also
failed before producing an axiom list. I cannot claim an independently clean
build or reconcile actual `Proof.final` dependencies with
`trust-inventory.json`; in particular, no prior claimed axiom output was
trusted.

The source-level trusted candidate gate does establish the following limited
facts:

- `Proof.final` states exactly the fixed generated target.
- Each of the six target parameters has exactly one candidate `def`.
- The candidate does not shadow `targetStatement`.
- Candidate-written Lean contains no `sorry`, `admit`, `unsafe`, new `axiom`,
  or new `opaque`.

Those facts are necessary but do not cure the operational failure below.

## Operational bridge audit

Five parameter implementations agree with their frozen meaning on their
complete bound domains:

- `addF` uses `Float.add`, matching supplied `+Float`.
- `subF` uses `Float.sub`, matching supplied `-Float`.
- `isFloat` recognizes exactly a singleton K sequence containing an injected
  Float.
- `project:Float?` returns exactly that optional Float projection.
- `projectFloat` is identity on injected Floats. Its `0.0` totalization is
  outside the `isFloat` guard, where this proof-local total helper has no
  frozen value equation.

The sixth parameter is unsound. It is bound to the global KORE symbol
`LblapplyBin…`, whose supplied operational semantics contains 32 `applyBin`
rules. The candidate implements only Float/Float `+` and Float/Float `-`, then
returns `noneV` for every other input. The candidate comment that the remaining
inputs have no mapped rewrite is false.

Two satisfiable adversarial witnesses are decisive:

| Input | Frozen operational result | Candidate result |
|---|---|---|
| `applyBin("+", inj_Int(2), inj_Int(3))` | `inj_Int(5)` by `semantics/int.k:9` | `noneV` |
| `applyBin("*", inj_Float(2.0), inj_Float(3.0))` | `inj_Float(mulF(2.0,3.0))` by `semantics/float.k:115–117` | `noneV` |

These are direct contradictions of ordinary supplied execution rules, not
arbitrary choices on K-stuck inputs. The fallback is therefore a hard-coded
convenience definition rather than an implementation of its bound operational
symbol.

I also prepared a counterfactual in which `addF` and `subF` are both constant
zero and the two `applyBin` branches return zero. The generated equations
remain structurally self-consistent under those coordinated mutations,
illustrating why candidate operational definitions must be checked
independently. Lean execution of the witness and counterfactual was blocked by
the same audit-image executable failure, but the actual candidate mismatch
above follows directly by definitional reduction of its wildcard branch and
the cited frozen K rules.

This operational-bridge failure is independently sufficient for rejection,
even if a functioning Lean installation were to confirm a clean build and an
acceptable axiom list.

## Final judgment

Stage 3 classification and the deterministic Stage 4 rule/obligation/target
mapping are substantively correct. The selected Stage 5 proof is nevertheless
not legitimate because one of its required bound definitions contradicts the
supplied operational semantics. The failed clean rebuild and missing
independent axiom output are additional unmet mechanical requirements, not the
basis for excusing or weakening the semantic rejection.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
