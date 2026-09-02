# Independent Stage 3–5 audit

## Scope and conclusion

I audited HumanEval `4-mean-absolute-deviation`, condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed audit envelope select `CLASSIFICATION_AND_PROOF`; the recomputed envelope digest is `8e59ab2adffdd938903809bb1fb311b38a9a5c4b6c215ace72da39136bd58de3`.

The protected Stage 3 classification is complete and semantically correct: the frozen local verification-module closure contains 15 rules, of which 12 are definitions and 3 are relevant domain lemmas. Deterministic Stage 4 generated exactly one nonvacuous obligation for each domain lemma. The Stage 5 candidate implements the six target parameters with the frozen operational meaning, proves the fixed target, builds from a clean copy, and uses only the permitted Lean foundational axioms. The resulting verdict is PASS/LEGIT.

Raw commands and results are in [evidence](/audit-output/evidence). No earlier review or verdict was used as authority.

## Producer and input authentication

I hashed the two mounted generation-time producer files before judging Stage 4.

| Producer | Observed SHA-256 | Result |
|---|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` | Matches the generator manifest and source manifest |
| `klean.py` | `b5168e18e064b737f09d9332335eb76e78f7ac5c4a73a60c345649cad2cdd26f` | Matches the generator manifest and source manifest |

The producer tree digest is `807266be9d75e18d2fb9e05eaff407609e69e5affe9fd144822293c310d1d111`, equal to `/audit-input.json`. The immutable image ID is consistently `sha256:cef3bf63d3f1a1df5e8c5e6c788f60cc26b0b64aa857f73d907d65c64147c345` in the generator manifest, source manifest, and audit-input producer reference. Thus no producer-source infrastructure error exists. See [producer authentication](/audit-output/evidence/01-producer-authentication.txt).

The trusted hash algorithms also reproduced the recorded Stage 1 workspace, Stage 2 audit, Stage 4 generation, producer tree, candidate workspace, Stage 1 export, generated tree, discovery manifest, obligation map, and trust-inventory hashes. All 780 individually recorded Stage 1 source paths and hashes matched bijectively. See [hash verification](/audit-output/evidence/05-hash-verification.txt).

## Independent rule inventory

I ran the trusted `tools.k_rule_inventory.inventory_verification` against `/reference/k-proof`, rather than reading the protected classification as an inventory. It selected `verification.k`, whose SHA-256 is `9a7f57e12ed6af64c001eb42b7de732ed57cc4f5e027d9363abe57b82068b5d4`, root module `VERIFICATION`, and local closure `VERIFICATION-SYNTAX`, `VERIFICATION`.

The reconstructed inventory follows. A `source_rule_id` is `rule-` followed by the normalized rule SHA-256 shown here.

| # | Span | Normalized SHA-256 | Independent class | Meaning |
|---:|---:|---|---|---|
| 1 | 26–44 | `0b30d37fcb1fa6f2e9d5602fd000c7184e19e2179cc09da8efcca1f73abb811e` | DEFINITION | `madBody` macro for the translated source body |
| 2 | 47 | `78f2a049ece805815d21e9063a74aff75f3d53f22a84a77fea64ffc91042a363` | DEFINITION | `allFloatVS` empty base |
| 3 | 48–49 | `2a5f59dcc54d654448c496b86879b657233ccdf91d38545bb4c06ceb1ed40871` | DEFINITION | `allFloatVS` recurrence |
| 4 | 54–56 | `97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e` | DOMAIN_LEMMA | Float projection definedness |
| 5 | 57–59 | `f394e6869605ba695d3a1ee914ff52207c3f62e8e1c3c99caa25ea85dac2403e` | DEFINITION | guarded equation for fresh `projectFloat` |
| 6 | 60–62 | `004b77064d41c5296c2b9a4939f9183460b9b84c088f3d578b78745808abb257` | DEFINITION | reverse normalization for `projectFloat` |
| 7 | 63 | `bd643f181b65c0fe3a82e3f5d4c2d3ba4e8c80c16d39267cbbeb88b6371fbbea` | DEFINITION | `projectFloat` identity on Float |
| 8 | 67–70 | `92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7` | DOMAIN_LEMMA | guarded `applyBin("+")` dispatch |
| 9 | 71–74 | `6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f` | DOMAIN_LEMMA | guarded `applyBin("-")` dispatch |
| 10 | 77 | `07e38f1df5e81d6a854903024c0a7ce85cdf237fa93efbb509e769c262f3bdac` | DEFINITION | `sumFloatVS` empty base |
| 11 | 78–79 | `c262061ba80c2445257ddcd2f041f47b796a7c356c25ccd0abdc0c61f65a8ab4` | DEFINITION | `sumFloatVS` recurrence |
| 12 | 81 | `e05dfca0da35f598226b9eaa3edd9657b842c4ca648929840531db77d9a1cc03` | DEFINITION | `deviationFloatVS` empty base |
| 13 | 82–86 | `86b9970d9f7bc47527162d9e7b2d0edf29e0222f21c615a73606be510fae2a55` | DEFINITION | `deviationFloatVS` recurrence |
| 14 | 88–89 | `64fc7fe46c4d3d4cba6d1895cec98deeda5e2d85a8aa58929c5d686628e20725` | DEFINITION | zero-length `madResult` branch |
| 15 | 90–99 | `07a3b4455e03279c9c5f1321b884035b05b44559041506e96c2b2c8559a8ca52` | DEFINITION | nonzero-length `madResult` branch |

The inventory digest is `3c1cfab2818be9154689f36432c8453a37abe25c1ae0c194f49ab53a863ede11`. Comparing the reconstruction to `/reference/lemma-discovery.json` found 15 versus 15 rules, identical order and identities, no duplicate on either side, no omission or extra rule, identical spans and normalized hashes, and the same whole-inventory digest. The complete reconstruction is in [inventory evidence](/audit-output/evidence/02-inventory-reconstruction.txt).

## Classification judgment

The 12 `DEFINITION` entries define a macro, structural predicates/folds, fresh named projection equations, and the two branches of the named result summary. None is an ordinary execution or observation rule. The three `DOMAIN_LEMMA` entries instead assert non-definitional facts about pre-existing K operations: partial Float projection and the guarded Float dispatch of `applyBin` for addition and subtraction.

This classification agrees with the operational definitions in `operators.k`, `float.k`, and compiled KORE. `BinOp` delegates to `applyBin`; Float `addF`/`subF` compute `+Float`/`-Float`; `isFloat` recognizes exactly a singleton K sequence containing an injected Float; and `project:Float` is defined exactly on that projection pattern. The source program uses Float addition in its sum loop and Float subtraction followed by addition in its deviation loop, so all three domain lemmas are directly relevant to execution and the postcondition.

There are no `OPERATIONAL_RULE` entries and no `PROVED_DERIVED_LEMMA` entries. In particular, Stage 1 compiles the complete `verification.k` and only then proves `spec.k`; it never first proves one of these exact rules against a module from which that rule is absent. Every rule carrying `simplification` or `simplification(10)` is one of the definitions or domain lemmas above. See [classification evidence](/audit-output/evidence/03-independent-classification.txt).

## Stage 4 deterministic generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the three required mounted inputs. It returned `PASS`, 3 obligations, 0 designated sorries, a Stage 1 export hash of `e61a94aba6b53c03a379c0a7381a9cb6a2b5a1626d0c8a9c09bab57c47eafb11`, discovery hash `c3a5b463f6cad2bd8194d8e29587745a85c56367f69aed863cd5d75ffb7d8288`, and generated-tree hash `90e07e50612516ce0a5d5294a37dd398866ff92b0ba9716ea3f90cd23a570bc6`. Its own clean build succeeded. The returned JSON and complete diagnostics are in [preflight evidence](/audit-output/evidence/04-preflight.txt).

The source-rule/obligation map is an ordered bijection:

| Obligation | Exact source rule | Mathematical content |
|---:|---|---|
| 1 | `rule-97b32164f2b5a0f8a4f7d3358ad9ac8bcf9d1636304fa03d8f8eba850e64967e` | partial projection is defined iff the value is Float |
| 2 | `rule-92241e2e54ad3adfe5140246eafc88d12ee532fcfc8c8c2e0d517f63bee4e6d7` | guarded Float `applyBin("+")` equals injected `addF` |
| 3 | `rule-6f259967cef4b955723deaec2b3a84a45eb80e7f4eaa15e3db1588a7a25c310f` | guarded Float `applyBin("-")` equals injected `subF`, with operand order preserved |

Each recorded source span, normalized source hash, inventory hash, discovery hash, and recomputed Lean-conjunct hash matches. There are no omitted, duplicated, extra, reordered, irrelevant, or weakened obligations. The domain set is genuinely nonempty, so this is correctly not a `KLEAN_NO_OBLIGATIONS` case.

Obligation 1 contains an internal `∧ True`. This is not an inserted vacuous requirement: it is the exact typed translation of the source `#Ceil(V)` for an already typed `V : SortVal`. The surrounding projection-definedness equivalence remains discriminating—singleton Float, singleton non-Float, and multi-item K-sequence inputs produce different outcomes. Obligations 2 and 3 retain their guards, operators, operand order, injections, projections, result functions, and quantifiers. Concrete witnesses satisfy them, while the counterfactual implementations described below falsify them. The full conjuncts and their hashes are in [obligation evidence](/audit-output/evidence/06-stage4-obligations.txt).

