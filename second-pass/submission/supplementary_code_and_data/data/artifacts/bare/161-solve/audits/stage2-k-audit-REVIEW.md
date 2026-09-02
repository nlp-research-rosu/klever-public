# Independent adversarial review — 161-solve

This audit used the required Kit order (`using-kit`, `validating-proof`, and,
because this is `GENERATED_SEMANTICS`, `writing-semantics`). I treated all
candidate and generation material as untrusted. There was no audit
infrastructure breach, so a candidate verdict is appropriate.

## 1. Input and provenance integrity

`/audit-input.json` declares:

- problem `161-solve`, condition `bare`;
- record layout `legacy-selected-stage1`;
- semantics mode `GENERATED_SEMANTICS`;
- `mount_reference_semantics: false`.

The campaign object in `/audit-input.json` is exactly equal to
`/audit-campaign-lock.json`. The lock hash and all launcher-recorded individual
hashes checked by the reviewer match: canonical, trusted prompt, trusted
translator, run manifest, task manifest, stage-one result, invocation, metrics,
usage, generation prompt, `codex-last.txt`, `codex-output.log`, and the
structured trace file. The structured trace has 199 valid JSON records and no
parse errors. The trace and generation logs claim a successful `#Top`; that
claim was not used as proof evidence.

All records required for `legacy-selected-stage1` are present and readable:
`/run.json`, `/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, `prompt.txt`, and the trace tree. `usage.json` is present
and was inspected. Historical runtime metrics are not required for this legacy
layout. No required mount or record is missing, mistyped, or symlinked.

The candidate's `prompt.py` and `py2mpy.py` are byte-identical to the trusted
`/reference` copies. `/reference/reference-semantics` is absent, as
`GENERATED_SEMANTICS` requires. The candidate contains all required proof
sources: `solution.py`, `solution.mpy`, `semantic.k`, `verification.k`,
`spec.k`, and `prove.sh`. There are no candidate helper K files.

Evidence:

- `evidence/01_provenance.sh` and `evidence/01_provenance.log`
- `evidence/01_trace_inspection.py` and
  `evidence/01_trace_inspection.log`

Stage 1 result: PASS.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For each character in the input Python string:

1. if it is a letter, replace it with its opposite case;
2. otherwise leave it unchanged;
3. if the complete string contains no letters, reverse the complete string.

The trusted canonical implements this character-by-character using
`i.isalpha()` and `i.swapcase()`.

The candidate is:

```python
def solve(s):
    return s.swapcase() if any(c.isalpha() for c in s) else s[::-1]
```

It has the right signature and passes the three examples and ordinary ASCII
boundaries. Trusted regeneration with `/reference/py2mpy.py` is byte-identical
to submitted `solution.mpy` (both SHA-256
`914d9811632a2b1c06304570e53c89b82af04a1c79fdde6d9f7e11b42e8d94eb`).

However, whole-string `str.swapcase()` is not universally equivalent to joining
the swapcase of each character. Python's contextual lowercase mapping for
Greek capital sigma supplies concrete contract-domain counterexamples:

| Input | Trusted canonical / character oracle | Candidate |
|---|---|---|
| `"ΟΣ"` | `"οσ"` | `"ος"` |
| `"AΣ"` | `"aσ"` | `"aς"` |
| `"ΣΣ"` | `"σσ"` | `"σς"` |
| `"ΜΆΙΟΣ"` | `"μάιοσ"` | `"μάιος"` |

The independent differential script imports both entry points and uses a third,
direct character-by-character contract oracle. It covers the documented
examples, empty and branch-boundary strings, ASCII boundaries, Unicode
case-mapping boundaries, all strings of lengths 0 through 3 over a
ten-character mixed alphabet, and 2,000 fixed-seed generated strings. It
reports 2,869 unique inputs and the four mismatches above. Its exit status is
1 because those are real result divergences, not a test failure.

Evidence:

- `evidence/02_differential.py`
- `evidence/02_run_python_checks.sh`
- `evidence/02_python_checks.log`

Stage 2 result: FAIL. The generated Python implementation itself is not
equivalent to the trusted canonical over the unrestricted Python-string
contract.

## 3. Clean proof reconstruction

I copied only source artifacts to `/tmp/audit-work/k-proof`; no
candidate-provided compiled definition or cache was copied. With K
v7.1.293 I independently:

1. regenerated and compared `solution.mpy`;
2. compiled `semantic.k` with the Haskell backend into
   `fresh-semantic-kompiled`;
3. executed the exact submitted `solution.mpy` on normal, empty, ASCII
   boundary, and Unicode boundary inputs;
4. compiled `verification.k` into `fresh-verification-kompiled`;
5. ran the only positive target claim in `SPEC`.

Both definitions compiled with exit 0. The sole `kprove` command exited 0 and
printed exactly `#Top`.

