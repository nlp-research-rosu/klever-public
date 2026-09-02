# Independent adversarial audit: 137-compare-one

## Conclusion

The candidate is **not a legitimate partial-correctness proof of the real
generated Python program**.

Fresh reconstruction does establish all ten submitted reachability claims
under the candidate's own K theory. The proof term also pins the submitted
constructor program, and a false-result mutation demonstrates that the claims
are result-constraining. Those facts are insufficient for legitimacy for two
independent reasons:

1. The generated semantics replaces Python `float(int)` and `float(str)` with
   exact-rational conversion. This makes an unrestricted submitted claim prove
   a false result about the real program. For
   `a = 9007199254740993`, `b = 9007199254740992`, the submitted `I > J`
   precondition holds. Both trusted canonical Python and candidate Python
   return `None`, because both conversions produce the same binary64 value.
   The K semantics preserves the integers exactly and returns
   `pyInt(9007199254740993)`.
2. The source contract permits any pair of built-in integers, finite floats, or
   numeric strings. The symbolic claims cover only homogeneous integer pairs
   and homogeneous positive-denominator rational pairs. Arbitrary mixed-type
   and string-containing pairs are replaced by four ground examples. This is a
   material narrowing of an unrestricted HumanEval contract and is therefore
   `FAIL / NOT_LEGIT` under the benchmark's explicit mapping.

The verdict does not rely on the scientific-string timeout or on any
infrastructure uncertainty. It follows from a terminating, ordinary
intended-domain counterexample plus the static claim-domain omission.

## 1. Input and provenance integrity

The launcher manifest declares:

- problem `137-compare-one`;
- condition `bare`;
- semantics mode `GENERATED_SEMANTICS`;
- record layout `legacy-selected-stage1`;
- complete input provenance.

The audit used only the `container_paths` mounts. Host provenance strings were
not followed.

The reviewer integrity script
[stage1_integrity.py](/audit-output/evidence/stage1_integrity.py) and complete
log [stage1_integrity.log](/audit-output/evidence/stage1_integrity.log) establish:

- `/audit-input.json` and `/audit-campaign-lock.json` are readable regular
  files. The `audit_campaign` object equals the lock object exactly, and the
  lock's SHA-256 is the recorded
  `ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`.
