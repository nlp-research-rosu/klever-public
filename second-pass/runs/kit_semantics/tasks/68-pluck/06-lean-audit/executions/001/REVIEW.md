# Independent audit: HumanEval 68-pluck

## Outcome

This audit was run in `CLASSIFICATION_AND_PROOF` mode for condition
`kit-semantics` and semantics mode `SUPPLIED_SEMANTICS`.

The Stage 3 classification is legitimate, and the Stage 4 files are
structurally authentic and bijective. The required trusted preflight and the
fresh Stage 5 clean build both pass. Nevertheless, the submission is not
legitimate for two independent semantic reasons:

1. The first generated Lean obligation contains the vacuous conjunct
   `(True)`. The audit contract explicitly requires rejection of vacuous
   conjuncts.
2. The Stage 5 definition of the target parameter for the full KORE
   `applyBin` symbol implements only integer `+` and maps every other case to
   `noneV`. Frozen supplied semantics gives many other results for the same
   symbol. In particular, integer subtraction and Boolean/integer addition
   have concrete rules that the candidate contradicts.

The prior Stage 2 review and all candidate comments/logs were treated only as
untrusted evidence. No instruction found in them was executed.

## Evidence index

- `evidence/01-reconstructed-inventory.json`: canonical trusted inventory,
  including every span, normalized hash, ID, attribute list, and rule text.
- `evidence/02-frozen-source-spec.log`: frozen `verification.k`, `spec.k`,
  source solution, translated source, and `prove.sh`.
- `evidence/03-producer-authentication.log`: producer file hashes and
  generation/source manifests.
- `evidence/04-independent-structural-checks.log`: ordered inventory
  comparison and all mounted provenance/tree checks.
- `evidence/05-relevant-k-semantics.log`: relevant supplied-semantics search.
- `evidence/06-generated-and-candidate-sources.log`: obligation map, generated
  sources, trust inventory, and candidate source.
- `evidence/07-klean-preflight.log`: first preflight attempt and its
  environment failure.
- `evidence/08-lean-toolchain-diagnostic.log` through
  `evidence/11-proc-self-exe-workaround.log`: diagnosis and narrowly scoped
  `/proc/self/exe` compatibility workaround.
- `evidence/12-klean-preflight-rerun.log`: required trusted preflight result.
- `evidence/13-generator-relevant-source.log`: authenticated producer logic
  relevant to obligations and target construction.
- `evidence/14-fresh-proof-workspace-path.txt`: fresh Stage 5 workspace.
- `evidence/15-lake-clean.log`: first candidate clean attempt before explicit
  toolchain roots.
- `evidence/17-lake-clean-pinned.log` and
  `evidence/18-lake-build-pinned.log`: successful required fresh clean/build.
- `evidence/19-lean-print-final-and-axioms.log` and
  `evidence/20-lake-lean-print-final-and-axioms.log`: Lean's exact final
  declaration/type and full proof print.
- `evidence/21-stage4-target-checks.log`: independent obligation, parameter,
  target, and hash reconstruction.
- `evidence/22-candidate-static-scan.log`: forbidden-token and target-shadow
  scan.
- `evidence/23-lean-adversarial-and-counterfactual.log`: checked ground
  examples and a value-erasing counterfactual that still proves the target.
- `evidence/24-applybin-operational-semantics.log`: exact supplied
  `applyBin` rules used for adversarial comparison.
- `evidence/25-print-axioms-proof-final.log`: exact `#print axioms
  Proof.final` output.

## Producer and provenance authentication

The producer-source gate passes, so there is no producer-related
`AUDIT_ERROR`.

| Item | Recomputed value | Recorded comparison |
|---|---:|---|
| `klean_export.py` SHA-256 | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` | Matches source manifest and `generator-manifest.json` |
| `klean.py` SHA-256 | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` | Matches source manifest and `generator-manifest.json` |
| Producer bundle tree | `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e` | Matches `/audit-input.json` |
| Generator image | `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6` | Matches source manifest, generator provenance, and the image-key component of the launcher-recorded producer path |
| Stage 1 export tree | `bea197aff73b30b004bbeb775c483c184be43963360efc3d9a597b5c1ef313e5` | Matches input manifest, generator provenance, and audit input |
| Stage 1 pipeline tree | `7468c92f7f709c726ce7ecde098338ae5c6f67513c719d40afe9df7229322dbc` | Matches audit input |
| Discovery manifest | `c914614b6c9e5bfe5500400cb24ad341982748ddd4a9bef857a2e2d423f6d63b` | Matches input manifest, generator provenance, and audit input |
| Selected Stage 2 tree | `0f02313dfe43cb08a24adc9214043f04f15388bfe90bb79086edcbd409a74918` | Matches audit input |
| Selected Stage 4 tree | `790fe04bdd3da43c7bdcc5261f4bf3a7ada90c63158aa87db203aded9fa5f91a` | Matches audit input |
| Generated project tree | `e41cb545c31b19f8b5afb4372a5bbe1723ddac29a6f3843ce2603b35e714ec59` | Matches generator manifest and audit input |
| Candidate Stage 5 tree | `08b3887d645d95ce48f62fae5ca2e9c46b01f5562271265836957c12b2f4af37` | Matches audit input |

