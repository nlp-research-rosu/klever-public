# Independent audit: HumanEval 108-count-nums

## Result

I independently audited Stage 3 lemma classification, deterministic Stage 4 generation, and the Stage 5 Lean proof for condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`. The launcher and environment both selected `CLASSIFICATION_AND_PROOF`.

The protected classification is complete and mathematically appropriate: the local verification-module closure contains 29 rules, of which 24 are genuine definitions and five are genuine, relevant domain lemmas. Stage 4 generates exactly one faithful obligation for each domain lemma and preserves the fixed target. The candidate clean-builds from a fresh assembly, proves that exact target without a project trust escape, and implements every target parameter consistently with its bound KORE symbol and the frozen operational meaning.

## Audit boundary and input integrity

I treated all mounted candidate, provenance, log, review, and comment content as untrusted evidence. Judgments below come from the frozen source, trusted inventory/preflight/final-gate code, fresh builds, direct inspection, and new adversarial tests.

The launcher resolution hash is `4027fe52e7c959486a64145265ef1239009f824964c680abff8ff5152197a61c`. The recorded mode and `AUDIT_MODE` both equal `CLASSIFICATION_AND_PROOF`. Independent tree/file hashing matched every available recorded value:

| Input | Observed and recorded SHA-256 |
|---|---|
| Stage 1 K pipeline workspace | `4817cd494240566a67a8dec838fbc5ad4ae18ab19af49eb5fbde283cd71510d6` |
| Stage 1 exported K workspace | `0b9500be5f09a202d093efad9f8c820dad7639990a3e7d69afd52dff5c55e346` |
| selected Stage 2 K audit | `439df0104dcad892aa05e60ab5dd6ddd54ae984557d85909a7275006d2afc742` |
| Stage 3 discovery manifest | `77be13d6ea2a48897fe1570e3a22e3540f58569c942222ef4c0ef019e242355e` |
| Stage 4 generation tree | `91f8b1a8f67f47f0af985f13e1dbdddf17ed445c5603e30305244025234d3dea` |
| Stage 4 generated project | `d07328eaa869c701a22c42ff7e8ae010ea0e3563e97ad614857c607e1c9b90e8` |
| generation producer-source tree | `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e` |
| Stage 5 candidate tree | `5e2c752f77246989ab9797b7a4a1782102cb88fe3946f849729ab7e8b7f70251` |

All 815 recorded Stage 1 per-file hashes matched, with no missing or extra file. Full reconstructed inventory and hash evidence is in [02-independent-inventory-and-hashes.log](/audit-output/evidence/02-independent-inventory-and-hashes.log).

## Generator producer provenance

I checked the required producer files before judging Stage 4:

| Producer | Observed SHA-256 |
|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` |

These hashes match the producer source manifest, `generator-manifest.json`, and the producer tree selected in `/audit-input.json`. The immutable generator image ID is identically recorded as `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6`; the selected producer-source path in the audit input is keyed by the same image digest. There is no producer-provenance infrastructure error. Raw evidence is in [01-producer-provenance.log](/audit-output/evidence/01-producer-provenance.log).

## Independent rule reconstruction and classification

Using the trusted rule-inventory implementation on the frozen Stage 1 `verification.k`, I reconstructed the complete local verification-module closure. It contains only the local module `VERIFICATION`; imported language modules are not local verification modules. The frozen `verification.k` SHA-256 is `a6a57397f1b7f6b856df6012dcde84159e0506d8875f11edbc0f76579f1f57c0`. The reconstruction produced 29 rules and inventory SHA-256:

`86637211d8eb42b498d51f829d1bcd21ab5987f93b26ba91a4a35193e5b3824b`

For every rule, the trusted inventory output independently recovered its module, exact source span, source text, attributes, normalized source hash, and `source_rule_id`. Comparing the ordered reconstruction with `lemma-discovery.json` was bijective: 29 versus 29 entries; identical order and identities; no omitted, duplicated, extra, or changed rule; and no unaccounted classification.

### Definitions

The following 24 entries genuinely define new summaries, structural recurrences, macros, or named proof terms:

| Source lines | Defined object and judgment |
|---|---|
| 10, 11–12 | base and recursive equations for `allInts` |
| 19, 28–30, 31–33, 34, 35–37 | `definedProjectInt` and the guarded `projectIntTotal` proof-term/cast normalization equations |
| 51, 52 | negative and nonnegative equations for `magnitude` |
| 59–61 | proof-side naming equation `strToCodes(Int2String(N)) => decimalCodes(N)` |
| 70, 71–72 | base and recursive equations for `allDigitCodes` |
| 81, 82–83 | base and recursive equations for `codeDigitSum` |
| 87, 88–89, 90–93 | the complete `chooseFirst` recurrence |
| 96, 97 | the complete `lastCode` recurrence |
| 100–103, 104–106 | negative and nonnegative equations for `signedDigitSum` |
| 109, 110–114, 115–117 | base, integer-head, and non-integer-head equations for `countNumsSpec` |

The `decimalCodes` naming rule does not assert the value-level digit property; that separate property is correctly treated as a domain lemma below. The projection equations define and normalize a new named proof term only under its definedness guard; they do not create an unconditional cast fact.

### Domain lemmas

The remaining five rules are neither ordinary operational rules nor proved-derived lemmas:

| Frozen span and identity | Independent classification and relevance |
|---|---|
| 24–26, `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | `DOMAIN_LEMMA`: characterizes definedness of the partial `Val`-to-`Int` cast. It is required when list iteration yields dynamically sorted `Val` values. |
| 41–44, `rule-f0bc44c15424da687bfa0aeb3e970f71a2cc9dbd9a38c4ac04629f27cea4ac69` | `DOMAIN_LEMMA`: guarded dynamic-to-static bridge for source comparisons `num < 0`. The supplied Int rule reduces `applyCmp("<", I, J)` to `I <Int J`. |
| 45–48, `rule-dd0c5a6695115ef6c4608553ba13c7b4e2cd91e78ce50bf59e458ba0a5eb5be2` | `DOMAIN_LEMMA`: guarded dynamic-to-static bridge for source unary `-num`. The supplied Int rule reduces it to `0 -Int I`. |
| 63–67, `rule-96422d110466a9240b0e25343046e54b8fa06a0bdf0abc4c25fcd195583f54da` | `DOMAIN_LEMMA`: guarded dynamic `str` bridge. The supplied builtin maps an Int to `str(strToCodes(Int2String(I)))`; the definition at lines 59–61 names that result `decimalCodes(I)`. This is used by `for char in str(n)`. |
| 76–78, `rule-5af48b88759940f404acea3042b6fa69d00290648ae1c95910aaad61bea89344` | `DOMAIN_LEMMA`: value-level contract that nonnegative decimal encodings contain only ASCII digit codes. It directly discharges the guard for the source `int(char)` rule, whose supplied semantics requires codes 48 through 57. |

Every Stage 1 claim in `spec.k` imports `VERIFICATION`, and `validation.k` does as well. There is no earlier exact proof of any of these five rules against a module omitting the rule, so none qualifies as `PROVED_DERIVED_LEMMA`. Conversely, none is an ordinary execution/observation equation already supplied by the operational semantics, so none qualifies as `OPERATIONAL_RULE`. All rules bearing `simplification` or `simplification(10)` are among the definitions or domain lemmas above.

The five domain lemmas are all tied to the frozen solution: dynamic integer cast, sign comparison, unary negation, `str(n)`, and the digit guard for `int(char)`. No irrelevant lemma was selected. The frozen source and operational-rule excerpts are captured in [12-source-operational-semantics.log](/audit-output/evidence/12-source-operational-semantics.log).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and exactly the requested K workspace, discovery manifest, and generation directory. The audit sandbox initially hid `/proc/<pid>/exe`, which prevented the pinned Lean launcher from discovering its installation; this environmental attempt is preserved in [03-klean-preflight-check-generation.log](/audit-output/evidence/03-klean-preflight-check-generation.log). I then used a narrowly scoped `readlink` compatibility shim that redirects only `/proc/<digits>/exe` to `/proc/self/exe`. Its source and binary hashes and the recovered pinned versions—Lean 4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, Lake 5.0.0—are recorded in [00-lean-launcher-shim.log](/audit-output/evidence/00-lean-launcher-shim.log). The shim changes neither source nor proof behavior.

The rerun returned `PASS`, clean-built the generated project, found zero designated sorries, and reported exactly five obligations. Complete returned evidence is in [04-klean-preflight-check-generation-rerun.log](/audit-output/evidence/04-klean-preflight-check-generation-rerun.log).

I independently compared the Stage 3 domain set, Stage 4 `source_rules`, and Stage 4 `obligations`. The three ordered identity lists are exactly equal and unique:

1. cast definedness, lines 24–26;
2. dynamic `<`, lines 41–44;
3. dynamic unary `-`, lines 45–48;
4. dynamic `str`, lines 63–67;
5. nonnegative decimal digit property, lines 76–78.

The generated obligations faithfully state, respectively:

1. partial projection is defined exactly when `definedProjectInt` is true;
2. guarded dynamic `<` equals projected integer `<`;
3. guarded dynamic negation equals `0 - projectIntTotal(V)`;
4. guarded `str(V)` equals the string constructed from `decimalCodes(projectIntTotal(V))`;
5. nonnegative `decimalCodes(N)` satisfies `allDigitCodes`.

There are no omissions, duplicates, irrelevant obligations, changed guards, changed right-hand sides, or target changes. The first generated conjunct contains `∧ True` because the source right-hand side contains `#Ceil(@V)` and `V` is already a typed `SortVal`; that subterm's translation is tautological. The obligation itself is not vacuous: it retains the substantive biconditional between partial-cast definedness and `definedProjectInt(V) = true`. None of the five conjuncts is merely `True`, and none can be discharged without implementing its substantive relation.