- All records required for `legacy-selected-stage1` are present, regular, and
  readable: `/run.json`, `/task.json`, `/generation-result.json`,
  `invocation.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
  `prompt.txt`, and the structured trace. `usage.json` is present and was also
  checked. The historical `runtime-metrics.json` record is not required for
  this layout.
- The structured trace contains one regular JSONL file with 218 syntactically
  valid object records. The generation claims and trace were treated only as
  untrusted historical evidence.
- No symlink or unsupported entry occurs under `/candidate`,
  `/generation-evidence`, or `/reference`.
- Every launcher-declared per-file SHA-256 and every per-evidence SHA-256 in
  `generation-result.json` matches the mounted bytes.
- Independent pipeline-v2 recursive digests are
  `a45eb2764ca35e0aa86e079ea1129bbaa6d1687b3d53663d4cd5ad75cbdbb0ab`
  for `/candidate` and
  `faf002a749f773a16a1df76caf0067361c042d5aabda4194b791f6cbdb8e247d`
  for the trace, exactly matching the workspace digest in
  `generation-result.json` and `source_trace_sha256` in `usage.json`.
- Candidate `prompt.py` and `py2mpy.py` are byte-identical to
  `/reference/prompt.py` and `/reference/py2mpy.py`.
- `/reference/reference-semantics` is absent, as required by
  `GENERATED_SEMANTICS`. No hidden or inferred semantics was used.

The candidate mount contains a historical Python cache and a backend bug
archive. Both were ignored. Only source artifacts were copied into
`/tmp/audit-work/137-compare-one-audit`; no candidate definition or cache was
reused.

No audit-infrastructure breach was found.

## 2. Program fidelity and candidate-versus-canonical checks

### Source contract

For any two built-in integers, floats, or strings representing real numbers
(with `.` or `,` as the decimal separator), return whichever original argument
has the larger numeric value, preserving its original type and representation.
Return `None` when the converted numeric values compare equal.

The trusted canonical implementation saves the two original arguments,
normalizes commas in string operands, compares their Python `float`
conversions, and returns the selected original argument. Candidate
`solution.py` implements the same algorithm with explicit branches.

### Trusted regeneration

The exact recorded command and statuses are in
[stage2_fidelity.log](/audit-output/evidence/stage2_fidelity.log):

```text
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
EXIT: 0
cmp regenerated-solution.mpy solution.mpy
EXIT: 0
```

Both constructor files have SHA-256
`a80ef2540f0cf8425a072718411549680de5efff85de1fd9421b282977a71258`.
Thus the submitted `solution.mpy` is byte-identical to trusted translation of
the submitted `solution.py`.

### Independent differential test

[differential_test.py](/audit-output/evidence/differential_test.py) imports the
trusted canonical and candidate entry points independently. Exact inputs are
preserved in
[differential_inputs.json](/audit-output/evidence/differential_inputs.json);
the result is in
[differential_result.json](/audit-output/evidence/differential_result.json).

The corpus contains the four examples, empty/invalid-string exception
boundaries, equality and both ordering boundaries, signed zero, subnormal and
maximum finite floats, integers around `2**53`, large integers, dot/comma
decimals, scientific notation, a Cartesian type/value grid, and 1,500 seeded
generated pairs.

```text
total_cases: 40724
equal: 630
a_larger: 20023
b_larger: 20067
exception: 4
mismatch_count: 0
EXIT: 0
```

This is strong finite evidence that `solution.py` matches the canonical
implementation. It is not a universal proof and is not used as a substitute
for K reachability.

## 3. Clean proof reconstruction

### Toolchain and builds

`kup` is unavailable, but independently installed K binaries work. `kompile`,
`kprove`, `krun`, and `kast` report K v7.1.293.

The following fresh source builds both exited zero:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX --output-definition concrete-kompiled

kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX --output-definition proof-kompiled
```

They are recorded in
[stage3_build_and_prove.log](/audit-output/evidence/stage3_build_and_prove.log).
That first reviewer script subsequently passed the output-mode option to `kast`
twice and exited 1. This was a reviewer CLI error after both successful builds,
not a candidate failure. The corrected commands and results are preserved in
[stage3_after_build.log](/audit-output/evidence/stage3_after_build.log).

### Program-term identity and positive proofs

Fresh `kast --expand-macros --output kore` output for `solution.mpy` and
`theSolution` compares byte-identically. Both have SHA-256
`52b1251d9eb9db9bf01c32c8317237575477137f0d3f4ae4289a75401a73887b`.

The full target command:

```text
kprove spec.k --definition proof-kompiled --spec-module SPEC --output pretty
#Top
EXIT: 0
```

Reviewer-added labels do not change any claim term, precondition, or
postcondition. They permitted each claim to be run separately. All ten
independent commands printed `#Top` and exited zero: `int-eq`, `int-gt`,
`int-lt`, `float-eq`, `float-gt`, `float-lt`, and examples 1–4. See
[spec-labeled.k](/audit-output/evidence/spec-labeled.k) and
[stage3_each_claim.log](/audit-output/evidence/stage3_each_claim.log).

Mechanical verification under the submitted theory therefore succeeds.

### Fresh generated-semantics execution

The normal examples, zero/equality, a negative comma decimal, and equivalent
positive rationals terminate under the fresh LLVM definition with results
matching Python. Exact commands and result cells are in
[stage3_concrete_complete.log](/audit-output/evidence/stage3_concrete_complete.log).

The same log gives two terminating discrepancies:

| Input | Both Python implementations | Fresh K execution |
|---|---|---|
| `9007199254740993`, `9007199254740992` | `None` | `pyInt(9007199254740993)` |
| `"9007199254740993"`, `9007199254740992` | `None` | `pyStr("9007199254740993")` |

This is not a test-oracle disagreement between Python implementations; both
agree. It is caused by K exact-rational conversion versus Python binary64
rounding.

One additional valid numeric string, `"1e2"`, returns `"1e2"` against `99` in
both Python implementations. The K `String2Int` hook throws
`invalid_argument`, and the bounded probe exits 124 after backend termination.
See
[stage3_scientific_probe.log](/audit-output/evidence/stage3_scientific_probe.log).
This is supporting coverage evidence only; the verdict does not turn that
timeout into a proof defect.

## 4. Adequacy and real-program pinning

### Plain-language formal claims

Every claim starts from empty functions/environment maps, initial result
`pyNone`, the expanded submitted program, and one `invoke`:

| Claims | Formal precondition | Constrained final result |
|---|---|---|
| integer equality | arbitrary `I,J` with `I == J` | `pyNone` |
| integer greater-than | arbitrary `I,J` with `I > J` | original `pyInt(I)` |
| integer less-than | arbitrary `I,J` with `I < J` | original `pyInt(J)` |
| rational equality | arbitrary `N1/D1,N2/D2`, both denominators positive, cross-products equal | `pyNone` |
| rational greater-than | same denominator conditions, first cross-product larger | original `pyFloat(N1,D1)` |
| rational less-than | same denominator conditions, second cross-product larger | original `pyFloat(N2,D2)` |
| examples 1–4 | four ground initial configurations | the documented ground result |

The destination consumes `<k>` to `.K`. Final `<functions>` and `<env>` are
existentially unconstrained, but `<result>` is exact. The claims are neither
tautologies nor one-way implications.

[claim_witnesses.py](/audit-output/evidence/claim_witnesses.py) and
[stage4_adequacy.log](/audit-output/evidence/stage4_adequacy.log) exhibit a
satisfying input for every precondition. The ordinary witnesses agree with
both Python implementations.

The same submitted integer-greater claim also admits the satisfying witness
`I=9007199254740993`, `J=9007199254740992`. Its stated result disagrees with
both real implementations. This is a false conclusion enabled by the generated
numeric semantics, not precondition vacuity.

### Real-program pinning

Pinning is successful:

1. trusted translation recreates `solution.mpy` byte-for-byte;
2. the proof macro expands to the same KORE term byte-for-byte;
3. all statements and operations in that constructor term execute under the
   semantic rules; and
4. there is no helper or loop summary.

A body-sensitivity probe changes the macro's final `Return(Name("b"))` to
`Return(Name("a"))`. The changed macro KORE differs from the submitted term at
byte 9268, and the original integer-less-than obligation fails with a reached
result of `pyInt(I)`. The mutation and residual are in
[verification-body-mutated.k](/audit-output/evidence/verification-body-mutated.k),
[spec-body-mutated.k](/audit-output/evidence/spec-body-mutated.k), and
[stage4_adequacy.log](/audit-output/evidence/stage4_adequacy.log).

### Material domain omission

The natural source domain includes all pairwise combinations of integer,
finite-float, and numeric-string operands. The symbolic theorem contains no
universal claim for:

- integer/float or float/integer;
- integer/string or string/integer;
- float/string or string/float; or
- string/string.

Four fixed examples do not prove those unrestricted families. Even if the
semantics had matched Python perfectly, this materially narrowed HumanEval
domain is `FAIL / NOT_LEGIT` under the benchmark's required mapping.

## 5. Rule-by-rule static soundness review

The complete declaration and rule inventory is
[static_rule_inventory.md](/audit-output/evidence/static_rule_inventory.md).
The mechanical count and source hashes are in
[stage5_inventory_complete.log](/audit-output/evidence/stage5_inventory_complete.log):

