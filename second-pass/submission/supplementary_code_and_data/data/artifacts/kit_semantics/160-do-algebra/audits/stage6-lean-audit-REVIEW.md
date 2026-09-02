# Independent audit: 160-do-algebra

## Scope and conclusion

I audited HumanEval `160-do-algebra`, condition `kit-semantics`, semantics mode
`SUPPLIED_SEMANTICS`.  Both `AUDIT_MODE` and `/audit-input.json` select
`CLASSIFICATION_AND_PROOF`.  I treated all candidate/provenance prose and prior
verdicts as untrusted evidence and based the judgment on the frozen source,
trusted inventory/preflight/final-gate code, direct hashing, and fresh Lean
execution.

The Stage 3 classification is complete and mathematically appropriate, Stage
4 is the deterministic four-obligation export of exactly the true domain-lemma
set, and the Stage 5 candidate proves the immutable generated target with
honest operational bindings.  I found no omitted lemma, weakened target,
candidate trust escape, or operational-bridge failure.

## Input and producer integrity

The recorded audit-input contract verifies, including its resolved-input hash
`91dd7133f5b1e997f704930e13f646191eb7f5d2ab4f51d17abccc22267d5607`.
I independently recomputed the authoritative tree/file hashes for the mounted
inputs.  The Stage 1 workspace, selected Stage 2 audit, discovery manifest,
complete Stage 4 generation, generated Lean tree, Stage 1 export, producer
source tree, and candidate workspace all match `/audit-input.json`.  I also
recomputed every one of the 770 entries in `stage1_source_hashes`; the key set
is exact and there are no hash mismatches.  See
`evidence/13_audit-input-and-source-hashes.txt`.

The required generation-time producer authentication passes:

| Item | Observed SHA-256 | Result |
|---|---|---|
| `klean_export.py` | `7cb3ed0da718d6b07560a910b8a2b3d9295cfb330b02bf52f0a8e1129f188752` | equals generator manifest and source manifest |
| `klean.py` | `50ca6b06c1387c7fd0a31354f65a31546227cf63ed35acd5386bef8fa118e346` | equals generator manifest and source manifest |
| Producer tree | `bf8ab7d57561461dce9bffa6786f6cf2f7158cc274f2c4c8b26f79a20154b35e` | equals audit input |
| Generator image | `sha256:1b835aff66132f7ce282a7c2489b068f07401e58dc0af481344242c0e33d7ef6` | equals generator manifest, source manifest, and audit-input producer path |

`evidence/04_producer-authentication.txt` preserves an exploratory tree hash
computed with `tools.audit_contract.sha256_tree`; it differs because that
function uses different tree framing and is not the Stage 4/audit-input hash
contract.  I corrected this with the authoritative
`tools.pipeline_contract.sha256_tree`, whose exact matching result is in
`evidence/04b_producer-tree-authoritative.txt`.  The two mandatory direct
producer-file hashes matched under either check, so there is no producer-source
infrastructure error.

## Rule-inventory reconstruction

Using only `tools.k_rule_inventory.inventory_verification` on
`/reference/k-proof`, I reconstructed the local verification-module closure as
`VERIFICATION-SYNTAX` and `VERIFICATION`.  The frozen `verification.k` hash is
`486e58b29c0d46347de2e7e8199fc104268615ddee0a2f46cd935f6b6d3ef850`.
The reconstruction contains 26 rules and has whole-inventory hash
`da317030086d190a2a4b66952efe2d94d9777d72413dabf6d2fb32bd5d672de7`.

The protected discovery manifest is a bijection with that reconstruction:
26 entries, canonical order preserved, unique identities, exact source spans,
exact normalized source hashes, and every identity equal to
`rule-<normalized_sha256>`.  There are no missing, duplicated, extra, or
reordered rules.  The complete reconstructed text and metadata are in
`evidence/02_inventory.json`; the independent comparison is in
`evidence/03_stage3-structural-check.txt`.

Every inventory entry was reclassified from source and semantics.  The exact
accounting is:

| Source span | Source rule ID | Classification | Independent basis |
|---|---|---|---|
| 30 | `rule-9e2ee339875a1d59e60ef1a09d50617f8c526c60d097a2a486ebed2a648461c5` | DEFINITION | defines the integer constructor discriminator |
| 31 | `rule-be84dcb9aded62f0c6e3a5401104828825eff4f20f59a0773cf8044129631296` | DEFINITION | defines the string constructor discriminator |
| 33-35 | `rule-0312858a8718cb93d212cdb7b679a2875534dc14191dff8edf7bccf9a96d8b43` | DOMAIN_LEMMA | asserts the guarded semantic equivalence for the partial `Val`-to-`Int` cast |
| 36-38 | `rule-0dda33275c7cbd1779ea25ffe3285879bf6652eca3210dd703138ffe06f5bf83` | DOMAIN_LEMMA | asserts the guarded semantic equivalence for the partial `Val`-to-`Str` cast |
| 40-42 | `rule-ced5adecb9e0d364813f64698375904533f4eeac50b93f2799465c7b5fead6d0` | DEFINITION | guarded concrete clause for named summary `projectIntTotal` |
| 43-45 | `rule-22fa1e67d4a05b75b5a578312159b0a4e049b756806628df2540b007f43bcb5d` | DEFINITION | symbolic bridge to the same named summary |
| 46 | `rule-7191d5f6c9756673cca00b440958222ca4d2d1d3d4e18cbc994313a0f4340442` | DEFINITION | constructor/base clause for `projectIntTotal` |
| 48-50 | `rule-e36d5c480914b95ecfc03189a914cb697e22cf78565e60467ec0e6c664136d4a` | DEFINITION | guarded concrete clause for named summary `projectStrTotal` |
| 51-53 | `rule-db9d27e9548a05d29d1ed50dae5699e3007e66b4be241553668c21d60b3a10ae` | DEFINITION | symbolic bridge to the same named summary |
| 54 | `rule-357de5496dc1a3e3b0ca9c3b05657fc36dd604057e89554979c1533e63de589f` | DEFINITION | constructor/base clause for `projectStrTotal` |
| 56 | `rule-db9ace5f904075a30e8c373b860a957613b5d313e1f148b4b3b5e8de1ee9df24` | DEFINITION | defines code extraction from the named string term |
| 57 | `rule-be4bdc1a56c0a6ad5ce5b89b9c7e34c8f82505a49e4ee67ef03de9b2564f9dff` | DEFINITION | defines named summary `codesProject` |
| 63-66 | `rule-532e0f2fb29f7ffe39ef42a75e9b8dc647afc9a5bea5118d59efc91aa6fb0c2d` | DOMAIN_LEMMA | verification-only guarded generalization of the frozen `str(I:Int)` dispatch |
| 68-71 | `rule-732e3db12428149cde5df3649531def1390bb546c9e8bf72aa92ed954f7e9ea5` | DOMAIN_LEMMA | verification-only guarded generalization of frozen string addition |
| 73-78 | `rule-7c8f0b9bab14968cab8a0ebcb0368e0bf680db9d93afc1b35f9e8ff93c3a41f6` | DEFINITION | defines the allowed-operator predicate |
| 83-89 | `rule-601ac6ff505ed21ebee6988a5f0ab7204a5a85ba002146ab7515fec6566db8ef` | DEFINITION | recursive validator clause for paired operand/operator lists |
| 91 | `rule-1a9baa3006dbad0e2d2d261d38ccd81892a0a10fafbffb6e417f47958dab1f5b` | DEFINITION | default validator clause |
| 95-96 | `rule-c53d40063880e69d6360260d8c67656341b373a008e1829b54b60e826eacc58a` | DEFINITION | terminal `validAlgebraRest` clause |
| 97-104 | `rule-74651854fc27bf85aca034c24477d437a29b1dcf3b8c9773b5edb284b7f2658c` | DEFINITION | recursive `validAlgebraRest` clause |
| 105 | `rule-1e15841822ebae8ce8a625ddd1c208717aad3f5aebd28eba98d877c046396e09` | DEFINITION | default `validAlgebraRest` clause |
| 108 | `rule-3e8d009985c5eba8a2269a5c0bcdf4b0dd68393ed77b3696e1a42bdae7a0f9a7` | DEFINITION | base clause for exact source-loop recurrence |
| 109-113 | `rule-6aa9e35f4f1fa9af281f3020d2a89aac20bdbacffbfb014a415067e44fa07d71` | DEFINITION | exhausted-operator recurrence clause |
| 114-125 | `rule-b1b9ea4c7230cfec8c4641fb3ab69e49050ca060d56531991d40506abacb4adc` | DEFINITION | recursive clause modeling `expression += str(oprn) + oprt` |
| 127-130 | `rule-71bd95b6455ab811eb01945827a595ff9fc562cb8a0741c76eddac54d1cffb6c` | DEFINITION | base clause for named last-pair summary |
| 131-136 | `rule-fa24fe5bb4c127b9263a33bb71318f5413821b87f5fab87183a237c9c0723707` | DEFINITION | recursive last-pair summary clause |
| 137 | `rule-3635eafd5332204dbdd6bbb67179cc7e6dc82b9a5feac31bd1e18f135a08915e` | DEFINITION | default last-pair summary clause |