The fixed generated target is:

```text
declaration: Klean4MeanAbsoluteDeviation.Lemmas.targetStatement
definition_sha256: 5c021c8f0c4cb38fc323789aa10d96159c82d20b4b6f7cabf3d22516570efdda
statement: Klean4MeanAbsoluteDeviation.Lemmas.targetStatement addF «applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val» isFloat projectFloat subF «project:Float?»
statement_sha256: 829c649b0060f54c7ee13f26fa9341bb89624cacc397ec3953fddee7b14ae783
```

The extracted generated target, generator manifest, and `/audit-input.json` agree exactly.

## Stage 5 clean proof and target identity

I created `/tmp/audit-work/stage5-fresh`, copied `/candidate` into it, and copied the generated project into `Base`. With the pinned Lean 4.22.0 toolchain, both `lake clean` and `lake build` exited 0. The generated `Lemmas.lean` in `Base` has SHA-256 `9038e3436875ee94e13254522d2138152e531533923f5131e7b2980f493f3dc0`, identical to the selected generation. Full output is in [clean-build evidence](/audit-output/evidence/07-clean-build.txt).

The candidate has exactly one `def` for each of the six target parameters and exactly one `Proof.final`. Its normalized theorem type is the exact fixed statement above. It neither defines nor shadows `targetStatement`. A Lean-source scan found no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.

