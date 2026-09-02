# Independent audit: 81-numerical-letter-grade

## Scope and result

I independently audited Stage 3 classification, deterministic Stage 4
generation, and the Stage 5 Lean proof for:

- problem: `81-numerical-letter-grade`
- condition: `kit-semantics`
- semantics mode: `SUPPLIED_SEMANTICS`
- audit mode: `CLASSIFICATION_AND_PROOF`

Stage 3 and Stage 4 are structurally and mathematically correct. The Lean
project builds cleanly, `Proof.final` has the exact fixed target type, and its
three axioms are recorded in the immutable trust inventory. The overall audit
nevertheless fails: the candidate's definition of the full KORE `applyCmp`
symbol is a theorem-shaped hard-coding, not the frozen symbol's operational
meaning. Concrete integer comparisons expose the mismatch.

## 1. Frozen Stage 1 inventory reconstruction

I ran the trusted `/reference/tools/k_rule_inventory.py` implementation
directly on `/reference/k-proof`. It selected `VERIFICATION`; its local module
closure contains only that module. The frozen source and reconstructed
inventory are:

- `verification.k` SHA-256:
  `b2323c2e29dd519f7c6457aac14996b82d5bd34e3eb9c6a939a6576d8b81f232`
- rule count: 16
- inventory SHA-256:
  `00b871c4197f4e4b8c563bbbfd4e2d0186e6f8ce8b19b803de1e23228bec6727`

For every rule, the trusted reconstruction recomputed the physical source
span, whitespace-normalized source hash, and
`source_rule_id = "rule-" + normalized_sha256`. The complete raw inventory is
in [01-inventory-reconstruction.txt](/audit-output/evidence/01-inventory-reconstruction.txt).

The comparison with `/reference/lemma-discovery.json` is bijective:

- 16 reconstructed and 16 classified entries;
- both lists contain 16 unique IDs;
- IDs are identical in source order;
- no omitted, duplicated, or extra IDs;
- every ID equals its recomputed normalized hash;
- reconstructed and protected whole-inventory hashes are identical.

The raw comparison is in
[02-stage3-bijection.txt](/audit-output/evidence/02-stage3-bijection.txt).

## 2. Independent rule classification

My classification is 14 `DEFINITION`, 2 `DOMAIN_LEMMA`, 0
`OPERATIONAL_RULE`, and 0 `PROVED_DERIVED_LEMMA`.

| Lines | Normalized hash | Classification | Independent reason |
|---:|---|---|---|
| 9-46 | `913248f07e570f8e9cf4e10ccd2e45330ef636bc76303ff5ad67835ed0374797` | `DEFINITION` | `GRADE-STEP` is a compile-time macro naming the exact nested source AST. |
| 49-57 | `ab056d115b33e511e623da01fcf497700ccb79847bda7824277b21bcbf6345af` | `DEFINITION` | `GRADE-PROGRAM` names the whole translated program AST. |
| 61 | `9407ea7d6a4de9439363534f67694ee47e6ff907df9b35ff34b4a866b6602e7b` | `DEFINITION` | Defines the numeric-domain predicate. |
| 64 | `c7226673454c9937bb81a182a982d47a41b4594d2a6ea2a53b050512a0f2120a` | `DEFINITION` | Empty-sequence base equation for `allGradeNumbers`. |
| 65-66 | `43811671f02c87468177174e87d1e0fa17daa38184b24c78d16b3da6de2f02be` | `DEFINITION` | Structural recurrence for `allGradeNumbers`. |
| 72 | `4aeb120c39e619e56b1bb2949769afb0de9f65a14815f8f8304abf8eabb853b0` | `DEFINITION` | Integer case of the named `gradeEq` summary. |
| 73 | `4b0057401ad369826c0c0f086d2de62b6bbdf480fcdb4ce5c3b9324e5f6b73cb` | `DEFINITION` | Float case of `gradeEq`. |
| 74-75 | `1dcc8c06aaff13c93012f8657da7bc9eee86e8cd2b9481c7d964bc6d833b79f8` | `DEFINITION` | Guarded nonnumeric totalization of `gradeEq`. |
| 78 | `8b8204b28122ab97e84e35c1504bdd05d5beed4934819f44dabcbedbc9f85f32` | `DEFINITION` | Integer case of the named `gradeGt` summary. |
| 79 | `5e4220b4a59610d50f112f372bc52b526f8251e55fcb996f2f236bbe7a0db863` | `DEFINITION` | Float case of `gradeGt`. |
| 80-81 | `5924db7e5f35f3f96f7f05931067b1ad392bdb7dcfde5b27f1927e6c1875992c` | `DEFINITION` | Guarded nonnumeric totalization of `gradeGt`. |
| 84-87 | `bb0819476c6343e9119c99a78b2ae8eb72ebad42dbc170a9eaa3c4af6f39f115` | `DOMAIN_LEMMA` | Guarded dynamic equality dispatch for the pre-existing operational `applyCmp` symbol. |
| 88-91 | `79c1c8d9ff74acff507b7b4a319ee7d9d034df3550afdf9196f29291297713c8` | `DOMAIN_LEMMA` | Guarded dynamic greater-than dispatch for `applyCmp`. |
| 96-133 | `c5a38f6c6613309dfda5d4776797f7bf662da9f4d9a3f34f58ebec448836c677` | `DEFINITION` | Defines the ordered one-element `gradeValue` summary. |
| 138 | `f3847c739a1d22b36c279a649f98bc18c2073c8ec8582b54956c1f02f33dc66c` | `DEFINITION` | Empty-suffix base equation for `gradeAcc`. |
| 139-143 | `954dcecb4ff810ef1b6ce869747c0457f931b774b64fd1f2197b5d3a0265ac57` | `DEFINITION` | Tail recurrence for `gradeAcc`. |