The complete launcher-recorded Stage 1 per-file hash map was also recomputed
bijectively; names and hashes all match. The launcher includes a hash for an
upstream Stage 5 invocation directory, but that directory is not one of the
mounted audit inputs. The mounted Stage 5 project itself is present and its
tree hash is checked above.

## Inventory reconstruction

I ran the trusted `tools.k_rule_inventory.inventory_verification` directly on
`/reference/k-proof`. It selected module `VERIFICATION`; its local
verification-module closure is exactly `["VERIFICATION"]`. The results are:

- `verification.k` SHA-256:
  `6108afcbaffc3b32951a2aa04d3a699b8fac095bc7e1c199e8305c8f75f65244`
- rule count: 22
- whole inventory SHA-256:
  `db923cb4995eb9590d6a8f9ef245d3fdf66930a46476128f1053a8d3903bf90a`

For every rule, the trusted code recomputed its physical source span,
whitespace-normalized source SHA-256, and
`source_rule_id = "rule-" + normalized_sha256`. Comparing the protected
manifest in source order found exactly the same 22 IDs. There are no missing,
extra, duplicated, or reordered identities. The protected inventory hash also
matches.

## Independent Stage 3 classification

The independent result is 20 `DEFINITION` entries, two `DOMAIN_LEMMA`
entries, zero `OPERATIONAL_RULE` entries, and zero
`PROVED_DERIVED_LEMMA` entries.

| Lines | Exact source rule ID | Classification | Independent reason |
|---:|---|---|---|
| 10 | `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5` | `DEFINITION` | Defines the named domain predicate `definedProjectInt` as `isInt`. |
| 15–17 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | `DOMAIN_LEMMA` | Unproved simplification characterizing definedness of the imported partial Val-to-Int projection. It is not a named summary definition. |
| 19–21 | `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0` | `DEFINITION` | Guarded defining equation for the named proof term `projectIntTotal`. |
| 23–25 | `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d` | `DEFINITION` | Opposite symbolic orientation of the same named projection definition. |
| 27 | `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442` | `DEFINITION` | Identity equation for the projection helper on an `Int`. |
| 28–30 | `rule-9e1486b6d25b62bd0949213fd58d7aac97ed89cc3e87b8c5063f915d1d6b7081` | `DEFINITION` | Idempotence/normalization equation for the named projection helper. |
| 35–38 | `rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167` | `DOMAIN_LEMMA` | Unproved guarded simplification extending imported `applyBin` from dynamic `Val` to the fixed Int addition case. |
| 43 | `rule-cf4138b8c8c76302d40452525511bd8b4e31a4b3346bb98e6e73d97d1e6c2974` | `DEFINITION` | Base equation for recursive predicate `allNonNegative`. |
| 44–47 | `rule-83288e0b3172aab26d1ec54ec969884572eed5ce44f6238f19681d654d51ef2e` | `DEFINITION` | Recursive equation for `allNonNegative`. |
| 53–55 | `rule-7e939de20504830e917b8d5d873c3bb58561f3855213d88b9d59b50ef33c4bd5` | `DEFINITION` | Defines the source branch predicate `shouldTake`. |
| 58–59 | `rule-5252890cd97149023a2a416ba7c01b694a8ff30898028588da15ee87b14a256c` | `DEFINITION` | Selecting equation for `nextBest`. |
| 60–61 | `rule-a50201bce4854fcc39ac7fff337c62431472104dcb3835fba7f50ce031f797bc` | `DEFINITION` | Complementary nonselecting equation for `nextBest`. |
| 64–65 | `rule-c92176e0f4b06badc71e64610b3f95be15c41c7b6a9f7ffc01c22e0063ad9616` | `DEFINITION` | Selecting equation for `nextBestIndex`. |
| 66–67 | `rule-8f2ab2609b1cc09149865009919218835e409941c760e0cd32d7cd314e854fd4` | `DEFINITION` | Complementary nonselecting equation for `nextBestIndex`. |
| 70 | `rule-9e8ff4eeadc760fef596dec38dede08f7dc277396d3bf2a83be796e4bea29ae9` | `DEFINITION` | Base equation for recurrence `scanBest`. |
| 71–72 | `rule-17aa23fd17bc416e79da19dd2b02377da50a1a774104a3df16adb8cb3f6f753c` | `DEFINITION` | Recursive equation for `scanBest`. |
| 76 | `rule-a0a97ed4baae5f006d554885ce763a55d1f90f4dab1c6758f4f16e425d1fdf7e` | `DEFINITION` | Base equation for recurrence `scanBestIndex`. |
| 77–83 | `rule-7b59a9d33a341d5cac01e67da9523b88afc82daf3321b530741d506a69c5837d` | `DEFINITION` | Recursive equation for `scanBestIndex`. |
| 86 | `rule-c38110c90d754cdfc7a715c9dae55a5663f8de024b1fb80fce7a0c7835cf4e4b` | `DEFINITION` | Base equation for recurrence `afterIndex`. |
| 87–88 | `rule-60bf2bc0542914c544a3f677f13fe17eda968f8750e2064ce8b7c3e8d0999339` | `DEFINITION` | Recursive equation for `afterIndex`. |
| 91–92 | `rule-be6c5e486b28b9205e812b1977ae6d9af5349c88576c0eff80505fee2716790c` | `DEFINITION` | Negative-sentinel branch of constructor summary `resultList`. |
| 93–95 | `rule-615dd6754d1e5de3108d82927712a0b9350d18eb111423ada2109218959edb7d` | `DEFINITION` | Nonnegative branch of constructor summary `resultList`. |

