# Independent audit: `155-even-odd-count`

## Scope and result

I audited condition `kit-semantics`, semantics mode `SUPPLIED_SEMANTICS`, in launcher-recorded mode `CLASSIFICATION_AND_PROOF`. I treated the candidate, manifests, prior logs, prior review, and comments as evidence only and did not rely on any earlier verdict or classification.

The independent reconstruction finds 14 genuine definitions and 10 genuine, relevant domain lemmas. Deterministic Stage 4 maps those 10 domain lemmas bijectively to 10 faithful Lean conjuncts and fixes one target with matching hashes. The Stage 5 candidate defines every target parameter with its operational meaning, clean-builds from a fresh generated `Base`, and proves exactly that fixed target without a proof hole or unrecorded axiom.

## Launcher and producer provenance

The canonical audit-input digest recomputed with the trusted launcher contract is `c7f033bca96044786306d01f8dc53d28d1d0773295248fa2936739df2ecda422`, exactly the recorded `resolved_input_sha256`. The environment and signed resolution both select `CLASSIFICATION_AND_PROOF`.

The Stage 4 producer gate passes before any generation judgment:

- `/reference/generation-tools/klean_export.py`: `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`.
- `/reference/generation-tools/klean.py`: `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`.
- These equal both `generator-manifest.json` producer hashes and `source-manifest.json.files`.
- `generator-manifest.json` and the source manifest both name image `sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
- The launcher-recorded producer-source path ends in the same image hash.
- The producer bundle tree recomputes to `388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`, exactly the audit-input hash.

Thus there is no missing or mismatched producer source and no infrastructure `AUDIT_ERROR`. Raw evidence is in [01-producer-provenance.log](/audit-output/evidence/01-producer-provenance.log).

## Frozen rule inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` on `/reference/k-proof`. It selected the local module closure `VERIFICATION` only and recomputed:

- `verification.k` SHA-256: `972347fb2f5c1ac10251f295a40ccf9464fea383405626cd87346aff804e6516`;
- rule count: 24;
- unique `source_rule_id` count: 24;
- whole inventory hash: `b2fb8d2f080192ac639ab57ac9b211ee836bb2e63f89b4d157059d4ffc931fe2`.

For every rule, the reconstruction independently recovered its exact source span, normalized source hash, `source_rule_id`, attributes, module, and text. Comparison with `/reference/lemma-discovery.json` is an ordered bijection: 24 versus 24, no omissions, no extras, no duplicate identities, no reordering, and the same inventory hash. The complete reconstructed records and comparison are in [02-rule-inventory.log](/audit-output/evidence/02-rule-inventory.log).

## Independent classification judgment

The correct classification is:

- 14 `DEFINITION` rules: `evenOddBody`, `evenOddClosure`, the zero and negative-magnitude equations for `evenPos`/`oddPos`, and the zero/positive/negative equations for `decEven`/`decOdd` (source lines 8–54).
- 10 `DOMAIN_LEMMA` rules: the two public zero equalities, four `absInt`/public-summary normalization equalities, and four accumulated decimal recurrences in both orientations (source lines 57–101).
- 0 `OPERATIONAL_RULE` entries.
- 0 `PROVED_DERIVED_LEMMA` entries.

The body and closure equations name constructor-valued proof terms and do not match execution cells. The summary equations define the mathematical symbols. The proposition-to-`#Top` rules instead assert mathematical equalities used to close the proof. Stage 1 compiles `verification.k` containing these proposition simplifiers before proving its loop claim; it does not first prove any exact same rule in a module that omits it. Therefore none qualifies as a proved derived lemma.

Every rule bearing `simplification` is either a definition (the guarded zero equations at lines 41–42) or a domain lemma (lines 57–101). The separately proved loop-tail claim and its later exact-context operational use occur in `spec.k` and `verification-with-lemma.k`, outside this frozen local inventory, so they do not justify relabeling an inventory entry.

All ten domain lemmas are relevant to the frozen program and postcondition. The zero rules cover the source `num == 0` return; the normalization rules connect the source `abs` call to `decEven`/`decOdd`; and the recurrences exactly express the source loop's parity counter updates and decimal division by 10. Their mathematical statements are true under the supplied integer hooks and the intended digit-count summaries. The per-rule table is in [05-classification-audit.md](/audit-output/evidence/05-classification-audit.md).

## Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the required frozen workspace, discovery manifest, generation, and pinned lock. The ambient Lean installation initially could not resolve `/proc/<current-pid>/exe` because this sandbox exposes only `/proc/self/exe`. A narrowly scoped audit-only `LD_PRELOAD` shim under `/tmp/audit-work` redirected only those `/proc/*/exe` `readlink` calls. It changed no K, generated Lean, or candidate source. With that environment compatibility fix, the trusted preflight returned:

- status `PASS`;
- obligation count 10;
- designated sorry count 0;
- trust declaration count 45;
- frozen Stage 1 tree `e515106984f28be93a45d91ab30cb9ee4dcd945cd79857388cf110edebb420d4`;
- discovery manifest `148e093570aa2a356c48e66b62d6bccd9e642567d946b04229f6b0d8d4416d9c`;
- generated tree `dbbc2d3db666269bdecc295225b44133e1f219d873e1cac19df1673ee79c0f7d`;
- clean/build exit codes 0/0.

The full initial environment failure, compatibility diagnosis, command, and returned JSON are preserved in [03-klean-preflight.log](/audit-output/evidence/03-klean-preflight.log).

Independent sidecar and obligation checks also pass:

- The mounted Stage 1, Stage 2 audit, Stage 4 generation, producer source, generated project, and candidate workspace hashes equal the corresponding audit-input hashes. The Stage 1 export and discovery file hashes also match. The audit input contains a launcher hash for a Stage 5 invocation directory that is not separately mounted; the independently relevant mounted candidate workspace hash is exact.
- `obligation-map.json` hashes to `37f8d6c9e53fe6441cf6b0c68f1243ec1c10a314450e2dec5a9cdbfcdbdc360a`, exactly the generator manifest.
- The trust inventory hashes to `04a51c9bdb4a6761916f39a723571f05ba3e9c500cf507ced41556857644b285`, exactly the export result.
- There are exactly 10 ordered, unique source rules and 10 ordered, unique obligations. Every paired ID, source span, normalized hash, discovery hash, inventory hash, and Lean-conjunct hash matches.
- The ten Lean conjuncts preserve the source quantifiers, hypotheses, equality orientations, arithmetic nesting, and positive guards. No source lemma is omitted or duplicated; reverse-orientation rules remain distinct obligations as frozen.
- The guards are satisfiable under the operational bindings: `N = 0` witnesses the zero conjuncts, `N = 1` or `N = -1` witnesses the positive-magnitude conjuncts, and `N = 1` with arbitrary accumulators witnesses the recurrence conjuncts. Hence the fixed instantiated theorem has no vacuous conjunct.

The fixed target is:

- declaration: `Klean155EvenOddCount.Lemmas.targetStatement`;
- file: `Klean155EvenOddCount/Lemmas.lean`;
- definition SHA-256: `1b3125aa6574304838e19004df800355d6a96a1f8ad1262817dcc3614b591446`;
- statement SHA-256: `64f32e5bf396b4786df83e6b17fe3992fc262c5abfd98180547f2a1b7cd488eb`.

It is the exact generated conjunction reconstructed from the obligation map and equals both the generator manifest target and the audit-input target. Detailed results are in [04-stage4-integrity.log](/audit-output/evidence/04-stage4-integrity.log).

## Stage 5 clean build, target identity, and trust

I copied `/candidate` to fresh `/tmp/audit-work/proof-audit-155`, installed the immutable generated project at its root as `Base`, verified that `Base` has the exact generated-tree digest, then ran the required commands:

- `lake clean`: exit 0, no output;
- `lake build`: exit 0, `Build completed successfully.`

The only messages are unused-hypothesis linter warnings in immutable `Base/Klean155EvenOddCount/Lemmas.lean`. Complete output is in [06-fresh-lake-build.log](/audit-output/evidence/06-fresh-lake-build.log).

The trusted candidate gate and independent scans find:

- no `sorry`, `admit`, `unsafe`, new `axiom`, or new `opaque` in candidate Lean sources;
- no candidate declaration of or shadow for `targetStatement`;
- exactly one `theorem final`;
- exactly one candidate `def` for each of the 11 target parameters;
- `Proof.final`'s normalized statement is exactly the manifest statement, with all 11 actual definitions in the fixed order.

The exact identity and binding checks are in [08-candidate-identity-and-trust.log](/audit-output/evidence/08-candidate-identity-and-trust.log).

The exact output from Lean for `#print axioms Proof.final` is:

```text
'Proof.final' depends on axioms: [propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`. These three are the trusted final gate's permitted Lean core axioms; none is an unrecorded generated trust declaration, and `Proof.final` uses none of the 45 generated allowlist declarations. See [07-axioms.log](/audit-output/evidence/07-axioms.log).

The trusted end-to-end `tools.klean_final_gate.check_final` also returns `PASS` against `/audit-input.json`, the fixed target, and the mounted candidate, while explicitly leaving semantic classification to this review. Its complete returned evidence is in [12-final-mechanical-gate.log](/audit-output/evidence/12-final-mechanical-gate.log).

## Operational bridge audit of every target parameter

