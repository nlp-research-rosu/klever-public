# Independent Stage 3–5 audit: HumanEval `92-any-int`

## Result

The protected Stage 3 classification is complete and mathematically correct, the selected Stage 4 generation is provenance-bound and exactly represents the one true domain lemma, and the Stage 5 Lean candidate proves the fixed target with an operationally faithful definition and no axiom dependencies.

Audit mode was `CLASSIFICATION_AND_PROOF` in both `AUDIT_MODE` and the verified `/audit-input.json`; semantics mode was `SUPPLIED_SEMANTICS`.

## Input and producer integrity

I treated all mounted candidate, provenance, logs, comments, and prior verdicts as untrusted evidence. The trusted inventory, preflight, hashing, and final-gate implementations came from `/reference/tools`.

The verified audit-input digest is:

`28a13a6fe0ec6a2ac52191f7fff9166a3cd46fe89dd9ce1cbc7352abb2a5f1cf`

Every recorded hash whose tree is among the mounted audit inputs was independently recomputed and matched:

| Artifact | Observed and recorded hash |
|---|---|
| Stage 1 workspace, pipeline tree hash | `f550ae1e2590152cd4b96f894807c517c076c835d473d261ea0e4435209832d8` |
| Stage 1 export, Klean tree hash | `7d55e057877a4212c12b19bce0565539800c2c0c0be418c057667e34516918c1` |
| Stage 3 manifest file | `ffef71b4dd9b819a2ff822a640540f254d04beac44bf8e606b5401f7feedaf9a` |
| Selected Stage 2 audit tree | `16172483f9d1520e7bbcd40c0a6cacd194af0973bc8dde91d3a817abc5666492` |
| Selected Stage 4 generation tree | `1b9737628a8db15ed0dac55229ea795cf0d4b58455c3ca9b3c640a5daa795ca4` |
| Stage 4 producer-source bundle | `94ba4c012f48b7135094fefcc4517f5c9a5c1052fc304449c5505ddb4dca91b4` |
| Generated Lean project | `6f6e503e5b5f69ae1569d05e376a67dd09279809fd2b1e5a9196cf89c7ccb98c` |
| Stage 5 candidate workspace | `eaca3a5fdcb0451fdf3041cf27c5eb1050cf637b37587d136badef5ae3ebf395` |

All 807 per-file Stage 1 source hashes also match `stage1_source_hashes` exactly. The audit input records a Stage 5 invocation-tree hash, but that invocation tree is not one of the launcher’s mounted inputs; the mounted candidate workspace itself was fully rehashed and matches.

Before judging Stage 4, I hashed the two exact generation-time producer files:

- `klean_export.py`: `0e653377b007bc1a742bbd8fa0dcfdf956ebb2ef2432a7137d032b0a70d59c1b`
- `klean.py`: `0e6dba9d9f456574b3bf4f4bf06933d774e9125f4d12c5a90b7314d8dd5c33a4`

These hashes match both `source-manifest.json` and `generator-manifest.json`. The source manifest and generator provenance agree on image ID `sha256:b377a4d6ce1a4210c17d7e862e3737d2c348cc4be96dfaca72ef9274846f4afc`; `/audit-input.json` binds the producer-source path to the same image digest and binds the complete producer bundle to the tree hash above. Producer provenance is therefore present and consistent; there is no producer-source `AUDIT_ERROR`.

## Stage 3 inventory reconstruction

Using `tools.k_rule_inventory.inventory_verification` on the frozen Stage 1 workspace, I reconstructed the local closure rooted at `VERIFICATION`. It contains `VERIFICATION-SYNTAX` and `VERIFICATION`, in source order, and exactly four rules:

| Span | `source_rule_id` / normalized hash | Independent class |
|---|---|---|
| `12–13` | `rule-d467c351c964bfa6aa3699f282303d6447cfcf61979d2a3950f1319a2bfd3c44` | `DEFINITION` |
| `16–40` | `rule-f0f9d16c2d45c2a40f20bad1f84e2c6cdaad7928fcf033dc6b8c2ffff3f6b10d` | `DEFINITION` |
| `52–54` | `rule-2337b981dde3e7f5b878ce7ffbb3f2c1c87d9b3c9777edc1dbeab1aeeba99ca5` | `DOMAIN_LEMMA` |
| `56–59` | `rule-b4cd16bb262eb62089f82976d9f4fde2111bb34eaa3c93afe9502b42d0c2119a` | `DEFINITION` |

The reconstructed `verification.k` hash is `dabf34f0d43ba43f7393c8ae07e5b4ba9b4a9173617f281dd619b5a8b245924f`; the canonical whole-inventory hash is `a8187743fcabaa841787ec6a8d9bc304dc4a1be6e3c03d3e3b0d7848487592b3`.