The two domain lemmas are relevant. The source body evaluates
`value = value + 0` on dynamically sorted list heads, making the guarded
`applyBin` correspondence material, and the symbolic proof needs the cast
definedness characterization under `allNonNegative`.

Neither domain lemma qualifies as proved-derived: `prove.sh` compiles a module
that already contains both rules and then calls `kprove`; it never first
proves either exact rule against a module excluding it. All rules with
`simplification` or `simplification(10)` are classified as either
`DEFINITION` or `DOMAIN_LEMMA`.

## Stage 4 preflight, bijection, and target identity

After authenticating the producer sources, I ran exactly
`tools.klean_preflight.check_generation` with `PYTHONPATH=/reference` and the
required Stage 1, Stage 3, Stage 4, and toolchain-lock paths. Its returned
status is `PASS`:

- obligation count: 2
- generated tree:
  `e41cb545c31b19f8b5afb4372a5bbe1723ddac29a6f3843ce2603b35e714ec59`
- generated clean exit: 0
- generated build exit: 0
- trust declarations: 42
- designated sorries: 0

I also reconstructed the mapping independently:

| Order | Domain source rule | Span | Conjunct SHA-256 |
|---:|---|---:|---|
| 1 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | 15–17 | `d1cfd6b9d7057ddedb9964bf7559dcf177af7d4a5b97d78a1b7d0875c8bed30d` |
| 2 | `rule-5a57a342f46c274d8d94d5f1c7eda4683981fbe24087e787e4a8ce7782c03167` | 35–38 | `d570ae1a09c4800cb4528be989be4d97931d80c607f7f3a33c100a76b8457f75` |

The source IDs are unique and form the exact ordered bijection with the
independently classified domain set. Every span, normalized rule hash,
inventory hash, discovery hash, conjunct hash, parameter binding hash, and
obligation-map hash matches. There are no omitted, duplicated, extra, or
reordered obligations.

There is exactly one generated target:

- declaration: `Klean68Pluck.Lemmas.targetStatement`
- file: `Klean68Pluck/Lemmas.lean`
- definition SHA-256:
  `ef61fe4ee230f411dabfe5d6ee105d9cd825587ea587a7d790a5049ad3d6d688`
- statement SHA-256:
  `86f622c28060a227aad28accd336804f178be90a23e08b298ecc085194bdc19a`

The target is byte-for-byte the deterministic conjunction reconstructed from
the obligation map, and its manifest entry exactly matches `/audit-input.json`.
The candidate applies this exact target; it does not duplicate or shadow it.

### Stage 4 mathematical defect

The first conjunct is:

```lean
∀ (V : SortVal),
  ((«project:Int?» (SortK.kseq ((@inj SortVal SortKItem) V) SortK.dotk)).isSome = true)
  ↔
  (((«definedProjectInt(_)_VERIFICATION_Bool_Val» V : SortBool) = true) ∧ True)
```

