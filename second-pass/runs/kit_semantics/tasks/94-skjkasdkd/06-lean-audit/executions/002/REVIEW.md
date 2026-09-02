# Independent audit: HumanEval `94-skjkasdkd`

## Scope and result

I independently audited Stage 3 lemma classification, deterministic Stage 4 generation, and the Stage 5 Lean proof for condition `kit-semantics` under `SUPPLIED_SEMANTICS`. Both `AUDIT_MODE` and the signed resolution in `/audit-input.json` select `CLASSIFICATION_AND_PROOF`. I treated all candidate/provenance prose, prior verdicts, and comments as untrusted evidence.

The audit found an exact 33-rule Stage 3 inventory, a mathematically correct partition into 20 definitions and 13 domain lemmas, a bijective 13-obligation Stage 4 target, and a clean Stage 5 proof whose operational bindings are faithful to the frozen program. No infrastructure provenance error or proof-legitimacy failure remains.

The raw evidence index is `evidence/README.md`; `evidence/final-gate-summary.log` records zero exit codes for the authoritative gates.

## Launcher and immutable-input binding

The launcher records:

- mode `CLASSIFICATION_AND_PROOF`;
- problem `94-skjkasdkd`;
- condition `kit-semantics`;
- semantics mode `SUPPLIED_SEMANTICS`.

I recomputed the signed resolution envelope hash as `5f4421814ce79891d86b0bf94561ed4b358b4453a594742f9bbd4a51d5ea3ec9`. The independently reimplemented launcher and Klean tree algorithms matched every mounted binding: Stage 1 pipeline tree `53fd561b800d737819075b7efb0043e3993fd95d7b42ef0a5a4a8d3a98ab9236`, Stage 1 export tree `a479ffc26d0888a54bafb361e930785a3b05365b6aba1bdcd36c5437b2e6b324`, Stage 2 audit tree `1cf76d2d01a854916f41b84ddc178b75fb71c815d6cc63c378383cf78af2ac84`, discovery file `96e36beab2d7540a7fb8eb90be52dc480a387490a00e35df62c753a106123002`, Stage 4 pipeline tree `50df09411ef6a7073de5a0412f26766b9246addac343a9e03f8b0a346e731075`, generated tree `d39652423da4b22eeaa43a473205673f746e535ba4d94082c472acd874151e0e`, producer-source tree `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e`, and candidate tree `6a65652395d1fc1655ca2a7353df9447e7cb7c8ea3068a4fcd726e174d7f9fd7`. The complete Stage 1 per-file hash map also matches bijectively.

The signed Stage 5 invocation digest is `52b9ba1b60b87c081d2cb02f6c44784809b2eb014e9077b08122783d349e46dd`; the invocation directory is not an audit mount named by the supplied contract, so that directory digest cannot be independently traversed here. This does not affect proof judgment: the mounted successful workspace is present, its launcher hash matches exactly, and it was rebuilt from clean state below `/tmp/audit-work`. See `evidence/stage4/independent-generation-audit.log` and `evidence/stage5/candidate-integrity-check.log`.

## Stage 4 producer authentication

Before judging generated content, I hashed the exact generation-time sources:

- `klean_export.py`: `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752`;
- `klean.py`: `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346`.

Both hashes agree with `source-manifest.json` and `generator-manifest.json`. The generator image ID is consistently `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6` in the source manifest, generator provenance, and the producer bundle component recorded in `/audit-input.json`. The producer bundle contains only the two sources and its source manifest, and its launcher tree hash matches. Therefore the infrastructure `AUDIT_ERROR` condition is not triggered. Evidence: `evidence/stage4/producer-authentication-corrected.log`.

## Stage 3 inventory reconstruction

I reran the trusted local rule inventory on frozen `/reference/k-proof/verification.k`. The selected verification module is `VERIFICATION`; its local verification-file closure is exactly `[VERIFICATION]` because `MPY` is supplied by the external semantics. Reconstruction produced 33 unique rules in source order, with:

- frozen `verification.k` SHA-256 `afc958d30c5d5c7578833f6f3a2373699d3fcff4c3b670d6af75e76bbf4d61ba`;
- canonical inventory SHA-256 `1858c992ef1e9a6b842e6b7d36b1e30b8abe0e686374e68b1766d4f9cb1e3824`.

For every entry I independently sliced the recorded line span from the source, normalized whitespace, recomputed the normalized SHA-256, rebuilt `source_rule_id = "rule-" + normalized_sha256`, and recomputed the whole canonical inventory hash. The protected discovery manifest has exactly the same 33 unique IDs, in exactly the same order, with no omission, duplicate, extra entry, hash change, or unaccounted classification. Full reconstructed records are in `evidence/stage3/reconstructed-inventory.json`; the per-entry checks are in `evidence/stage3/inventory-bijection.log`.

## Stage 3 independent classification