Thus the correct totals are 22 `DEFINITION`, four `DOMAIN_LEMMA`, zero
`OPERATIONAL_RULE`, and zero `PROVED_DERIVED_LEMMA`.  The named discriminators,
guarded totalizations, validators, and recurrences genuinely define summaries
or proof terms.  The four domain entries instead make semantic claims about
pre-existing casts/dispatch symbols.  They were not first proved against a
module omitting them, so none qualifies as a proved derived lemma.  Nor are
the guarded dispatch twins ordinary frozen MPY execution rules: the ordinary
rules remain `applyBuiltin("str", I:Int, .Vals)` in `builtins.k` and
`applyBin("+", str(A), str(B))` in `str.k`.

Every rule carrying a `simplification` attribute is either a definition or one
of the four domain lemmas; none is misclassified as operational or
proved-derived.

## Domain relevance and Stage 4 generation

The domain set is genuinely nonempty and relevant.  The frozen solution loops
over `zip(operand, operator + [""])`, appending `str(oprn) + oprt` before
evaluating the resulting expression.  The two cast lemmas expose precisely the
dynamic integer/string cases of the zipped heads.  The guarded `str` lemma
connects the operand head to decimal text, and the guarded `+` lemma connects
the running expression to the operator string.  Removing any of these bridges
breaks the symbolic connection used by the exact source recurrence and its
postcondition.  No unrelated mathematical fact was exported.

I reran the required
`tools.klean_preflight.check_generation(/reference/k-proof,
/reference/lemma-discovery.json, /reference/klean-generation)` with
`PYTHONPATH=/reference` and the pinned Lean 4.22 toolchain.  It returns `PASS`,
with four obligations, no designated sorries, Stage 1 export hash
`3b075ef14e32e815806f536525144b7f06bd8a6a51791be31d0fdb9e642e9889`,
and generated tree hash
`0adc30863f031457992c6ea2ee486e335fa5361acc4ea9f2a2b45e9c88238f89`.
The complete returned evidence is in
`evidence/05d_preflight-rerun-shimmed.txt`.

Lean/Lake initially could not locate its own binary because the sandbox's PID
namespace and visible `/proc` namespace differ.  The failed unmodified attempts
are retained as evidence.  I used a narrowly scoped, source-recorded
`LD_PRELOAD` compatibility shim that changes only `readlink` of exact
`/proc/<digits>/exe` paths to `/proc/self/exe`; all other paths pass directly to
`readlinkat`.  Its source, binary hashes, diagnosis, and the pinned Lean commit
check are in `evidence/00_lean-proc-compatibility-shim.txt`.  It does not alter
Lean source, elaboration, compilation, or kernel checking.

The independent Stage 4 comparison establishes an exact ordered bijection:

1. `rule-031285...` maps to the `Int` cast-is-defined equivalence.
2. `rule-0dda33...` maps to the `Str` cast-is-defined equivalence.
3. `rule-532e0f...` maps to guarded `str` dispatch through `Int2String` and
   `strToCodes`.