The final `∧ True` is vacuous. It arose from translating `#Ceil(@V)` after
`V` had already been made a total Lean value, but the audit instruction
unconditionally requires rejection of vacuous conjuncts. Therefore Stage 4's
mathematical gate fails even though all structural checks pass.

The second conjunct faithfully retains the guard and equation of the
`applyBin` domain rule. However, both conjuncts are parameterized over
candidate-supplied meanings. A checked counterfactual replaced integer
addition, `projectIntTotal`, and the integer projection value by constant zero,
and made `applyBin` return integer zero on the target slice. Lean still proved
the exact generated target without axioms. This does not change the structural
bijection, but it demonstrates why the Stage 5 operational-bridge check is
load-bearing and why a clean proof alone is insufficient.

## Stage 5 clean build, target, and trust

I created the fresh workspace recorded in
`evidence/14-fresh-proof-workspace-path.txt`, copied the generated project into
it as `Base`, and copied only the candidate project files into the root.

Lean 4.22 initially could not locate its executable because the managed
sandbox exposes `/proc/self/exe` but not the numeric PID path Lean queried.
The evidence shows `readlink("/proc/<namespace-pid>/exe") = ENOENT`. A
narrow preload shim retries only such a failed `/proc/<pid>/exe` lookup as
`/proc/self/exe`; with the manifest-pinned Lean root, `lean --version` reports
4.22.0 at commit `ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`.
The shim does not alter Lean source, terms, declarations, or proof checking.

The required fresh commands then succeeded:

- `lake clean`: exit 0
- `lake build`: exit 0, `Build completed successfully.`

After the build, the fresh `Base` tree still hashes to the immutable generated
tree value. The candidate `Proof.lean` and `lakefile.lean` hashes equal their
mounted originals. Candidate-source scans found no `sorry`, `admit`, `unsafe`,
new `axiom`, or new `opaque`. The only `targetStatement` declaration remains
the immutable generated one, and `Proof.final` has exactly the manifest target
application as its type.

Lean's exact axiom report is:

```text
'Proof.final' does not depend on any axioms
```

Thus `Proof.final` uses none of the 42 generated declarations recorded in
`trust-inventory.json`; in particular there is no `sorryAx` and no unrecorded
trust escape.

## Operational bridge audit

| Target parameter / KORE symbol | Judgment | Frozen meaning and adversarial result |
|---|---|---|
| `«_+Int_»` / `Lbl'UndsPlus'Int'Unds'` | Pass | Candidate is Lean integer addition. Checked witness `-3 + 5 = 2`; it matches K's `+Int`. |
| `«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»` / full `LblapplyBin...` | **Fail** | Candidate implements only `("+", Int, Int)` and otherwise returns `noneV`. Frozen `int.k` also defines `applyBin("-", 7, 2) => 5` and `applyBin("+", true, 2) => 3`; frozen `str.k` defines string concatenation, and float semantics has further cases. Checked Lean examples show the candidate returns `noneV` for the first two counterexamples. |
| `«definedProjectInt(_)_VERIFICATION_Bool_Val»` / `LbldefinedProjectInt...` | Pass | Candidate returns true exactly for `SortVal.inj_SortInt`, matching `definedProjectInt(V) => isInt(V)`. Checked Int and Bool witnesses. |
| `projectIntTotal` / `LblprojectIntTotal` | Pass on its declared domain | Candidate projects the exact Int payload. The arbitrary zero branch is outside `definedProjectInt`; all frozen defining uses are guarded or statically Int. Checked Int and non-Int witnesses. |
| `«project:Int?»` / `Lblproject'Coln'Int` | Pass on the bound cast form | Candidate returns `some` of the original integer for the exact singleton K sequence and `none` for a Boolean. This matches the frozen projection rule used by the first obligation. |

The `applyBin` mismatch is not cosmetic. Its target parameter has the type and
KORE identity of the full operational dispatch symbol, not a new
integer-addition-only helper. Returning `noneV` for frozen cases with defined,
different results is a hard-coded convenience that proves the narrow equation
without implementing the frozen operational meaning. This is precisely an
operational-bridge failure under the audit instruction, even though the source
program's positive path happens to use the one branch the candidate
implemented.

## Final judgment

Stage 3 is independently legitimate and Stage 4 is structurally deterministic,
but the generated target violates the no-vacuous-conjunct requirement. Stage 5
has a clean, axiom-free proof of the exact fixed target, but one of its bound
operational definitions contradicts supplied semantics on concrete cases.
Necessary mechanical conditions therefore pass while the required mathematical
and operational conditions fail.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