My classification is 20 `DEFINITION`, 13 `DOMAIN_LEMMA`, 0 `OPERATIONAL_RULE`, and 0 `PROVED_DERIVED_LEMMA`, exactly matching the protected manifest. The complete 33-row independent decision table, with full IDs and spans, is `evidence/stage3/independent-classification.md`.

The 20 definitions are genuine named macros or recursive summaries: four exact translated-body macros; the two `allInts` equations; the named projection-definedness and guarded projection equations; three primary/base `primeTail` equations; `isPrime`; the two `selectPrime` equations; three `largestPrime` equations; and the two defining `digitSum` equations. They do not assert independent facts merely under a definitional label.

The 13 domain lemmas are exactly:

1. cast definedness (lines 74–76);
2. reverse cast/projection (82–84);
3. projection idempotence (87–89);
4. three specialized comparison dispatch bridges (93–106);
5. two specialized binary dispatch bridges (108–116);
6. two `primeTail` shortcuts/folds (133–142);
7. three `digitSum` reverse/normalization/accumulator folds (174–191).

They are not ordinary execution rules: the fixed semantics already supplies `BinOp`/`Compare` evaluation through `applyBin`/`applyCmp`, and `semantics/int.k` supplies the underlying integer operations. They are not definitions because they are reverse equations, idempotence facts, dispatch bridges, or derived folds rather than primary named recurrences. They are not `PROVED_DERIVED_LEMMA`: inspection of the actual Stage 1 command sequence shows every `kprove` uses `verification-kompiled`, and every spec requires `verification.k`; Stage 1 never first proves the exact rule in a module that omits it and then uses it later. Evidence: `evidence/stage3/stage1-proof-sequence-inspection.log`.

All rules bearing `simplification` are classified as `DEFINITION` or `DOMAIN_LEMMA`. Every domain lemma is relevant: projection/dispatch bridges connect the dynamically typed `Val` list to integer execution; `primeTail` folds summarize the divisor loop; and `digitSum` folds summarize the decimal accumulator loop. Each is directly tied to the source program and postcondition `digitSum(largestPrime(VS, 0))`.

## Stage 4 preflight, bijection, and target identity

I reran the required call to `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`, `/reference/k-proof`, `/reference/lemma-discovery.json`, `/reference/klean-generation`, and the trusted lock. It returned `PASS`, 13 obligations, zero designated sorries, and a successful fresh generated-project build. Complete returned evidence is `evidence/stage4/check-generation-proc-compat.log`.

The container exposes host `/proc` while Lean runs inside a PID namespace, so unmodified Lean 4.22 initially looked for a nonexistent `/proc/<namespace-pid>/exe` and Lake could not locate its application. I retained that failed diagnostic. For the authoritative rerun I copied the pinned `libleanshared.so` under `/tmp/audit-work` and changed only the four-byte address operand in `lean_io_app_path` from its `/proc/%d/exe` string to the library's existing `/proc/self/exe` string. The original toolchain and every audit input remained untouched. The resulting executable still identifies exactly as Lean 4.22.0, commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`; the patch affects application-path discovery, not parsing, elaboration, kernel checking, or generated source. The byte-level record and successful pinned build are in `evidence/stage4/proc-self-toolchain-fix-test2.log`.

Beyond preflight, I independently rebuilt all Stage 4 structural commitments. The 13 independently classified domain IDs equal, in source order, the 13 `input-manifest.source_rules`, 13 `obligation-map.source_rules`, and 13 obligation IDs. All are unique. Every obligation carries the exact frozen span, normalized hash, inventory hash, discovery hash, and a correct SHA-256 of its Lean conjunct. The 20 definitions also match exact reconstructed source records; the operational-rule and proved-derived lists are empty. All 21 parameter binding hashes recompute, and every binding references only relevant domain-rule IDs.

Mathematically, the obligations preserve the exact guarded rules: projection definedness/reversal/idempotence; integer `>`, `>=`, `<`, `%`, and `+` dispatch; the two guarded `primeTail` folds; and the three positive-`N` digit folds. There are no omissions, duplicates, changed guards, irrelevant obligations, or stand-alone `True` conjuncts. The first proposition contains `∧ True` only as the faithful rendering of `#Ceil(@V)` for an already well-sorted `Val`; its projection-definedness iff remains substantive. A rule-by-rule mathematical assessment is in `evidence/stage4/mathematical-obligation-review.md`.

I reconstructed the target definition directly from the ordered parameter list and the 13 conjuncts and compared it byte-for-byte with `Klean94Skjkasdkd/Lemmas.lean`. It is the only `targetStatement`. Its fixed hashes agree across the generated file, generator manifest, preflight, and audit input:

- definition SHA-256 `59d9bcf3f62a054d1f933d400dbfa78e5797720737511640b2dd0f953d4837db`;
- applied-statement SHA-256 `697b0dbcd4c7e94800f6ee2a3079030a59743d59cf5c3b936fb9d8135ddf80b9`.