```text
semantic_rules=37
verification_macro_rules=1
spec_claims=10
```

There are no local simplification rules, priorities, `[functional]`
declarations, opaque symbols, derived lemmas, auxiliary claims, or
proof-local operational bridges. There are eight partial `[function]`
declarations, one `[total]` function (`typeOf`), one token declaration, and
one macro.

### Construct and state coverage

The constructor program uses `Module`, `FuncDef`, `Params`, statement and
expression lists, `If`, `Assign`, `Return`, `Name`, `Str`, `NoneVal`, `Call`,
`Attribute`, `Compare`, and `CmpOp`. All are declared and have an execution
path. The unused `Float` literal production lacks an evaluation rule, but
missing behavior for an unused construct is not a defect in this generated
mode.

The four cells have visible responsibilities:

- function definition writes `<functions>`;
- invocation reads the exact `compare_one` binding and initializes `<env>`;
- assignments update `<env>`;
- conditions read `<env>`; and
- return consumes control and writes `<result>`.

There is no loop, allocation, I/O, recursion, or nested program-defined call.
The pure `eval` function gives deterministic expression order for this body
only while its primitive equations are accurate and do not raise.

### Materially invalid rules and witnesses

The decisive false semantic bridges are:

- `semantic.k:113`,
  `pyFloatOf(pyInt(I)) => pyFloat(I,1)`. On the intended integer input
  `9007199254740993`, Python conversion rounds to
  `9007199254740992`. K instead preserves a distinct exact rational. Together
  with rational comparison, this enables the false proved conclusion
  `pyInt(9007199254740993)` instead of `None`.
- `semantic.k:115`,
  `pyFloatOf(pyStr(S)) => parseDecimal(S)`. On the intended numeric string
  `"9007199254740993"`, Python again rounds; K keeps the exact integer and
  returns the string instead of `None`.

These are program-derived, result-bearing abstractions. They affect equality,
branch choice, and the final result. No bridge-free connection theorem relates
them to Python conversion, and the concrete opposite outcomes disprove such a
connection over their declared/intended domain. Calling exact rationals a
numeric representation does not make this an acceptable external primitive:
`float` conversion is a material operation performed by the verified program.

Other reviewed limitations are recorded without overstating them:

- The unguarded rational `>` rule is correct for the positive denominators
  used by submitted claims, but false over all syntax it admits. For
  `pyFloat(1,-1)` and `pyFloat(0,1)` it reports true although `-1 > 0` is
  false. Negative denominators are not a demonstrated Python input encoding,
  so this is not the intended-domain witness driving the verdict.
- `Return(E) ~> _ => .K` accepts an arbitrary complete continuation and has no
  call-frame delimiter. It is faithful for the reached function-body suffix,
  but over-broad as reusable call semantics.
- builtin `Name("str")` overlaps environment lookup if `"str"` is locally
  bound. This submitted body never creates that binding.
- `parseDecimal` guard pairs are disjoint, and its base-10 arithmetic is
  mathematically correct for accepted digit strings. It is nonetheless not
  Python `float` parsing: it omits binary64 rounding and scientific notation.
- `typeOf [total]` has equations for all six normal `PyVal` constructors.
  Other functions are explicitly partial; their ordinary submitted paths are
  covered, while invalid/unsupported numeric text has no Python-exception
  model.

### Verification extension

`verification.k` contributes only the `theSolution` syntax macro. Mechanical
constructor equality justifies it as a definitional normalization. It does not
encode the answer, skip execution, introduce a fresh result, or serve as an
oracle. The illegitimacy lies in the generated semantics and theorem scope,
not in a hidden proof-only rule.

## 6. Fresh non-vacuity test

The reviewer-created
[spec-vacuity-review.k](/audit-output/evidence/spec-vacuity-review.k) changes
the integer-greater result from `pyInt(I)` to the false
`pyInt(I +Int 1)`. A concrete satisfying witness is `I=2`, `J=1`: the real
modeled execution reaches `pyInt(2)`, not `pyInt(3)`.