The protected Stage 3 manifest has the same inventory hash and the same four identities in the same order. Each identity embeds the independently recomputed normalized hash. There are no repeated identities, omissions, extras, reordered rules, or unaccounted classifications. The detailed spans, texts, attributes, and hashes in Stage 4’s bound input manifest also match the reconstruction.

### Independent classification judgment

1. `AnyIntCall(X,Y,Z) => Call(Name("any_int"), ...)` is a parse-time macro for the named invocation proof term. It is a `DEFINITION`, not an execution shortcut.
2. `anyIntModuleScope => scope(...)` is the parse-time macro defining the named proof configuration containing the exact `any_int` closure and source body. It is a `DEFINITION`.
3. `boolAsInt(B) => #if B #then 1 #else 0 #fi [simplification]` is a `DOMAIN_LEMMA`. It does not introduce or define `boolAsInt`; the supplied semantics already declares that symbol and gives the exhaustive rules `boolAsInt(true) => 1` and `boolAsInt(false) => 0`. Stage 1 installs the generalized simplification before the main proof. No Stage 1 K claim first proves that exact generalized rule in a module excluding it, so it cannot be a `PROVED_DERIVED_LEMMA`. It is also not an ordinary operational rule.
4. `anySum(X,Y,Z) => ...` is the sole total equation defining the named mathematical summary used by the postcondition. It is a `DEFINITION`.

The only rule with the `simplification` attribute is classified as `DOMAIN_LEMMA`, satisfying the simplification restriction. There are no `OPERATIONAL_RULE` or `PROVED_DERIVED_LEMMA` entries.

The domain lemma is materially relevant. The source program accepts both `Int` and `Bool` through `isinstance(_, int)`; the supplied semantics says `isIntV(_:Bool) => true`, promotes Booleans to integer values in arithmetic and comparison, and the Stage 1 claims use `boolAsInt` for all seven claim families containing Boolean inputs. This is not an irrelevant mathematical fact or a disguised statement of the overall postcondition.

## Stage 4 generation and target identity

I reran the required function:

`tools.klean_preflight.check_generation(/reference/k-proof, /reference/lemma-discovery.json, /reference/klean-generation, toolchain_lock=/reference/klean-toolchain.lock.json)`

The successful returned evidence has:

- status `PASS`;
- one obligation;
- generated tree hash `6f6e503e5b5f69ae1569d05e376a67dd09279809fd2b1e5a9196cf89c7ccb98c`;
- clean/build exit codes `0/0`;
- zero designated sorries; and
- 41 generated trust declarations, all structurally reconciled with the generated trust inventory.

The first invocation exposed a container `/proc` namespace mismatch: Lean uses `/proc/<getpid()>/exe`, while namespace PIDs such as `/proc/3/exe` do not exist in this container even though `/proc/self/exe` does. I retained that failed output. A narrow `LD_PRELOAD` compatibility shim redirected only `/proc/<digits>/exe` readlink calls to `/proc/self/exe`; with it, the pinned Lean reports version 4.22.0 and commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unchanged trusted preflight passes. The shim changes no candidate, provenance, Lean term, elaboration rule, or kernel check.

The true domain set contains exactly the one `boolAsInt` rule. The Stage 4 status is correctly `OK`/`PASS`, not `KLEAN_NO_OBLIGATIONS`.

The obligation mapping is a strict one-to-one ordered mapping:

`rule-2337b981dde3e7f5b878ce7ffbb3f2c1c87d9b3c9777edc1dbeab1aeeba99ca5`

maps to:

`∀ (B : SortBool), boolAsInt B = kite B 1 0`

where generated `SortBool` is definitionally `Bool`, `SortInt` is definitionally `Int`, and `kite` is Lean’s Boolean `cond`. This is exactly the frozen K rule’s universal content. It neither drops a guard nor weakens the equality. The universal domain has the two concrete inhabitants `true` and `false`, so the conjunct is not vacuous.

There is one source rule, one obligation, and one distinct obligation ID. Source span `52–54`, normalized hash, inventory hash, discovery-manifest hash, conjunct hash, obligation-map hash, and binding hash all recompute correctly. There are no omissions, duplicates, extra conjuncts, or target changes.

The fixed target is:

- declaration: `Klean92AnyInt.Lemmas.targetStatement`;
- statement: `Klean92AnyInt.Lemmas.targetStatement «boolAsInt(_)_MPY-CORE_Int_Bool»`;
- definition hash: `660a75b84fa6674815103a0030359f8f594860e82c1136c9141a0fd96ea8b24d`;
- statement hash: `e27b6d924bf730490ad5cfae385719a50cfee6e7083279ec17c8b4414c4e5dec`; and
- parameter binding hash: `076354302ef4e76f7ac196cb92478e4710776f0430d06c6abaed6a10a5a8cd1b`.