The normal concrete runs agree with Python:

- `"1234"` produces code points `[52, 51, 50, 49]`;
- `"ab"` produces `[65, 66]`;
- `"#a@C"` produces `[35, 65, 64, 99]`;
- `""` produces the empty `PString`;
- `"@A[\`a{"` produces `[64, 97, 91, 96, 65, 123]`.

The Unicode runs expose that the freshly rebuilt semantics does not execute
the real Python operations:

| Input | Candidate Python | Candidate K semantics |
|---|---|---|
| `"éa"` | `"ÉA"` = `[201, 65]` | `[233, 65]` |
| `"ß1"` | `"SS1"` = `[83, 83, 49]` | `[49, 223]` |

These are normal terminating inputs satisfying the source signature. The K
results follow from the candidate's ASCII-only letter predicate and one-code-
point toggle, not from Python `isalpha()` and `swapcase()`.

Evidence:

- `evidence/03_reconstruct_and_run.sh`
- `evidence/03_reconstruction.log`

Stage 3 reconstruction result: the positive K claim closes, but concrete
semantic fidelity FAILS.

## 4. Adequacy and real-program pinning

### Formal claim in plain language

The claim has no `requires` or `ensures`, so its logical precondition is `true`.
For every `S:PString` and arbitrary `Exprs` values in the two call-argument
positions, it starts with:

- the exact `solve` name;
- the exact one-parameter binding `Params("s")`;
- the submitted conditional-expression body, except that the two call argument
  lists are claim variables;
- input cell `S`;
- result cell `noResult`.

It requires execution to consume `<k>` and change `<result>` to:

```text
expected(S)
= ifPString(hasAlpha(S), swapCase(S), reverse(S))
```

This is result-constraining inside the candidate theory. It is not a free
result, implication-only postcondition, or tautological destination cell.

The precondition is satisfiable. Examples include `S = .PString` and
`S = 97 :: 98 :: .PString` (`"ab"`), with the exact submitted program in
`<k>` and `noResult` in `<result>`. For `"ab"`, the claimed K result `[65, 66]`
agrees with both Python implementations. For `"éa"`, the claimed result is
`[233, 65]`, while both Python implementations return `[201, 65]`.

### Mechanical program pinning

I emitted the compiled claim as KAST JSON, parsed the regenerated ground
`solution.mpy` as KAST JSON, extracted the claim's `<k>` left-hand side, and
performed constructor-level unification. The ground program contains no K
variables. It unifies exactly with the claim pattern using only:

```text
_ISALPHA_ARGS -> empty Exprs list
_SWAPCASE_ARGS -> empty Exprs list
```

Thus the exact regenerated program is genuinely an instance of the theorem;
this is not a substituted-program failure. The claim is unnecessarily broader
than the real body, and that breadth becomes unsound because semantic rules
ignore those arguments, but the ground submitted program itself is pinned.

There are no helper or loop claims. The complete control path is the top
`Module/FuncDef/Return` rule followed by `evalString` and its helper functions.