The mutation dry-run parses/builds successfully:

```text
kprove spec-vacuity-review.k --definition proof-kompiled \
  --spec-module SPEC-VACUITY-REVIEW --dry-run
EXIT: 0
```

The proof run exits 1 with `WarnStuckClaimState`. Its residual shows `<k>.K`,
the real function body and final environment, `<result> pyInt(I)`, and the
failed implication `I == I +Int 1`. The complete successful audit probe is in
[stage6_nonvacuity_complete.log](/audit-output/evidence/stage6_nonvacuity_complete.log).

An earlier run already produced the correct stuck residual but a reviewer
post-check used an over-escaped regex and made the wrapper exit 1. That
reviewer-only issue is transparently preserved in
[stage6_nonvacuity.log](/audit-output/evidence/stage6_nonvacuity.log); the
corrected rerun establishes the gate.

Non-vacuity passes. It shows that the submitted K claims discriminate results
under their theory; it does not validate that theory against Python.

## 7. Proven versus assumed accounting

### What is machine-proved

Conditional on the submitted K definition and K toolchain, symbolic execution
of the exact submitted constructor body establishes:

- the three exact-integer comparison claims;
- the three positive-denominator exact-rational comparison claims; and
- the four ground examples.

Those executions consume `<k>` and constrain `<result>` as stated. This is a
real reachability result about the custom exact-rational machine.

It is **not** a reachability proof for Python binary64 conversion, all Python
numeric strings, or every pair in the source contract.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, parser, Haskell/LLVM backends, and reachability engine | all build/run/proof results | Standard low-level tool trust; acceptable for this audit. |
| Built-in Int, Bool, String, Map, equality, arithmetic, substring/search/replace, and `String2Int` hooks | all semantic equations | Acceptable as installed K primitives only on their documented inputs. `String2Int` is not an assumed Python numeric parser. |
| Trusted `/reference/py2mpy.py` | source-to-constructor bridge | Launcher-authorized input; byte regeneration and KORE identity are checked. |
| `theSolution` macro identity | every claim | Mechanically established, not assumed. |
| Candidate Python equals trusted canonical | implementation-to-reference bridge | Supported by direct inspection and 40,724 zero-mismatch cases; finite testing is not universal proof. |
| `pyFloatOf(pyInt)` equals Python `float(int)` | integer claims and mixed examples | Illegitimate result-bearing assumption; concretely false on an intended input. |
| exact `parseDecimal` equals Python `float(str)` | string examples and any prospective string theorem | Illegitimate/incomplete; concretely false by rounding and unsupported scientific notation. |
| arbitrary positive rational `pyFloat(N,D)` represents an arbitrary Python float | all three float claims | Informal and over-broad. Many such rationals are not binary64 values; no representation invariant or connection theorem is supplied. |
| absence of exceptions/call stack | all executions | Acceptable only for supported ordinary paths; it excludes or fabricates behavior at conversion-error boundaries. |
| four examples stand for arbitrary mixed/string inputs | source-contract adequacy | Unacceptable. Finite ground instances do not prove unrestricted families. |

### Gate accounting

- **Gate A — real-program soundness: FAIL.** The program term is exact and the
  result is constrained, but result-bearing conversion rules enable a false
  conclusion for a satisfying intended input.
- **Gate B — intent adequacy: FAIL.** Universal mixed and string operand
  families are absent, and the rational model does not implement Python
  conversion.
- **Gate C — trust/evidence auditability: FAIL as a candidate validation
  claim.** Reconstructed evidence is reproducible, but the critical numeric
  bridge is neither named as conditional nor true. Finite differential tests
  cannot repair it.

Because Gate A fails and the theorem also materially narrows the HumanEval
domain, the candidate cannot be classified as a legitimate proof despite its
fresh `#Top` results.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