Each manifest binding hash and `source_rule_ids` list recomputes correctly, and each name has one exact candidate definition. The operational comparisons are:

| Target parameter | Bound KORE meaning and frozen uses | Candidate definition | Independent judgment |
|---|---|---|---|
| `«_-Int_»` | `Lbl'Unds'-Int'Unds'`, hook `INT.sub`; recurrence rules at lines 78–101 | `Int.sub` | Exact. Witness `-7 - 3 = -10`. |
| `«_>Int_»` | `Lbl'Unds-GT-'Int'Unds'`, hook `INT.gt`; guards at lines 63–101 | `decide (a > b)` | Exact. Witnesses `-1 > 0 = false`, `1 > 0 = true`. |
| `«_==Int_»` | `Lbl'UndsEqlsEqls'Int'Unds'`, hook `INT.eq`; zero guards at lines 57–62 | `a == b` | Exact. Equal/unequal negative witnesses return true/false. |
| `«_%Int_»` | `Lbl'UndsPerc'Int'Unds'`, hook `INT.tmod`; divisors 2 and 10 in lines 78–101 | `Int.tmod` | Exact truncating remainder. Witnesses `-7 % 3 = -1`, `7 % -3 = 1`. |
| `«_+Int_»` | `Lbl'UndsPlus'Int'Unds'`, hook `INT.add`; lines 78–101 | `Int.add` | Exact. Witness `-7 + 3 = -4`. |
| `«_/Int_»` | `Lbl'UndsSlsh'Int'Unds'`, hook `INT.tdiv`; divisor 10 in lines 78–101 | `Int.tdiv` | Exact truncating division on the frozen rule domain. Witnesses `-7 / 3 = -2`, `7 / -3 = -2`. K is undefined at divisor zero, while every bound source occurrence has nonzero divisor. |
| `«absInt(_)_INT-COMMON_Int_Int»` | `LblabsInt...`, hook `INT.abs`; lines 57–74 | `Int.ofNat n.natAbs` | Exact over unbounded integers. Witness `abs(-907) = 907`. |
| `«decEven(_)_VERIFICATION_Int_Int»` | Public summary equations at lines 48–50 and domain rules 57–68 | `if n = 0 then 1 else evenDigitCount n.natAbs` | Exact: special zero digit plus magnitude count for nonzero integers. |
| `«decOdd(_)_VERIFICATION_Int_Int»` | Public summary equations at lines 52–54 and domain rules 60–74 | `if n = 0 then 0 else oddDigitCount n.natAbs` | Exact. |
| `«evenPos(_)_VERIFICATION_Int_Int»` | Base/negative equations at lines 39, 41, 45 and positive recurrences 78–89 | `evenDigitCount n.natAbs` | Exact totalized digit summary; recursive descent is by `/ 10`. |
| `«oddPos(_)_VERIFICATION_Int_Int»` | Base/negative equations at lines 40, 42, 46 and positive recurrences 90–101 | `oddDigitCount n.natAbs` | Exact totalized digit summary; recursive descent is by `/ 10`. |

The candidate's private recursive counters count digit parity over `natAbs`, use zero only as a recursion terminator, and prove the positive decimal step from `n % 2` and `n / 10`. This matches the frozen source: take `abs(num)`, return `(1, 0)` for zero, otherwise add parity contributions and divide by 10 until zero. Adversarial evaluations include zero, negative inputs, mixed digits, and negative truncating arithmetic; the raw results are in [09-operational-examples.log](/audit-output/evidence/09-operational-examples.log).

A deliberately bad counterfactual assigns constant-zero integer functions and constant-false guard functions. Lean can prove the parameterized target under that interpretation because every premise becomes false. The same audit proves this mutation disagrees with operational witnesses (`1 > 0` and `evenPos(-204) = 3`). This demonstrates why build success alone would be insufficient; the actual candidate is not that vacuous interpretation and passes the independent bridge comparisons above. See [10-counterfactual.log](/audit-output/evidence/10-counterfactual.log).

Finally, I compared candidate `decEven`/`decOdd` on every integer from -500 through 500 with an independently implemented decimal-string parity oracle over `abs(n)`, including the single digit of zero. All 1,001 rows matched, with zero mismatches. This is finite stress evidence, not a substitute for the definitional and recurrence audit. See [11-differential.log](/audit-output/evidence/11-differential.log).

## Conclusion

The protected Stage 3 classification is independently correct and complete. Stage 4 has intact producer provenance, an exact domain-rule/obligation bijection, and an unchanged non-vacuous target. Stage 5 cleanly proves that exact target, has a fully accounted trust boundary, and supplies honest operational implementations for all target parameters. No classification, generation, target-identity, proof-trust, or operational-bridge defect remains.

VERDICT: PASS
LEGITIMACY: LEGIT