Running Lean on `#print axioms Proof.final` produced exactly:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`, no candidate-created axiom or opaque dependency, no use of any of the 47 generated trust-inventory declarations, and no unexpected dependency. The three reported names are on the trusted foundational allowlist. See [axiom evidence](/audit-output/evidence/08-axioms.txt). The trusted final mechanical gate also returned `PASS`, reproduced the exact theorem type, and reported the same three dependencies; its deliberate `semantic_classification: NOT_EVALUATED` is supplied by the independent analysis in this review. See [mechanical-gate evidence](/audit-output/evidence/10-mechanical-gate.txt).

## Operational bridge audit

I compared every bound parameter definition to its `kore_symbol`, associated source-rule IDs, frozen verification rules, source operations, and the supplied operational semantics.

| Target parameter | Independent operational judgment |
|---|---|
| `addF` / `LbladdF` | Implements `Float.add`, matching the K rule `addF(F1,F2) => F1 +Float F2`; nonconstant witnesses were checked. |
| `applyBin` / the `LblapplyBin...` symbol | Exhaustively matches the 26 unique frozen `applyBin` cases from integer, Float, and string semantics. For the target it dispatches Float `+` and `-` to the correct injected results and operand order. Its fallback is confined to cases where frozen `applyBin` has no rule or an underlying partial integer hook is undefined. |
| `isFloat` / `LblisFloat` | Recognizes exactly the generated representation of a singleton K sequence containing an injected Float; it rejects an injected Int and a multi-item K sequence. |
| `projectFloat` / `LblprojectFloat` | Is identity on the Float constructor as required. Its totalized zero case lies outside the guarded domain; using zero on all inputs fails a generated ground instance. |
| `subF` / `LblsubF` | Implements `Float.sub`, matching `subF(F1,F2) => F1 -Float F2`; nonconstant witnesses were checked. |
| `project:Float?` / `Lblproject:Float` | Returns `some` exactly for the singleton injected-Float projection pattern and `none` for singleton Int and multi-item sequences. |

The bridge is not an arbitrary co-defined oracle: arithmetic uses concrete Lean Float operations, while the recognizer and projection inspect concrete generated constructors. The candidate also preserves relevant integer and string dispatch behavior.

An independent Lean adversarial harness evaluated 16 honest ground cases as `true`, covering Float add/subtract, the two guarded equations, integer addition and negative modulo, string concatenation, unmatched dispatch, Float recognition, total projection, and partial projection. Six isolated constant counterfactuals all evaluated `false`: constant-zero `addF`, constant-none `applyBin`, constant-true `isFloat`, constant-zero `projectFloat`, constant-zero `subF`, and constant-none partial projection each violate a concrete source obligation. See [adversarial output](/audit-output/evidence/09-adversarial.txt) and [the harness source](/audit-output/evidence/AdversarialAudit.lean).

As an additional source-side check, `krun` reached `.K` with `NoExc` and exit code 0 for the supplied smoke program, whose assertions cover the empty, singleton, and `[1.0,2.0,3.0,4.0]` mean-absolute-deviation cases. See [K smoke evidence](/audit-output/evidence/11-krun-smoke.txt).

## Sandbox infrastructure note

The first exact preflight invocation failed before examining the project because Lean 4.22 asks for `/proc/<pid>/exe`, while this audit sandbox exposes `/proc/self/exe` but not the numeric PID path. I recorded and compiled a narrow `LD_PRELOAD` shim that redirects only such `readlink` requests to `/proc/self/exe`; it does not alter Lean, K, candidate, or generated data. The shim source is [procself_readlink.c](/audit-output/evidence/procself_readlink.c). With it, the pinned Lean reports version 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and all preflight, clean-build, axiom, adversarial, and final-gate commands run successfully. This was a sandbox path-lookup workaround, not a proof or provenance exception.

VERDICT: PASS
LEGITIMACY: LEGIT