Evidence:

- `evidence/04_pinning_commands.sh`
- `evidence/04_program_pinning.py`
- `evidence/04_pinning.log`

Stage 4 result: real-program constructor pinning and local result constraint
PASS; source-contract adequacy FAILS.

## 5. Rule-by-rule static soundness review

### Complete local declaration inventory

`MPY-SYNTAX` declares:

- `Exprs ::= List{Expr, ","}`;
- `Params(String)`;
- expression forms `Name`, `Str`, `Bool`, `Int`, `UnaryOp`, `Attribute`,
  `Call`, `IfExp`, `GenExp`, and `Subscript`;
- `CompFor`;
- `SliceBound ::= NoBound | Expr` and `Slice`;
- statements `Return` and `FuncDef`;
- `Stmts ::= List{Stmt, ""}`;
- `Program ::= Module(Stmts)`.

`SEMANTIC` declares:

- `PString ::= .PString | Int :: PString | pstr(String)`;
- function `pstr` and function `pstrAt`;
- total functions `isAlpha`, `toggle`, `hasAlpha`, `swapCase`, `reverse`,
  `reverseAcc`, and `ifPString`;
- functions `evalBool` and `evalString`;
- `Result ::= noResult | PString`;
- one configuration with `<k>`, `<input>`, and `<result>`.

`VERIFICATION` declares the total function `expected`. `SPEC` contains one
unlabeled reachability claim. There are no local opaque symbols, priority
rules, `[simplification]` rules, `[concrete]` rules, macros, `[functional]`
declarations, auxiliary claims, or local lemmas. The only attributes affecting
equations are `[function]` and `[total]`.

The exact submitted term maps to the semantics as follows:

| Used constructor | Declaration and behavior |
|---|---|
| `Module`, `FuncDef`, `Params`, `Return` | Top operational rule R21 |
| outer `IfExp` | `evalString` R18 |
| `Call(Name("any"), GenExp(...))` | `evalBool` R17 |
| `Call`, `Attribute`, `Name`, `CompFor`, `Bool(true)` for `isalpha` generator | Syntactically matched and summarized by R17 |
| `Call(Attribute(Name("s"),"swapcase"), empty)` | `evalString` R19 |
| `Subscript`, `Slice`, two `NoBound`, `UnaryOp("-",Int(1))` | `evalString` R20 |
| empty `Exprs` lists | Generated list syntax; matched by claim variables and ignored by R17/R19 |

Unused syntax needs no behavior in a minimal generated semantics. The defect is
not lack of unused Python coverage; it is false behavior for constructs the
submitted program actually uses.

### Exhaustive rule inventory and decisions

