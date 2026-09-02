# Independent audit: `146-specialFilter`

## Result

I independently audited the Stage 3 classification, deterministic Stage 4 generation, and Stage 5 Lean proof for condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. The launcher and `/audit-input.json` both select `CLASSIFICATION_AND_PROOF`.

All integrity, classification, generation, proof, axiom, and operational-bridge checks passed. The four rules classified as `DOMAIN_LEMMA` are genuine, program-relevant trust-boundary rules. Stage 4 generated one exact obligation for each of them, and `Proof.final` proves the immutable generated target with honest implementations of all nine semantic parameters and no axioms.

## Audit method and evidence

I treated the mounted workspaces, manifests, comments, logs, and earlier verdicts as untrusted evidence. Rule extraction, hashes, classifications, target comparisons, builds, and semantic checks were redone from the frozen inputs and trusted tooling. The complete command transcripts are under [`evidence/`](/audit-output/evidence/). The principal records are:

- [`02_reconstructed_inventory.log`](/audit-output/evidence/02_reconstructed_inventory.log): trusted rule-inventory output.
- [`07_independent_structural_hash_checks.log`](/audit-output/evidence/07_independent_structural_hash_checks.log): independent hashes, ordered bijections, source spans, and identities.
- [`16_fresh_klean_preflight_success.log`](/audit-output/evidence/16_fresh_klean_preflight_success.log): fresh `tools.klean_preflight.check_generation` result.
- [`17_obligations_and_generated_target.log`](/audit-output/evidence/17_obligations_and_generated_target.log): complete obligation map and target.
- [`19_isolated_candidate_clean_build.log`](/audit-output/evidence/19_isolated_candidate_clean_build.log): required fresh-copy `lake clean` and `lake build`.
- [`20_candidate_integrity_and_forbidden_scan.log`](/audit-output/evidence/20_candidate_integrity_and_forbidden_scan.log): Base identity, candidate hashes, forbidden-token scan, and shadow scan.
- [`21_print_axioms_Proof_final.log`](/audit-output/evidence/21_print_axioms_Proof_final.log): exact independent axiom report.
- [`22_trusted_full_mechanical_gate.log`](/audit-output/evidence/22_trusted_full_mechanical_gate.log): trusted final mechanical gate.
- [`24_bridge_adversarial_examples_success.log`](/audit-output/evidence/24_bridge_adversarial_examples_success.log) and [`25_counterfactual_mutation_builds.log`](/audit-output/evidence/25_counterfactual_mutation_builds.log): operational examples and mutations.

## Frozen inputs and producer provenance

The independently recomputed structural hashes matched `/audit-input.json`:

| Item | SHA-256 |
|---|---|
| canonical resolved audit input | `9d9214768295bf4908b93e0fe00bb308be4c268df7952b6a6b12b24274f2ef39` |
| Stage 1 pipeline tree | `ad42536a51b9be7f81e3255cb483f748549043d676adc4258a837836013d7e67` |
| Stage 1 export tree | `45217f43f894542f2c5938a0f53421570a2f164faeb1d46d52376055b687a11c` |
| selected Stage 2 audit tree | `019d4e990714d92d8838ae50e0e5e060e64a92030651c830dead59b874a466d2` |
| Stage 3 discovery file | `f9e267ead4719425d16a655655ad1236b3feba5baf3dacaf5af3905c86e740b8` |
| Stage 4 generation tree | `ce1b068aeaca7f9d1ab13755aa472247d273041fdbaba386df07530da5d0dbb1` |
| generated target tree | `bff3038eaeead46822f8d71c55649adc5f8a1426a6851d19a688334e3dbb7e80` |
| producer source bundle | `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e` |
| Stage 5 candidate tree | `11bf88e60e61a55a1bbe5af11d8eb0e9c49f069914edc92ec09e07830bc6bef8` |

All 790 recorded Stage 1 file hashes matched exactly.

Before judging Stage 4, I directly hashed both generation-time producers:

| Producer | SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

The two file hashes and the exact three-file producer bundle matched the source manifest, `generator-manifest.json`, and `/audit-input.json`. The immutable generator image ID also matched all three provenance paths:

`sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`.

There is therefore no producer-source infrastructure error.

## Inventory reconstruction and bijection

Using the trusted inventory implementation with `PYTHONPATH=/reference`, I reconstructed the local verification-module closure of frozen `verification.k`. The closure is exactly the single module `VERIFICATION`. It contains 23 rules, in source order, and has inventory hash:

`12d01103d80c6a489390efcbe9d1f159bccf941a293215593306572eb7a48336`.

For every rule, I recomputed the source span, normalized text hash, and `source_rule_id`. The ordered list is:

| # | Lines | Recomputed identity | Independent class |
|---:|---:|---|---|
| 0 | 8–31 | `rule-415fd1ad47bbd9592fe0bc3347c631bc989d2b9a7b8ff6b61fe66f8e47b2c03f` | `DEFINITION` |
| 1 | 34–39 | `rule-9d27a81e40c58ebe05874d4adb1e888533322d5b70991a2c1e9eee4699e7a495` | `DEFINITION` |
| 2 | 43 | `rule-8277b118773512287e2b2b20da4dbf45607f85956623bafa9028b50596471d08` | `DEFINITION` |
| 3 | 44–45 | `rule-fa394f9b181c0d7a89141e7d4e865895db0443da2d399ebaeb0492e3a9b63ed4` | `DEFINITION` |
| 4 | 51 | `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5` | `DEFINITION` |
| 5 | 56–58 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | `DOMAIN_LEMMA` |
| 6 | 60–62 | `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0` | `DEFINITION` |
| 7 | 63–65 | `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d` | `DOMAIN_LEMMA` |
| 8 | 67 | `rule-6af2af3333ef4c545e9fa962d5a6a41f10d5a21d3b53f046c5a85b21fabfe502` | `DEFINITION` |
| 9 | 68–70 | `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081` | `DEFINITION` |
| 10 | 74–77 | `rule-b16fd6610afeba9b173c4b9ae74c4766789b5284e03220a93a65bb86fd2ce505` | `DOMAIN_LEMMA` |
| 11 | 79–82 | `rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d` | `DOMAIN_LEMMA` |
| 12 | 88–89 | `rule-23265a9d293bd576a32766c0e55fa4981f126101f0e0d7690761db7ffcb2511d` | `DEFINITION` |
| 13 | 90–93 | `rule-3f693acbe30326ded85fe4006a1d92ccd6733a56cc235cd3362184e45e6e0d03` | `DEFINITION` |
| 14 | 98–99 | `rule-974792a28f9b7a63655bcdf632d17b799ff47d88f98edb17cfbda11da0b4e134` | `DEFINITION` |
| 15 | 100–101 | `rule-2c02dd94194fee46825cab7bb678d5ce9b78d9fd35922d845a511aac67c002b9` | `DEFINITION` |
| 16 | 102–105 | `rule-b7bc811f77603533c8a84ab371982791a09f666627712b97a86c9485df7ca00d` | `DEFINITION` |
| 17 | 109 | `rule-263170eeee79c9fa6bcc877a8f7a4a1f10d0f88ea601d2e6d7d17a11a2e7dd6a` | `DEFINITION` |
| 18 | 110–116 | `rule-d972de31aae78be4a6fb8338a082189d7c2e15b41b89c0773f9772965d576d23` | `DEFINITION` |
| 19 | 117–121 | `rule-26da31847512880d0540245b0754633d04890594e3b53b5c3ef24bc167782924` | `DEFINITION` |
| 20 | 122–127 | `rule-afb214b6a9bf2e42a13be20b529fce2ebe6d3ca1a335dce3ce37190f50890458` | `DEFINITION` |
| 21 | 128–134 | `rule-2e05f3a96a7a035d681bbfa13334d88944a91d898ef048576709ac3a01770e43` | `DEFINITION` |
| 22 | 135–138 | `rule-df7473fc4632d0a69cd067dbf602701426b0e1948899340451f8a6ff743fbc83` | `DEFINITION` |

This reconstruction is bijectively identical to `lemma-discovery.json`: same count, unique identities, source order, spans, normalized hashes, attributes, texts, and inventory hash. There are no omitted, duplicated, extra, reordered, or unaccounted rules.

## Independent classification judgment

I did not accept the manifest labels merely because the reconstruction matched.

The 19 `DEFINITION` entries genuinely define named syntax or proof summaries:

- `filterBody` and `specialFilterStmts` are exact macros for the frozen source program.
- `allInts` is the contract-domain recurrence.
- `definedProjectInt` and the concrete/normalization rules for `projectIntTotal` define the named guarded total projection. The idempotence rule normalizes the same named proof term; it is not a fact about the source program smuggled in under another symbol.
- `firstDecimalCode`, `lastDecimalCode`, `firstDigitOdd`, `lastDigitOdd`, and `isSpecial` are named summaries of the source predicate.
- The six `specialCount` rules are the base case and exhaustive recurrence branches for the mathematical result summary.

None of these 19 is an ordinary language-execution rule, and none asserts an independent domain theorem about an existing semantic operator.

The remaining four rules are correctly classified as `DOMAIN_LEMMA`:

1. Lines 56–58 characterize definedness of the pre-existing partial `Val`-to-`Int` cast.
2. Lines 63–65 replace that partial cast by `projectIntTotal` under the integer guard.
3. Lines 74–77 bridge dynamic `applyCmp(">", V, I)` to integer comparison under the same guard.
4. Lines 79–82 bridge dynamic `applyBuiltin("str", V, .Vals)` to decimal integer string construction under the guard.

These are not definitions of the pre-existing cast, comparison dispatcher, or builtin dispatcher. Stage 1 compiles them into `VERIFICATION` before proving its claims; it does not first prove any exact rule against a module that omits that rule. Thus none qualifies as `PROVED_DERIVED_LEMMA`. They are also not ordinary `OPERATIONAL_RULE` entries from the supplied language semantics.

All four domain lemmas are relevant. The frozen function checks `num > 10`, calls `str(num)`, and inspects the first and last decimal character. Its quantified input is represented by dynamically sorted `Val` elements constrained by `allInts`, so the cast-definedness and guarded dispatch bridges are exactly the facts needed to connect those elements to the supplied operational rules. There is no irrelevant domain lemma.

Every rule carrying `simplification` or `simplification(...)` is independently classified as either `DEFINITION` or `DOMAIN_LEMMA`. No simplification rule is mislabeled as operational or previously proved.

The operational source confirms the bridge meanings: `Val` includes `Int`; integer `applyCmp(">")` reduces to `>Int`; `applyBuiltin("str", I, .Vals)` reduces through `Int2String` and `strToCodes`; and string code sequences are character codes. The frozen Python body and K macro both implement the same count: integers greater than 10 whose first and last decimal characters have odd character codes. Negative and boundary values remain governed by the same decimal-string behavior.

## Deterministic Stage 4 generation

I reran:

`tools.klean_preflight.check_generation("/reference/k-proof", "/reference/lemma-discovery.json", "/reference/klean-generation")`

with `PYTHONPATH=/reference`. The fresh result is `PASS`, with four obligations, no designated `sorry`, generated tree hash `bff3038eaeead46822f8d71c55649adc5f8a1426a6851d19a688334e3dbb7e80`, and successful clean/build diagnostics.

The sandbox prevents Lean's ordinary `/proc/<pid>/exe` lookup. The first preflight therefore failed before checking the project. I recorded that environment failure, then used a narrow audit-local `LD_PRELOAD` shim which only supplies the kernel `AT_EXECFN` result for `/proc/*/exe` `readlink` calls. The pinned Lean binary reported version 4.22.0 and commit `ba2cbbf588db76c01b4c7b3ce49c32879e349b27`. The successful preflight and all subsequent Lean commands used that same pinned toolchain. The shim does not alter sources, Lean elaboration, proof checking, hashes, or command results.

There is an exact ordered source-rule/obligation bijection:

| Domain rule | Generated mathematical obligation |
|---|---|
| `rule-031285…` | The partial `project:Int?` succeeds exactly when `definedProjectInt V = true`; the source's additional `#Ceil(V)` is true because `V` already has the total algebraic sort `Val`. |
| `rule-22fa1e…` | Under `definedProjectInt V = true`, `project:Int` of the injected K term equals `projectIntTotal V`. |
| `rule-b16fd…` | Under the guard, dynamic `applyCmp ">" V (inj Int I)` equals `projectIntTotal V >Int I`. |
| `rule-532e…` | Under the guard, dynamic one-argument `str` equals the injected string of the decimal character codes of `projectIntTotal V`. |

The first generated conjunct contains an inner `∧ True`. This is not an inserted vacuous replacement for a domain obligation: it is the exact typed Lean image of the source rule's explicit `#Ceil(@V)`. Since `@V : Val`, that source subcondition is itself tautological. The other side of the equivalence remains the non-vacuous cast-definedness condition. No whole domain lemma, top-level target conjunct, or source condition was weakened to `True`.

There are four unique domain identities and four unique obligations, with exact per-conjunct hashes. No obligation is irrelevant, weakened, omitted, duplicated, or replaced by a vacuous theorem.

The fixed target is:

- declaration: `Klean146Specialfilter.Lemmas.targetStatement`
- file: `Klean146Specialfilter/Lemmas.lean`
- definition SHA-256: `07cd0a74b5f49bcd9bacbaa3914a1fd08a2f75c52af70bdc2772bb5ddcaa53ef`
- instantiated statement SHA-256: `370d889c97e5bf8cfa7b7c2a7ff4afb6ccaaf5a6f99202b1e1e581ecf92cfbb3`

The complete target object—including the declaration, statement, all nine ordered parameters, their types, KORE symbols, source-rule IDs, and binding hashes—is identical in `generator-manifest.json`, the preflight record, both audit-input locations, the generated source, and the fresh proof workspace.