4. `rule-732e3d...` maps to guarded string addition through `seqConcat` and
   `codesProject`.

The domain IDs, obligation IDs, and source-rule IDs are identical and in the
same order.  There are no duplicates.  Each obligation's embedded source text,
span, normalized hash, source ID, and Lean-conjunct hash recomputes exactly.
The obligation-map hash is
`50df6c52253edba75c7fca885ab68012d994597e06afcbc249052c4d25c99630`.

The `∧ True` inside each cast equivalence is the faithful translation of
`#Ceil(@V)` after `V` is already sorted `Val`; it does not make the complete
equivalence vacuous.  The remaining side tests projection definedness against
the corresponding concrete constructor discriminator.  The dispatch
conjuncts retain their guards and full right-hand sides.  I found no irrelevant,
weakened, omitted, duplicated, or wholly vacuous conjunct.

The generated declaration is fixed as
`Klean160DoAlgebra.Lemmas.targetStatement`, with definition hash
`6c18f11d434a872569e371507143ffd1b3d761ef288046bff0b88b9d64bed407`
and statement hash
`4d877509120ffd208f5e3d828f09e969ca9354fc2a5dbbec4a3cfeeefcf0a8a5`.
The observed declaration, all eleven parameter bindings, complete statement,
and both hashes equal the generator manifest, generator sidecars, and both
target copies in `/audit-input.json`.  The full generation tree is
`94d9b05e9cb703925d5e8c24832d61a5cabc245a8b189055d0b4337e951c5d8f`,
also exactly recorded.  See `evidence/06_stage4-structural-independent.txt`.
The selected export status is `OK`, not `KLEAN_NO_OBLIGATIONS`.

## Stage 5 proof identity and trust accounting

I created fresh workspace `/tmp/audit-work/stage5-audit.HfRJIU`, copied the
candidate into it, and then copied the immutable generated project into
`Base`.  Both required commands were run there: `lake clean` exits 0 and
`lake build` exits 0.  Complete output is in
`evidence/07_stage5-clean-build.txt`.

After the build, `Base` still has tree hash
`0adc30863f031457992c6ea2ee486e335fa5361acc4ea9f2a2b45e9c88238f89`,
identical to the selected generated tree.  The target declaration and hashes
remain exact.  The candidate declares the target parameters only in namespace
`Proof`; it neither changes nor shadows the generated target declaration.  It
contains exactly one `theorem final` and no `sorry`, `admit`, `unsafe`, new
`axiom`, or new `opaque`.  Candidate integrity details are in
`evidence/11_target-and-candidate-integrity.txt`.

The trusted final gate independently recopied both inputs, cleaned, rebuilt,
type-checked `final` against the exact manifest statement, and passed.  Its
full report is `evidence/09_trusted-final-gate.txt`.  Therefore `Proof.final`
is not a duplicate or weakened theorem: its type is exactly the fixed
application of the generated target to the eleven candidate definitions.

The exact Lean output is:

`'Proof.final' depends on axioms: [propext, Classical.choice]`

The trust inventory hash is
`de2aea896d47ea6b53209d736f91bec0b2fd45cfefbfc2127d664676b01c1d31`
and records 50 generated trust declarations.  The trusted final-gate policy
reconciles that inventory with Lean's fixed foundation allowance
`Classical.choice`, `propext`, and `Quot.sound`.  Both reported dependencies
are in that fixed core set.  `Proof.final` depends on none of the 50 generated
trust declarations, no unrecorded declaration, and no `sorryAx`.  Exact output
and reconciliation are in `evidence/08_print-axioms.txt` and
`evidence/12_axiom-reconciliation.txt`.

## Operational bridge audit

The generated relational theorem could in principle be satisfied by
coordinated dishonest functions, so clean compilation and the theorem proof
were not treated as sufficient.  I located and inspected each exact candidate
`def`, followed its bound KORE symbol and source-rule IDs back to frozen
`verification.k`, and compared it with the supplied MPY rules and source
program:

| Target parameter | Candidate meaning | Operational judgment |
|---|---|---|
| `Int2String` | Lean integer `toString` | implements K's decimal `Int2String`; `-120` and `0` were tested |
| `applyBin` | delegates to `modelApplyBin` | relevant `"+"`, `str(A)`, `str(B)` branch returns `str(seqConcat(A,B))`, exactly frozen `str.k` and rule `732e3d...` |
| `applyBuiltin` | delegates to `modelApplyBuiltin` | relevant `"str"`/singleton integer branch returns decimal character codes, exactly frozen `builtins.k` and rule `532e0f...` |
| `codesProject` | extracts codes from the `Str` constructor | exactly `codesOf(projectStrTotal(V))` on the required string guard |
| `definedProjectInt` | true exactly on `SortVal.inj_SortInt` | exact constructor/domain test used by cast and `str` rules |
| `definedProjectStr` | true exactly on `SortVal.inj_SortStr` | exact constructor/domain test used by cast and addition rules |
| `projectIntTotal` | returns the integer payload | exact on its required guard; the `0` default is only a totalization outside the K cast's defined domain |
| `seqConcat` | structural recursion, empty-left base and cons recursion | exactly the two frozen `str.k` clauses |
| `strToCodes` | folds string characters to integer code points in order | exactly the frozen empty/recursive conversion and correct for every decimal result of `Int2String` |
| `project:Int?` | `some` exactly for a singleton-K integer injection | exact partial cast observation for rule `031285...` |
| `project:Str?` | `some` exactly for a singleton-K string injection | exact partial cast observation for rule `0dda33...` |

The arbitrary total defaults of `codesProject` and `projectIntTotal` occur only
outside the corresponding frozen partial cast's defined domain.  Every
generated use is guarded by the exact constructor predicate, so those defaults
neither add behavior to the source program nor make an obligation convenient.

I compiled adversarial evaluations over negative and zero integers, empty and
nonempty code sequences, wrong constructors, both partial projections, the
singleton-argument `str` dispatch, and string concatenation.  For example,
`-120` maps to `[45,49,50,48]`, `[65,66] ++ [43,42]` maps to
`[65,66,43,42]`, wrong-constructor projection is absent, and the relevant
dispatch branches return those exact code sequences.  Constant
`Int2String`, constant `codesProject`, left-identity `seqConcat`, and
constant-none `applyBuiltin` mutations all produced observably different
results on source-relevant inputs.  An always-failing cast projection was also
proved incompatible with the correct discriminator equivalence.  The complete
command, outputs, and interpretation are in
`evidence/10_operational-adversarial-tests.txt`.

These bodies implement the frozen operational meanings used by the four
obligations; they are not constants, identities, hard-coded witnesses, or
vacuous definitions.  The operational bridge therefore passes.

## Evidence index

- `evidence/00_lean-proc-compatibility-shim.txt`: sandbox diagnosis and exact shim.
- `evidence/01_environment.txt`: mode and primary input hashes.
- `evidence/02_inventory-command.txt`, `evidence/02_inventory.json`: trusted reconstruction.
- `evidence/03_stage3-structural-check.txt`: discovery-manifest bijection.
- `evidence/04_producer-authentication.txt`, `evidence/04b_producer-tree-authoritative.txt`: producer files, image, and authoritative tree hash.
- `evidence/05_preflight-rerun.txt` through `evidence/05d_preflight-rerun-shimmed.txt`: failed environment attempts and complete successful preflight result.
- `evidence/06_stage4-structural-independent.txt`: obligation/source/target/hash checks.
- `evidence/07_stage5-clean-build.txt`: fresh clean build.
- `evidence/08_print-axioms.txt`, `evidence/09_trusted-final-gate.txt`, `evidence/12_axiom-reconciliation.txt`: proof identity and trust accounting.
- `evidence/10_operational-adversarial-tests.txt`: operational and counterfactual tests.
- `evidence/11_target-and-candidate-integrity.txt`: immutable Base and candidate scan.
- `evidence/13_audit-input-and-source-hashes.txt`: audit-input contract, mounted tree hashes, and all 770 Stage 1 file hashes.
- `evidence/15_review-marker-validation.txt`: trusted final-marker normalization.

VERDICT: PASS
LEGITIMACY: LEGIT