| Rule | Exact role | Decision |
|---|---|---|
| R1 `pstr(S) => pstrAt(S,0)` | Concrete input bridge | Sound for the tested embedding. |
| R2 `pstrAt` at `I >= lengthString(S)` | Terminates conversion | Guard is disjoint from R3 and correct for reachable nonnegative indices. |
| R3 `pstrAt` at `I < lengthString(S)` | Appends `ordChar(substrString(...))` and increments | Correct for the reachable conversion path, conditional on K String hooks. |
| R4 `isAlpha(C)` | Defines only ASCII `[A-Z]` or `[a-z]` | **Unsound as Python `str.isalpha` semantics.** At `C=233` (`é`), it concludes false although Python concludes true. |
| R5 `toggle` uppercase ASCII | Adds 32 | Correct on its ASCII guard. |
| R6 `toggle` lowercase ASCII | Subtracts 32 | Correct on its ASCII guard. |
| R7 `toggle` when `not isAlpha` | Leaves code point unchanged | **Unsound as Python `swapcase`.** At `C=233` it yields 233 instead of 201; at `C=223` (`ß`) Python yields two code points `[83,83]`, which this `Int -> Int` function cannot express. |
| R8/R9 `hasAlpha` empty/cons | Recursive existential letter test | Structurally total and terminating, but inherits R4's false meaning. For `233::.PString`, it yields false while Python `any(ch.isalpha())` yields true. |
| R10/R11 `swapCase` empty/cons | Pointwise use of `toggle` | Structurally total and terminating, but inherits R7. The exact-program witness `"éa"` produces `[233,65]` instead of `[201,65]`. |
| R12 `reverse` | Starts accumulator reversal | Sound list definition. |
| R13/R14 `reverseAcc` empty/cons | Finishes or descends on the source list | Sound, disjoint, terminating list equations. |
| R15/R16 `ifPString(true/false,...)` | Selects a branch | Disjoint and exhaustive over `Bool`; sound as a pure selector. |
| R17 `evalBool(any(generator),S) => hasAlpha(S)` | Operational bridge for `any(c.isalpha() for c in s)` | **Unsound.** It inherits the Unicode error and ignores both `_ARGS` and `_IFS`. With the generator filter changed to `Bool(false)` and input `"a"`, Python returns false and the altered program returns `"a"`; K concludes true and returns `"A"`. |
| R18 `evalString(IfExp(...),S)` | Reduces conditional to `ifPString` | Sound only relative to `evalBool`/branch summaries. Both exact branches are pure, so skipped Python evaluation-order effects are not independently material here. |
| R19 `evalString(s.swapcase(...),S) => swapCase(S)` | Operational bridge for `swapcase` | **Unsound.** It inherits the Unicode error and ignores `_ARGS`. On term `s.swapcase(1)` with input `"a"`, K returns `"A"` while Python raises `TypeError`. |
| R20 exact `s[::-1]` term to `reverse(S)` | Operational bridge for the reverse slice | Sound for finite Python strings under the code-point-list embedding. |
| R21 exact module/function/return shell | Entry harness; writes `evalString(E,S)` to result | It pins name, parameter, body, input, and result but omits ordinary Python definition/call/environment machinery. For this pure single-function term it is an explicit low-level harness assumption, not by itself a demonstrated false conclusion. |
| R22 `expected(S)` | Defines the postcondition using the same `hasAlpha`, `swapCase`, and `reverse` symbols as execution | A consistent definition inside K, but not an independent semantic connection. It makes the proof circular with respect to the unproved—and concretely false—Python meanings of R4/R7/R17/R19. |

The guarded `toggle` equations are pairwise disjoint and exhaustive relative to
R4. Recursive constructor equations are disjoint and descending. The
`ifPString` equations are disjoint and exhaustive. The three `evalString`
heads are syntactically disjoint. No priority or simplification interaction
exists. These logical-consistency facts do not repair the false source-language
interpretation.

### False-conclusion and body-sensitivity witnesses

The reviewer created two ground constructor programs and independent Python
analogs:

1. A material `Bool(true) -> Bool(false)` generator-filter change. Python on
   `"a"` returns `"a"`; K returns `"A"`.
2. A `swapcase(1)` call. Python raises `TypeError`; K returns `"A"`.

More strongly, the reviewer changed the generator filter to `Bool(false)` in a
separate claim while retaining the original contract result. That changed the
program term actually executed by the claim. The mutation parsed, and `kprove`
still exited 0 with `#Top`. The source theorem is false at satisfying input
`"a"`. This directly shows that R17 can make a false property provable and that
the proof is insensitive to a material body component.

Evidence:

- `evidence/05_run_static_witnesses.sh`
- `evidence/05_static_witnesses.log`
- `evidence/05_semantics_witnesses.py`
- `evidence/05_witness-filter-false.mpy`
- `evidence/05_witness-swapcase-arg.mpy`
- `evidence/spec-body-mutation.k`

Stage 5 result: FAIL. R4, R7, R17, and R19 (and their dependent summaries) have
explicit false-conclusion witnesses.

## 6. Fresh non-vacuity test