The two dispatch rules are not definitions: their left side is the
pre-existing MPY operational symbol. They are not proved derived lemmas,
because Stage 1 compiles them into `VERIFICATION` before proving the target and
contains no earlier proof of the exact rules against a module with those rules
removed. They are domain lemmas.

Both are relevant. The source function compares each dynamic grade with Float
thresholds: equality at `4.0`, followed by strict greater-than comparisons.
The supplied semantics separately defines `applyCmp` on Int/Float and
Float/Float operands; the two domain lemmas combine those cases under
`isGradeNumber`. Both and only `[simplification]` rules are therefore
`DOMAIN_LEMMA`, satisfying the simplification-class restriction. The detailed
classification is preserved in
[02b-independent-classification.txt](/audit-output/evidence/02b-independent-classification.txt).

The true domain set is nonempty, so `KLEAN_NO_OBLIGATIONS` would have been
wrong. Stage 4 correctly generated two obligations.

## 3. Generator producer provenance

Before judging Stage 4, I hashed the mounted generation-time producers:

- `klean_export.py`:
  `bbd11ce0fe6ac12ea89d4bdc70c260044bc9f87c987ff310684b637ea6464a07`
- `klean.py`:
  `42a38e6d65b74af3536acc49947b7cfbac809406bdfe5549841e3132af5a5c4d`

Each matches both `source-manifest.json` and `generator-manifest.json`. The
producer-tree hash is
`388cac39f4f89b5a912d2628ef5c7963e791f5ed775cf1e9606fe64dcfd5f11e`,
exactly the value in `/audit-input.json`.

The source manifest and generator manifest both record immutable generator
image
`sha256:f884238cea5ab1ed0da0a75d0c9a29ac4abe988616c3f493ba60e74ca3290cf7`.
The same digest is the terminal component of the image-addressed producer path
in `/audit-input.json`. There is no producer-source infrastructure error.
Raw evidence is in
[03-producer-provenance.txt](/audit-output/evidence/03-producer-provenance.txt).

## 4. Deterministic Stage 4 generation

I reran `tools.klean_preflight.check_generation` with `PYTHONPATH=/reference`,
the required Stage 1 workspace, discovery manifest, generation, and pinned
toolchain lock.

The first invocation exposed a sandbox PID/procfs namespace mismatch: Lean
4.22 tries `/proc/<getpid()>/exe`, while this sandbox returns an inner PID
against parent-namespace procfs. A minimal preload compatibility shim supplied
the procfs-visible PID; it did not modify Lean, the generated project, or the
trusted checker. Under that shim the pinned Lean identified itself as version
4.22.0 at commit
`ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05`, and the unmodified checker
completed successfully. The diagnosis, source, commands, and initial failure
are in
[05-preflight-environment.txt](/audit-output/evidence/05-preflight-environment.txt)
and
[getpid_procfs_compat.c](/audit-output/evidence/getpid_procfs_compat.c).