These values agree among the generated source, obligation map, generator manifest, trusted target parser, and audit input.

## Stage 5 clean build, theorem identity, and trust

I made a fresh project at `/tmp/audit-work/lean-proof-final.txJ0EJ`, copied the generated project’s contents into `Base`, and ran:

1. `lake clean` in the proof project — exit `0`;
2. `lake clean` in `Base` to ensure its absolute generated build directory was also clean — exit `0`;
3. `lake build` in the proof project — exit `0`, `Build completed successfully.`

The candidate contains exactly one definition of the required parameter and no definition shadowing `targetStatement`. Its Lean sources contain none of `sorry`, `admit`, `unsafe`, `axiom`, or `opaque`. The candidate defines:

```lean
def «boolAsInt(_)_MPY-CORE_Int_Bool» : SortBool → SortInt
  | true => 1
  | false => 0
```

and states `Proof.final` at exactly the generator’s fixed statement. The trusted final mechanical gate independently copied, rebuilt, type-checked, rehashed, and accepted the candidate; its mode is `CLASSIFICATION_AND_PROOF`, status is `PASS`, and its used-axiom set is empty.

The exact requested Lean query produced:

```text
Proof.final : Klean92AnyInt.Lemmas.targetStatement Proof.«boolAsInt(_)_MPY-CORE_Int_Bool»
'Proof.final' does not depend on any axioms
```

Thus `Proof.final` uses none of the 41 collection-hook axioms recorded in `trust-inventory.json`. The empty dependency set is a subset of the allowlist; `sorryAx` is absent, and there is no unrecorded trust escape.

## Operational-bridge adequacy

The target parameter is bound to KORE symbol:

`LblboolAsInt'LParUndsRParUnds'MPY-CORE'Unds'Int'Unds'Bool`

and to the one Stage 3 source rule above. In the frozen compiled KORE, that exact symbol has the two operational equations sourced from `reference-semantics/semantics/core.k`:

- `false ↦ 0`;
- `true ↦ 1`.

The candidate’s definition is extensionally and branch-for-branch identical. Because `SortBool = Bool`, these two cases exhaust its complete domain; because `SortInt = Int`, the codomain representation is also exact. This is an honest finite operational implementation, not a constant, identity, or test-specific shortcut.

Adversarial Lean checks evaluated the candidate to `(1, 0)` on `(true, false)` and proved that all three counterfactuals fail the fixed target:

- constant zero;
- constant one;
- swapped branches.

Independent execution under the frozen K semantics completed two source-program witnesses that are sensitive to both branches:

- `any_int(True, 2, 2) = false`, which rejects treating `true` as `0`;
- `any_int(False, 1, 1) = true`, which rejects treating `false` as `1`.

These witnesses supplement the universal Lean target; they do not replace it. Together with the exact K equations, KORE binding, and exhaustive candidate definition, they rule out a convenient but operationally false bridge.

## Evidence index

Raw commands and complete or tool-returned results are under `/audit-output/evidence/`. Principal files are:

- `01-producer-provenance.log`, `01b-producer-manifests-audit-input.log`: producer hashes and manifests;
- `02-reconstructed-inventory.log`: canonical reconstructed inventory;
- `04-klean-check-generation.log`: retained initial `/proc`-related failure;
- `07-klean-check-generation-with-proc-shim.log`: successful required preflight result;
- `11-trusted-final-mechanical-gate.log`: bound final mechanical gate;
- `12-operational-bridge-adversarial-lean.log`: candidate and counterfactual Lean checks;
- `14-independent-k-bridge-witnesses.log`: independent source-program K witnesses;
- `15-independent-structural-hash-audit.log` and `structural_audit.py`: all mounted-tree hashes, 807 source-file hashes, inventory bijection, target, and candidate checks;
- `16-semantic-target-candidate-sources.log`: frozen K rules, supplied semantics, generated target, KORE equations, and candidate;
- `17-print-axioms-Proof-final-exact.log`: exact `#print axioms Proof.final` result;
- `18-proc-namespace-shim-evidence.log`: environment fault, narrow shim source/hash, and pinned Lean identity;
- `19-no-prior-derived-lemma-proof.log`: absence of an earlier exact K claim proving the generalized rule; and
- `20-fresh-proof-clean-build-final.log`: final pristine clean-build transcript.

VERDICT: PASS
LEGITIMACY: LEGIT