I did not rely on a candidate vacuity artifact; none was submitted. The fresh
reviewer mutation changes the destination from `expected(S)` to unconditional
`reverse(S)`. It is demonstrably false for the satisfying input
`S = 97 :: 98 :: .PString` (`"ab"`): original execution returns
`65 :: 66 :: .PString`, while reversal is `98 :: 97 :: .PString`.

The mutation's `kprove --dry-run` exited 0, so it parses and builds. The actual
mutation proof exited 1 with `WarnStuckClaimState`. Its residual is the expected
unmet equality:

```text
ifPString(hasAlpha(S), swapCase(S), reverseAcc(S,.PString))
#Equals reverseAcc(S,.PString)
```

This is meaningful non-vacuity evidence: the original claim constrains its
result inside the supplied K theory. It does not validate that theory's Python
meaning.

Evidence:

- `evidence/spec-vacuity-audit.k`
- `evidence/06_run_nonvacuity.sh`
- `evidence/06_nonvacuity.log`

Stage 6 result: PASS.

## 7. Proven versus assumed accounting

### What the successful proof actually establishes

Under the candidate's K equations, for every inductive `PString` `S` and every
argument-list instantiation admitted by the claim pattern, executing the
matched constructor term consumes `<k>` and returns:

```text
ifPString(hasAlpha(S), swapCase(S), reverse(S))
```

The exact regenerated submitted term is a ground instance with both argument
lists empty. This is a universal, result-constraining reachability result about
the candidate's ASCII-oriented list model. It is not a partial-correctness
proof of Python `solve` against the trusted HumanEval contract.

### Trust ledger

| Boundary | Status and dependents |
|---|---|
| K v7.1.293 Haskell backend and reachability engine | Ordinary accepted proof-tool boundary; all K proof results depend on it. |
| Imported `BOOL`, `INT`, and `STRING` primitives, including comparison, arithmetic, `lengthString`, `substrString`, and `ordChar` | Ordinary low-level K boundary. R1–R7 depend on it. |
| Trusted `py2mpy.py` | Strongly checked bridge: regeneration is byte-identical. Program pinning depends on it. |
| Python string to `PString` code-point embedding | Informal plus finite concrete evidence; adequate for the shown characters, but no universal machine-checked connection theorem. |
| R21 direct entry harness instead of Python function definition/call machinery | Informal low-level invocation bridge. Exact ground constructor pinning limits its scope, but no independent connection theorem exists. |
| Python `isalpha`, `any`, `swapcase`, and slicing meanings | Result- and control-bearing semantic boundary. Slicing/reversal is credible for the used term; `isalpha`/`any`/`swapcase` are concretely false on in-domain witnesses and therefore illegitimate. |
| `expected` as the HumanEval property | It reuses the same execution summaries, so the bridge is circular. Its claimed Python meaning is concretely false. Every positive claim depends on it. |
| Candidate implementation equivalence to trusted canonical | Falsified by four contextual Greek-sigma witnesses. |

There are no opaque symbols. Differential tests support only tested points;
here they also refute the claimed universal bridges. Neither tests,
`PROOF.md`-style prose, the generation trace, nor the reconstructed `#Top`
substitutes for a sound K-to-Python connection.

### Decision

- Gate A (real-program soundness): FAIL. Used semantic rules have concrete
  false conclusions, and a material false body mutation still proves `#Top`.
- Gate B (intent adequacy): FAIL. The Python implementation diverges from the
  trusted canonical, and the generated semantics materially narrows Python's
  Unicode letter/case domain to ASCII.
- Gate C (trust/evidence auditability): evidence is reproducible, but it
  exposes rather than repairs the failed trust boundaries.

The successful reconstruction and fresh non-vacuity test show that this is not
a missing-proof or vacuity case. It is a proof of the wrong, unsoundly
abstracted model. Under the benchmark's explicit mapping, material narrowing of
the HumanEval source-contract domain is `FAIL / NOT_LEGIT`, not a non-fatal
concern.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