Evidence: `evidence/stage4/independent-generation-audit.log`. The selected status is correctly `PASS`, not `KLEAN_NO_OBLIGATIONS`, because the true domain set has 13 entries.

## Stage 5 clean build and proof identity

I copied the read-only candidate to fresh `/tmp/audit-work/proof-audit-final` and copied the selected generated project contents into its pre-existing empty `Base`. Before and after building, `Base` has exact generated-tree hash `d39652423da4b22eeaa43a473205673f746e535ba4d94082c472acd874151e0e`. I then ran both `lake clean` and `lake build` with the pinned compatibility library. Both exit 0; the build reaches `Built Proof` and `Build completed successfully`. The only diagnostics are unused-variable lints in generated code. Complete outputs are `evidence/stage5/lake-clean.log` and `evidence/stage5/lake-build.log`.

The candidate workspace hash remains the signed `6a65652395d1fc1655ca2a7353df9447e7cb7c8ea3068a4fcd726e174d7f9fd7`. Its two candidate sources copy byte-for-byte into the fresh workspace. After stripping comments, the candidate contains no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque`. It neither defines `targetStatement` nor enters the generated target namespace. Each of the 21 fixed target parameters has exactly one candidate `def`.

There is exactly one `theorem final`; its normalized type is exactly the manifest's fixed target application, in the same parameter order. Lean's `#check`/`#print` independently shows `Proof.final` at that target, with only namespace qualification added to the supplied definitions. Thus it is not a duplicate, weakening, or vacuous substitute. Evidence: `evidence/stage5/candidate-integrity-check.log` and `evidence/stage5/print-axioms-direct.log`.

## Axiom accounting

The exact required Lean output ends:

`'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]`

These are the trusted final gate's explicit standard Lean baseline. Reconciliation with `trust-inventory.json` found 42 generated allowlisted declarations, but `Proof.final` reaches none of them. It reaches no `sorryAx`, no candidate declaration, and no unrecorded axiom. Both designated- and other-sorry counts in the inventory are zero. Evidence: `evidence/stage5/axiom-reconciliation.log`.

## Operational-bridge audit

I compared every target parameter's exact candidate definition with its bound KORE symbol, source-rule IDs, frozen verification rules, source solution, and fixed operational semantics:

- `«_-Int_»`, `«_+Int_»`, `«_%Int_»`, and `«_/Int_»` use Lean integer subtraction, addition, truncating remainder, and truncating division, matching K `-Int`, `+Int`, `%Int`, and `/Int`.
- `_andBool_` and the six comparison/equality parameters `«_>Int_»`, `«_>=Int_»`, `«_<Int_»`, `«_<=Int_»`, `«_==Int_»`, and `«_=/=Int_»` implement the exact Boolean/integer operations.
- `applyBin` implements the bound integer `%` and `+` dispatch arms, returning the correct injected integer values; `applyCmp` implements the bound integer `>`, `>=`, and `<` arms.
- `definedProjectInt`, `isInt`, `«project:Int»`, `projectIntTotal`, and `«project:Int?»` recognize and recover exactly the generated integer injections on the guarded cast domain. Defaults outside a partial cast's guard do not invent an in-domain result; `projectIntTotal` is deliberately totalized in K and only operationally consumed under `definedProjectInt`/`isInt` in these rules and the source contract.
- `pyMod` is exactly `tmod (tmod x y + y) y`, the frozen `((x %Int y)+Int y)%Int y` rule.
- `primeTail` implements all three defining cases and the `D+1` recurrence, rather than only the two generated fold equations.
- `digitSum` implements the nonpositive base and positive base-10 recurrence, rather than a theorem-convenient identity or constant.

The independent executable suite checks all 21 bindings through 38 boundary/adversarial observations: negative truncating remainder and Python modulo, negative division, comparison equality boundaries, integer versus Boolean projection, nonsingleton K sequences, prime/composite and recurrence boundaries, nonpositive digit sum, and the prompt examples 181 → 10 and 4597 → 25. Every check evaluates to true. Seven counterfactuals also distinguish the candidate from constant `primeTail`, identity `digitSum`, hard-coded projection, truncating-only Python modulo, constant comparison, left-identity binary dispatch, and constant `isInt`; every distinction evaluates to true and is compiled as a Lean assertion. Evidence: `evidence/stage5/operational-adversarial-tests.log` and the complete parameter analysis in `evidence/stage5/operational-bridge-review.md`.

## Conclusion

Stage 3 is complete and correctly classified; Stage 4 is authenticated, deterministic, bijective, target-preserving, and mathematically faithful; and Stage 5 cleanly proves exactly that target with accounted standard axioms and honest operational bridges. Mechanical success was not used as a substitute for the independent semantic checks above.

VERDICT: PASS
LEGITIMACY: LEGIT