The returned preflight evidence reports:

- status `PASS`;
- Stage 1 tree:
  `4e9649cf9fb4ccc09350c7e18186b0e0b7570d75167492abb453f7b3a33a7ab8`;
- Stage 3 manifest:
  `5f03f6a223a8ea831acacf3471470a8edf5763001879e7a8c533e3fbf4ccca5d`;
- generated tree:
  `6605b72d5f62c698fc9e460110023b0818ceeb0e036858d36de34c384ad0161e`;
- two obligations;
- 50 generated trust declarations;
- zero designated sorries;
- successful `lake clean` and `lake build`.

The exact returned document is
[06-preflight-rerun.json](/audit-output/evidence/06-preflight-rerun.json).

I also independently recomputed every material recorded hash. The Stage 1
tree, discovery file, verification source, generated tree, obligation map,
trust inventory, producer tree, and both producer files all match their
manifests and `/audit-input.json`. All independent checks are `true`; the
reproducible script and result are
[stage4_independent_checks.py](/audit-output/evidence/stage4_independent_checks.py)
and
[04-stage4-hash-bijection.txt](/audit-output/evidence/04-stage4-hash-bijection.txt).

### Obligation bijection and mathematical identity

The two generated obligations occur once each, in source order:

1. `rule-bb0819…f115`, lines 84-87: for numeric `V`, `applyCmp "==" V
   (inj_Float F) = gradeEq V F`.
2. `rule-79c1c…13c8`, lines 88-91: for numeric `V`, `applyCmp ">" V
   (inj_Float F) = gradeGt V F`.

Their source IDs, normalized hashes, spans, inventory hash, discovery hash,
Lean conjunct hashes, and order all match. There are no duplicate, missing, or
extra obligations. The operator strings, dynamic left operand, injected Float
right operand, and translation of the K `requires isGradeNumber(V)` clause to
`isGradeNumber V = true` are exact. Neither conclusion is weakened, and the
intended guard is satisfiable; the Lean adversarial check evaluates it to
`true` for an injected integer.

The generated target is exactly the conjunction of those two obligations, with
no additional or vacuous conjunct:

`Klean81NumericalLetterGrade.Lemmas.targetStatement
«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»
«gradeEq(_,_)_VERIFICATION_Bool_Val_Float»
«gradeGt(_,_)_VERIFICATION_Bool_Val_Float»
«isGradeNumber(_)_VERIFICATION_Bool_Val»`

Its definition hash is
`40098983cd633833d65c09f60c20fedcb1a20d9382b4e0e5b2a3dc8d8018e619`;
its instantiated-statement hash is
`f486a227f41afc456b054856aba86cf4116399675f7f861ef1387a23b4e3b17b`.
Those values and the complete target record are identical in the generator
manifest, trusted preflight result, generated source, and `/audit-input.json`.
See
[16-generated-obligations.txt](/audit-output/evidence/16-generated-obligations.txt).

## 5. Fresh Stage 5 build and source checks

I created `/tmp/audit-work/stage5-audit-81`, copied the immutable generated
project into it as `Base`, copied the candidate's three source/configuration
files to the root, then ran:

```text
LD_PRELOAD=/tmp/audit-work/getpid_procfs_compat.so lake clean
LD_PRELOAD=/tmp/audit-work/getpid_procfs_compat.so lake build
```

Both commands exited 0. `Proof` and all Base modules rebuilt successfully;
only unused-variable linter warnings appeared. Complete output is in
[07-fresh-lake-clean.log](/audit-output/evidence/07-fresh-lake-clean.log) and
[08-fresh-lake-build.log](/audit-output/evidence/08-fresh-lake-build.log).

After the build:

- the fresh `Base` tree still hashes to the immutable generated-tree hash;
- the target record in fresh `Base` equals the generator manifest and audit
  input;
- the fresh target file is byte-identical to the selected generated target;
- the candidate tree hash equals the Stage 5 workspace hash in the audit input;
- the copied `Proof.lean` is byte-identical to `/candidate/Proof.lean`;
- candidate Lean sources contain no `sorry`, `admit`, `unsafe`, `axiom`, or
  `opaque`;
- the candidate does not declare or shadow `targetStatement`.

See
[09-candidate-and-target-identity.txt](/audit-output/evidence/09-candidate-and-target-identity.txt)
and
[10-candidate-forbidden-scan.txt](/audit-output/evidence/10-candidate-forbidden-scan.txt).