The obligation-map file hash is `ccabc697c6aadd3b96999b806b7c135054eec70f7e439cdfb6e875edc440b230`, exactly the manifest value. Detailed statements and the independent ordered-bijection result are in [13-target-bijection-candidate-integrity.log](/audit-output/evidence/13-target-bijection-candidate-integrity.log).

### Fixed target identity

The generated target is identical in the generated file, generator manifest, preflight result, and audit input:

| Field | Fixed value |
|---|---|
| declaration | `Klean108CountNums.Lemmas.targetStatement` |
| file | `Klean108CountNums/Lemmas.lean` |
| definition SHA-256 | `70f1d88809dcc5ae4f0d283099e5dae878c4385dad1fa0e44959bce6562ed6b4` |
| statement SHA-256 | `f41037e06fc1909c2283b8fa272875c5f8f536e51ff4b915280347c2c4a38188` |
| parameter count | 13 |

The selected status is not `KLEAN_NO_OBLIGATIONS`; the independently established domain set is nonempty and is correctly represented by five generated obligations.

## Stage 5 Lean proof

I assembled a fresh project at `/tmp/audit-work/108-count-nums-proof.Iop7KI`, copied the generated project into it as `Base`, and ran both `lake clean` and `lake build`. Both exited zero. The full command transcript is [05-fresh-candidate-clean-build.log](/audit-output/evidence/05-fresh-candidate-clean-build.log).

The candidate has one `Proof.final` declaration. Its statement is textually the fixed 13-argument target application after whitespace normalization. It neither declares nor shadows `targetStatement`. Each target parameter has exactly one public candidate definition, and the parameter names, types, KORE-symbol associations, binding hashes, and `source_rule_ids` agree with the generator manifest. A source scan found no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque` in `Proof.lean`.

### Axiom accounting

A fresh `#print axioms Proof.final` produced exactly:

`[propext, Classical.choice, Quot.sound]`

There is no `sorryAx`. The 43 custom generated declarations recorded in `trust-inventory.json` are the complete possible project-specific generated trust boundary, but none appears in `Proof.final`'s dependency list. The three reported names are Lean's standard logical/library foundations and are accepted by the trusted final-gate policy; they are not unrecorded candidate declarations. Thus every reported dependency is reconciled: zero unrecorded project axiom, zero generated Klean axiom used, and three standard Lean dependencies. Exact output is in [06-print-axioms.log](/audit-output/evidence/06-print-axioms.log), and the trusted end-to-end reconciliation is in [11-trusted-final-gate.log](/audit-output/evidence/11-trusted-final-gate.log).

### Operational bridge audit

I inspected every public definition bound by `target.parameters`, rather than treating target provability as sufficient:

| Parameter(s) | Candidate meaning versus frozen K meaning |
|---|---|
| `«_-Int_»` | integer subtraction `a - b`, matching `INT.sub` and the unary-negation right-hand side |
| `_andBool_` | Boolean conjunction `a && b`, matching the K Boolean hook |
| `«_>=Int_»`, `«_<Int_»` | Lean integer order, matching the `INT.ge`/`INT.lt` hooks and source guards |
| `«allDigitCodes(_)…»` | structural recursion accepting exactly codes 48–57, matching lines 70–72 |
| `«applyBuiltin(_,_)…»` | its relevant `("str", [Int])` branch returns `str(decimalCodesImpl(i))`, matching supplied `strToCodes(Int2String(i))`; the implementation is a real dispatcher, not a constant |
| `«applyCmp(_,_,_)…»` | its relevant `("<", Int, Int)` branch computes integer less-than, matching `int.k:22` |
| `«applyUn(_,_)…»` | its relevant `("-", Int)` branch returns injected `0 - i`, matching `int.k:7` |
| `«decimalCodes(_)…»` | actual sign-aware base-10 encoding: zero is `[48]`, nonnegative digits are produced most-significant first, and negatives are prefixed by code 45; the source program uses its nonnegative branch after `magnitude` |
| `«definedProjectInt(_)…»` | true exactly for the `SortVal.inj_SortInt` constructor |
| `isInt` | true exactly for the K sequence consisting of an injected integer followed by `.dotk` |
| `projectIntTotal` | returns the underlying integer on the guarded Int constructor; its fallback `0` is unreachable in every source obligation, matching the guarded proof-term definition |
| `«project:Int?»` | returns `some i` exactly for the corresponding injected Int K value and `none` otherwise |

Fresh executable Lean assertions exercised negative and positive subtraction; Boolean truth cases; order boundaries; empty, boundary, and rejected digit codes; integer versus string cast observers; partial and total projections; dynamic comparisons and negation; decimal encodings for `0`, `7`, `10`, `101`, `908`, `-12`, and `1234567890123456789`; and dynamic `str` for `0` and `908`. They also type-checked `Proof.final` at the exact target. The corrected adversarial suite exited zero in [08-operational-adversarial-tests-rerun.log](/audit-output/evidence/08-operational-adversarial-tests-rerun.log). The earlier [07-operational-adversarial-tests.log](/audit-output/evidence/07-operational-adversarial-tests.log) records only a superseded test-harness issue: equality was first asked of types without `DecidableEq`; it was corrected to their derived `BEq` observer.

As a counterfactual, I changed `decimalCodesImpl` to return the constant code sequence `[48]` and adjusted only its local all-digits proof. That coordinated but operationally false implementation still clean-built and proved the parameterized equation, demonstrating why target provability alone is insufficient. The same adversarial suite then rejected every nonzero decimal witness and the corresponding `str(908)` result. The exact diff and outcomes are in [10-counterfactual-constant-decimal-rerun.log](/audit-output/evidence/10-counterfactual-constant-decimal-rerun.log). The mounted candidate is not that counterfactual: it implements the real decimal conversion and passes all witnesses. The initial unadjusted mutation attempt in [09-counterfactual-constant-decimal.log](/audit-output/evidence/09-counterfactual-constant-decimal.log) is superseded by the coordinated counterfactual.

This counterfactual does not expose a Stage 4 source-rule omission: Stage 4 exactly translates the five frozen domain lemmas. It exposes the intended separate trust question for parameter implementations, which the mounted candidate passes under direct source comparison and adversarial evaluation.

## Mechanical gate reconciliation

The trusted final gate independently repeated generation preflight, a clean proof build, exact theorem printing, target identity checks, trust-inventory checks, and axiom printing. It exited zero with overall status `PASS`, exact target hashes, five obligations, and used axioms `[Classical.choice, Quot.sound, propext]`. Its reported `semantic_classification` is `NOT_EVALUATED`, as expected: the mathematical classification and operational-bridge judgments are supplied by the independent analysis above, not delegated to the structural gate.

No prior PASS, prior review conclusion, or protected rationale was used as authority. On the frozen source and semantics, the Stage 3 classification is sound, Stage 4 is deterministic and bijective, and the optional Stage 5 proof is an exact, clean, operationally faithful proof of the fixed target.

VERDICT: PASS
LEGITIMACY: LEGIT