## Fresh Stage 5 proof audit

I created `/tmp/audit-work/146-specialfilter-proof-audit` from scratch, copied the generated project into it as `Base`, and copied only the candidate proof project files alongside it. I then ran both required commands:

- `lake clean`: exit 0.
- `lake build`: exit 0; `Proof` and the immutable target module built successfully.

After the build, the copied `Base` tree still had the exact generated hash `bff3038eaeead46822f8d71c55649adc5f8a1426a6851d19a688334e3dbb7e80`. Candidate source hashes matched the mounted candidate. The candidate does not declare or shadow `targetStatement`; its only occurrence is the exact type of `Proof.final`. A candidate-owned scan found no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`.

`Proof.final` has exactly the fixed target statement, with the same nine parameters in the same order. It proves the four conjunctions of that target directly; it does not introduce a duplicate or weaker theorem.

The trusted final mechanical gate also returned `PASS`, including its own fresh preflight, clean proof build, exact target check, and axiom audit. Its `semantic_classification` field is intentionally only `NOT_EVALUATED`; the independent semantic assessment is supplied in this review rather than inferred from that structural gate.

## Axiom accounting

In the fresh workspace I created an audit file containing only:

```lean
import Proof
#print axioms Proof.final
```

The exact Lean output was:

```text
'Proof.final' does not depend on any axioms
```

The exit status was 0. The used dependency set is therefore empty and is trivially a subset of the 50 declarations recorded by `trust-inventory.json`. In particular, there is no `sorryAx` and no recorded or unrecorded proof trust escape.

## Operational bridge audit

I independently located each of the nine exact candidate `def`s bound by `target.parameters` and compared it with its KORE symbol, source-rule IDs, frozen verification rules, source solution, and the supplied operational K semantics:

| Parameter | Candidate meaning | Independent judgment |
|---|---|---|
| `_>Int_` | Lean integer `left > right` | Exact total K integer comparison. |
| `Int2String` | `toString value` | Exact signed decimal representation needed by K's integer-to-string operation; checked at `-73`, `0`, and `109`. |
| `strToCodes` | recursive `Char.toNat` conversion | Exact character-code sequence; `-73` produced `[45,55,51]`, and `109` produced `[49,48,57]`. |
| `definedProjectInt` | true only for `SortVal.inj_SortInt` | Exact definedness predicate for the guarded cast; false on Boolean and string adversaries. |
| `project:Int?` | `some n` only for the exact injected integer K term | Exact partial projection; returned `some (-73)` for the integer injection and `none` for a Boolean injection. |
| `project:Int` | the same projection with a default outside its domain | Exact on every guarded use. The default is unreachable in the generated rule obligation and does not claim semantics for an undefined source cast. |
| `projectIntTotal` | extracts an injected integer; default outside the guarded domain | Exact on the domain required by all three linked rules, including `109 ↦ 109`. The off-domain default is never used under `definedProjectInt = true`. |
| `applyCmp` | integer comparison on integer injections, plus compatible additional cases | Its relevant `">"` integer branch exactly dispatches to the same comparison. Tests at `11/10`, `10/10`, and `-73/10` gave true, false, and false. |
| `applyBuiltin` | the `"str"`/single-integer branch returns the injected decimal-code string | Exact relevant builtin dispatch for both negative and positive integers; direct `rfl` checks matched manually constructed code sequences. |

The tests cover the critical boundary at 10, a qualifying positive value, a negative value with a sign character, zero, non-integer `Val` constructors, successful and failed projections, and concrete decimal code lists. These examples are adversarial to constant, identity, unsigned-only, missing-sign, always-defined, and convenient-default implementations.

I also performed counterfactual mutation builds. Replacing `_>Int_` by constant false caused the proof build to fail at the comparison obligation, as expected. Replacing both `Int2String` and `strToCodes` by mutually convenient constants still allowed the equation-only target to build; that demonstrates why the independent operational-bridge audit is necessary. The submitted candidate does not use those mutations: its definitions implement signed decimal conversion and character-code construction, and the adversarial results above confirm their operational meaning. Thus the target's parameterization does not create an operational-bridge failure in this candidate.

## Final judgment

The protected Stage 3 classification matches the independently reconstructed inventory and the semantic role of every rule. The four true domain lemmas are complete and relevant. Deterministic Stage 4 generation has authenticated producer provenance, an exact four-to-four rule/obligation bijection, and an unchanged fixed target. The Stage 5 project builds from a fresh copy, proves exactly that target, uses no axioms or forbidden trust escapes, and supplies honest operational implementations for every target parameter.

VERDICT: PASS
LEGITIMACY: LEGIT