## 6. Proof identity and axiom accounting

Lean's `#check` and `#print` show that `Proof.final` has exactly the fixed
generated target applied to the candidate's four parameter definitions. It
does not prove a duplicated or separately weakened proposition. Exact output
is in [11-theorem-check.txt](/audit-output/evidence/11-theorem-check.txt).

Running Lean with `#print axioms Proof.final` produced exactly:

```text
[«Int2Float(_,_,_)_FLOAT_Float_Int_Int_Int»,
 «_==Float_»,
 «_>Float__FLOAT_Bool_Float_Float»]
```

All three are unique entries in `trust-inventory.json`, each an axiom in the
generated `Func.lean` trust boundary. There is no `sorryAx` and no unrecorded
dependency. Exact output and reconciliation are in
[12-axioms.txt](/audit-output/evidence/12-axioms.txt) and
[13-axiom-reconciliation.txt](/audit-output/evidence/13-axiom-reconciliation.txt).

These checks establish syntactic proof hygiene and kernel acceptance. They do
not repair an incorrect operational parameter.

## 7. Operational-bridge audit

The four generated target parameters bind exact KORE symbols:

| Parameter | Bound frozen rules | Independent judgment |
|---|---|---|
| `isGradeNumber` | both domain lemmas | Adequate. It delegates to the generated total definition of the frozen `isInt(V) orBool isFloat(V)` rule; an injected integer evaluates to `true`. |
| `gradeEq` | equality domain lemma | Adequate relative to generated trust. It totalizes the exact three frozen definition cases: Int via `intToF/eqF`, Float via Float equality, and guarded nonnumeric `false`. |
| `gradeGt` | greater-than domain lemma | Adequate relative to generated trust. It totalizes the exact Int, Float, and guarded nonnumeric frozen cases. |
| `applyCmp` | both domain lemmas | **Failure.** The candidate implements only the two theorem patterns and returns `false` for all other operands/operators, although the bound KORE symbol has many defined frozen operational cases. |

The candidate's `applyCmp` definition checks only:

- operator `"=="` or `">"`;
- a right operand constructed as `SortVal.inj_SortFloat`;
- a true numeric guard;

and otherwise returns `false`. The frozen operational symbol also has ordinary
rules for Int/Int comparisons, reverse Float/Int comparisons, `!=`, `<`, `<=`,
`>=`, and Bool, String, List, Set, Dict, and `None` cases. This is exactly the
kind of convenient, target-shaped definition the operational-bridge gate
forbids.

Two compiled adversarial witnesses are decisive:

- candidate `applyCmp("==", inj_Int 7, inj_Int 7) = false`, while frozen
  `MPY-INT` rewrites it to `7 ==Int 7 = true`; the generated `_==Int_` hook
  also reduces to `some true`;
- candidate `applyCmp(">", inj_Int 2, inj_Int 1) = false`, while frozen
  `MPY-INT` rewrites it to `2 >Int 1 = true`; the generated `_>Int_` hook
  also reduces to `some true`.

The Lean file also proves that the intended numeric guard is satisfiable. A
counterfactual `applyCmp` that agrees only on the two generated patterns but
returns the opposite value (`true`) everywhere else still proves the fixed
target. Thus the target cannot distinguish arbitrary off-pattern behavior, and
the candidate did not supply the independently required operational meaning.

The adversarial file compiled with exit 0:
[OperationalBridgeCheck.lean](/audit-output/evidence/OperationalBridgeCheck.lean)
and
[14-operational-bridge-check.txt](/audit-output/evidence/14-operational-bridge-check.txt).
The corresponding frozen rules are preserved in
[15-fixed-semantics-applyCmp.txt](/audit-output/evidence/15-fixed-semantics-applyCmp.txt).

## 8. Final judgment

The protected Stage 3 classification is independently confirmed. Stage 4 has
authentic producer provenance, exact source/obligation bijection, an unchanged
target, and a successful trusted preflight. The Stage 5 theorem is cleanly
built and has a clean, fully recorded axiom list.

Nevertheless, `Proof.final` is instantiated with an `applyCmp` implementation
that demonstrably disagrees with the frozen operational semantics. A clean
build and clean axiom list are necessary but not sufficient; this operational
bridge failure requires `FAIL` / `NOT_LEGIT`.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
