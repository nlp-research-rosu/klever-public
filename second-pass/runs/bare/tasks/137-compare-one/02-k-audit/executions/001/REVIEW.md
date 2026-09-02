# Independent adversarial audit — 137-compare-one

This review treats every file under `/candidate` as untrusted evidence. All
executions used source copies under `/tmp/audit-work`; no candidate-provided
kompiled definition, cache, bytecode, trace, or claimed `#Top` was reused.
Reviewer-authored tests and bounded logs are preserved under `evidence/`.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`. The required boundary is intact:
`/reference/reference-semantics` is absent both as a path and as a symlink.
There is therefore no infrastructure contradiction and no hidden/supplied
semantics was sought or used. See
[02-integrity.log](evidence/02-integrity.log).

### Required inputs and artifact types

`/reference/canonical.py`, `/reference/prompt.py`, and
`/reference/py2mpy.py` are regular files. The candidate's required generation
records (`run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured JSONL trace) are present and regular.
The candidate source artifacts `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, `prove.sh`, `prompt.py`, and `py2mpy.py` are also
present and regular. No required entry is missing, mistyped, or symlinked.
The complete type inventory is in
[01b-source-inventory.log](evidence/01b-source-inventory.log), and the
generation-record sizes and trace location are in
[03-generation-artifact-inventory.log](evidence/03-generation-artifact-inventory.log).

The candidate prompt and translator are byte-identical to their trusted
mounted versions:

- `prompt.py`: SHA-256
  `0c94cb2d22bf30cfd86a065309a310cb675ef7a5da3dfb3370f5b9e256ed8620`
- `py2mpy.py`: SHA-256
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`

Both `cmp` operations exited 0; see
[02-integrity.log](evidence/02-integrity.log).

The candidate also contains extra generated material:
`definition-kompiled/`, `definition2-kompiled/`, `semantic-kompiled/`,
`verification-kompiled/`, `verification2-kompiled/`,
`verification3-kompiled/`, `__pycache__/`, and `kore-exec.tar.gz`. These are
not integrity failures in generated-semantics mode, but none was trusted or
used.

`run-input.json` identifies the expected bare/generated condition and the
trusted prompt/translator hashes. `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured trace claim a successful generation and
eventual `#Top`; they also record earlier failed builds/proofs. These records
were inspected only as claims. The bounded scan is preserved in
[04-generation-claims.log](evidence/04-generation-claims.log) and
[06-untrusted-generation-scan.log](evidence/06-untrusted-generation-scan.log).

**Stage 1 result:** PASS. There is no infrastructure breach and no required
source/provenance mismatch.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For two inputs that are integers, floats, or strings representing real
numbers, compare their numeric values after accepting either `.` or `,` as the
string decimal separator. Return the original argument having the larger
numeric value, preserving its original type; return `None` when the converted
values compare equal.

The trusted canonical implementation saves the original arguments, normalizes
commas in string operands, converts both comparison operands with CPython
`float`, returns `None` on equality, and otherwise returns the original larger
argument.

### Submitted implementation

`solution.py` performs the same steps, converting each operand once and using
`type(x) == str` rather than the canonical's `isinstance(x, str)`. For the
stated exact input types `int`, `float`, and `str`, this distinction does not
change behavior. String subclasses would differ, but they are outside the
documented domain. The implementation has all three result branches:
equality, first greater, and second greater.

The trusted translator was independently rerun:

```text
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
```

It exited 0, and the regenerated file is byte-identical to the submitted
`solution.mpy` (both SHA-256
`a80ef2540f0cf8425a072718411549680de5efff85de1fd9421b282977a71258`).
See [07-translation-identity.log](evidence/07-translation-identity.log).

### Independent Python differential

[differential_compare.py](evidence/differential_compare.py) independently
loads the trusted canonical and submitted solution entry points. It tests all
four prompt examples; equal, greater, and lesser branches; both string
conversion branches; negatives and signed zero; invalid empty-string
boundaries; the `2**53` rounding boundary; and the full Cartesian product of
28 representative generated values spanning integers, floats, dot/comma
strings, negatives, and large values.

The exact run covered 17 named cases plus 784 generated pairs, 801 total. It
exited 0 with zero canonical-versus-submission mismatches. Both implementations
raised `ValueError` on the two empty-string cases. See
[08-python-differential.log](evidence/08-python-differential.log).

This supports equivalence of the two Python implementations over the tested
scope; it does not validate the K semantics.

**Stage 2 result:** PASS. The generated program matches the trusted
translation and no material Python implementation divergence was found.

## 3. Clean proof reconstruction

Only the candidate source files were copied. Their scratch copies compare
byte-for-byte with the source, and fresh definitions have distinct
`semantic-fresh-kompiled/` and `verification-fresh-kompiled/` names. See
[08b-scratch-isolation.log](evidence/08b-scratch-isolation.log).

The installed independent toolchain was K v7.1.293 and Python 3.10.12
([05-toolchain.log](evidence/05-toolchain.log)).

### Fresh builds

The concrete semantics was compiled from `semantic.k` with the LLVM backend:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition semantic-fresh-kompiled
```

Exit 0: [09-kompile-concrete.log](evidence/09-kompile-concrete.log).

The proof definition was compiled from `verification.k`, which imports
`semantic.k`, with the Haskell backend:

```text
kompile verification.k --backend haskell --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-fresh-kompiled
```

Exit 0: [10-kompile-proof.log](evidence/10-kompile-proof.log).

### Positive claims

The original aggregate target command exited 0 and printed `#Top`
([11-kprove-all-original.log](evidence/11-kprove-all-original.log)).
Because the candidate left its ten claims unlabeled,
[spec-individual.k](evidence/spec-individual.k) reproduces each claim in a
separate spec module. Each module was then proved independently against the
fresh definition:

| Original claim | Independent module | Exit | Output |
|---|---:|---:|---|
| integer equality | `SPEC-01` | 0 | `#Top` |
| integer first greater | `SPEC-02` | 0 | `#Top` |
| integer second greater | `SPEC-03` | 0 | `#Top` |
| rational equality | `SPEC-04` | 0 | `#Top` |
| rational first greater | `SPEC-05` | 0 | `#Top` |
| rational second greater | `SPEC-06` | 0 | `#Top` |
| prompt example 1 | `SPEC-07` | 0 | `#Top` |
| prompt example 2 | `SPEC-08` | 0 | `#Top` |
| prompt example 3 | `SPEC-09` | 0 | `#Top` |
| prompt example 4 | `SPEC-10` | 0 | `#Top` |

The exact ten commands and outputs are in
[12-kprove-individual.log](evidence/12-kprove-individual.log).

### Fresh concrete semantics validation

[concrete_semantics_compare.py](evidence/concrete_semantics_compare.py) ran the
fresh LLVM definition on all prompt examples, concrete witnesses for all ten
claims, negative/comma cases, IEEE-754 boundaries, and empty-string
boundaries. It independently executed both Python implementations for the
same cases.

All prompt and small claim witnesses agreed, but four of sixteen cases did
not:

- Valid integer witness:
  `a = 9007199254740993`, `b = 9007199254740992`.
  Both Python implementations convert both to
  `9007199254740992.0` and return `None`; K retains exact integers and returns
  `pyInt(9007199254740993)`.
- Valid string/integer witness:
  `a = "9007199254740993"`, `b = 9007199254740992`.
  Both Python implementations again return `None`; K parses the string as an
  exact integer-valued rational and returns the original string.
- The two invalid empty-string boundary cases raise `ValueError` in Python but
  K treats the empty decimal as zero and returns `pyNone`. These two are
  outside the documented “strings representing real numbers” domain, but
  expose the absence of exception fidelity.

The first two mismatches are inside the intended integer/string domain and are
material. The complete 16-case result is
[13-concrete-semantics-compare.log](evidence/13-concrete-semantics-compare.log).
A focused valid-domain witness, including Python conversions, complete K final
state, and an independently closing `SPEC-02`, is in
[16-unsound-float-bridge-witness.log](evidence/16-unsound-float-bridge-witness.log).

**Stage 3 result:** FAIL. The K claims reconstruct successfully, but the
required generated-semantics concrete comparison falsifies the bridge to the
real submitted program.

## 4. Adequacy and real-program pinning

### Entry claims in plain language and satisfiable states

Every entry claim starts from `<functions> .Map`, `<env> .Map`,
`<result> pyNone`, and the computation
`theSolution ~> invoke(A, B)`. The following witnesses satisfy every
precondition. Each claimed result agrees with both Python implementations for
the listed small witness, as recorded by the concrete comparison:

| # | Precondition | Required postcondition | Satisfying witness and both-Python result |
|---:|---|---|---|
| 1 | arbitrary K integers `I == J` | result is `pyNone` | `(7, 7)` → `None` |
| 2 | arbitrary K integers `I > J` | result is original `pyInt(I)` | `(8, 7)` → `8` |
| 3 | arbitrary K integers `I < J` | result is original `pyInt(J)` | `(7, 8)` → `8` |
| 4 | positive-denominator rationals with equal cross-products | result is `pyNone` | `(1/2, 2/4)` represented by Python `(0.5, 0.5)` → `None` |
| 5 | positive-denominator rationals with first cross-product greater | result is original first `pyFloat` | `(3/2, 1/1)` represented by `(1.5, 1.0)` → `1.5` |
| 6 | positive-denominator rationals with first cross-product smaller | result is original second `pyFloat` | `(1/2, 1/1)` represented by `(0.5, 1.0)` → `1.0` |
| 7 | fixed `pyInt(1), pyFloat(25,10)` | second input | `(1, 2.5)` → `2.5` |
| 8 | fixed `pyInt(1), pyStr("2,3")` | second input | `(1, "2,3")` → `"2,3"` |
| 9 | fixed `pyStr("5,1"), pyStr("6")` | second input | `("5,1", "6")` → `"6"` |
| 10 | fixed `pyStr("1"), pyInt(1)` | `pyNone` | `("1", 1)` → `None` |

These witnesses show that no entry precondition is contradictory. The result
cell is constrained to a concrete expression in every claim, `<k>` must reach
`.K`, and the false-postcondition test in Stage 6 confirms that the result is
not free or tautological. Final function and environment maps are existential,
but they are internal bookkeeping and do not weaken the returned-result
constraint.

### Program identity and control-flow pinning

The proof macro contains the complete constructor tree from `solution.mpy`.
Both were independently parsed and macro-expanded with the fresh Haskell
definition. Their KORE files are byte-identical, with SHA-256
`52b1251d9eb9db9bf01c32c8317237575477137f0d3f4ae4289a75401a73887b`;
see [14-program-macro-identity.log](evidence/14-program-macro-identity.log).

Execution is not replaced by a summary: `Module` installs the actual
`compare_one` body, `invoke` selects that installed body, and the real
assignments, conditions, and returns execute. There are no helper or loop
claims.

Thus the proof is syntactically pinned to the submitted program. Its failure is
semantic, not program substitution.

### Adequacy gaps

The universal integer claim is false about the pinned Python program. Claim 2
accepts the satisfying state
`I=9007199254740993, J=9007199254740992`; K proves and returns `I`, while the
real program returns `None`. The symmetric ordering claim has the same issue
when the adjacent large values are reversed.

The six symbolic claims cover only homogeneous integer or candidate-defined
rational inputs. There is no universal claim for:

- any string/string pair;
- general integer/string, float/string, or integer/float pairs;
- comma/dot normalization beyond three fixed string examples; or
- CPython conversion errors and IEEE-754 edge behavior.

The four examples cannot substitute for those missing universal obligations.
Even absent the concrete false theorem, this is a material scope gap relative
to the stated `int | float | str` input domain.

**Stage 4 result:** FAIL. The exact program is pinned and the claims are
result-constraining, but a universal entry claim is false about that program
and the declared contract is only partially covered.

## 5. Rule-by-rule static soundness review

The numbered source and machine-generated declaration scan are preserved in
[15-static-source-inventory.log](evidence/15-static-source-inventory.log).
There are no generated helper K files beyond `semantic.k` and
`verification.k`.

### Local syntax, attributes, and configuration inventory

Every local production is listed here:

| ID | File/line | Declaration |
|---|---|---|
| S1 | `semantic.k:8` | token `FloatLiteral` for signed digit-dot-digit literals |
| S2 | `:10` | `Pgm ::= Module(Stmts)` |
| S3 | `:12` | juxtaposed `Stmts` list |
| S4 | `:13` | comma-separated `Names` list |
| S5 | `:14` | `Params(Names)` |
| S6 | `:15` | comma-separated `Exprs` list |
| S7 | `:16` | comma-separated `CmpOps` list |
| S8–S11 | `:18–21` | `Stmt` constructors `FuncDef`, `Assign`, `If`, `Return` |
| S12–S19 | `:23–30` | `Expr` constructors `Name`, `Int`, `Float`, `Str`, `NoneVal`, `Call`, `Attribute`, `Compare` |
| S20 | `:32` | `CmpOp(String, Expr)` |
| S21–S26 | `:34–39` | `PyVal` constructors `pyInt`, `pyFloat`, `pyStr`, `pyBool`, `pyType`, `pyNone` |
| S27 | `:58` | stored `function(Params, Stmts)` |
| S28–S29 | `:59–60` | computation items `execute(Stmts)` and `invoke(PyVal, PyVal)` |
| S30 | `:87` | `eval(Expr, Map) [function]` |
| S31 | `:88` | `typeOf(PyVal) [function, total]` |
| S32 | `:89` | `pyFloatOf(PyVal) [function]` |
| S33 | `:90` | `pyReplace(PyVal, PyVal, PyVal) [function]` |
| S34 | `:91` | `pyCompare(String, PyVal, PyVal) [function]` |
| S35 | `:127` | `parseDecimal(String) [function]` |
| S36 | `:128` | `parseUnsignedDecimal(String, Int) [function]` |
| S37 | `:129` | `decimalDigits(String) [function]` |
| S38 | `verification.k:8` | `theSolution [macro]` |

The configuration has exactly four state components: `<k>`,
`<functions>`, `<env>`, and `<result>`. There are no heap, allocation, I/O,
exception, or call-stack cells. For this loop-free body over immutable
primitive inputs, no heap/allocation cell is needed, but the lack of exception
and IEEE-float state is material.

There is one `total` declaration (`typeOf`), whose six equations cover all six
`PyVal` constructors with disjoint patterns. There are no `[functional]`,
`[simplification]`, `[priority]`, `[opaque]`, `[anywhere]`, or `[owise]`
declarations or rules. The other functions are intentionally partial.

### Mapping of the submitted program's constructs

`solution.mpy` uses `Module`, `FuncDef`, `Params`, statement sequencing,
`If`, `Assign`, `Return`, `Compare`, one `CmpOp`, `Call`, `Name`,
`Attribute`, `Str`, and `NoneVal`. Each has syntax above and an applicable
execution/evaluation rule below. Empty else branches use `.Stmts`.
`Int(...)` and `Float(...)` expression literals are declared, but are not used
in the submitted body; in particular, the absent `eval(Float(...))` rule is
not a used-construct defect in generated-semantics mode. General comparison
chains, arbitrary attributes, and arbitrary calls are likewise outside the
submitted construct set and visibly remain unmodeled.

### Exhaustive rule inventory and decision

| Rule | File/line and effect | Class and assessment |
|---:|---|---|
| R1 | `semantic.k:62`, `Module(SS) => execute(SS)` | Operational sequencing; faithful for the submitted module. |
| R2 | `:63`, empty `execute` terminates | Operational base case; sound. |
| R3 | `:64`, execute head statement then tail | Operational sequencing; preserves source order. |
| R4 | `:66–67`, install `FuncDef` in `<functions>` | State rule; binds the exact body and parameters. Sound for the module. |
| R5 | `:69–71`, invoke installed `compare_one`, reset environment to two parameters | Dedicated top-level call rule. It reads the installed body and binds both actual arguments. It is not a summary. Sound for this single-function harness; it does not model general Python calls. |
| R6 | `:73–74`, evaluate and assign a named target | State rule. Atomic evaluation is adequate for the pure primitive expressions used here. |
| R7 | `:76–78`, true `If` branch | Operational guard; disjoint from R8. |
| R8 | `:79–81`, false `If` branch | Operational guard; disjoint from R7. |
| R9 | `:83–85`, evaluate return, write `<result>`, discard suffix | Control rule. It implements function return for the top-level invocation. It would be too broad for a language with nested call frames, but no such frame exists in this submitted semantics/program. |
| R10 | `:93`, environment name lookup | Definitional evaluation; sound when the key is bound. |
| R11 | `:94`, `Name("str") => pyType("str")` | Built-in-name rule used by the program. It overlaps R10 if an environment binds `"str"`; that would make broader-language lookup nonconfluent, but the submitted function never binds that name. This is a reuse limitation, not the intended-domain verdict witness. |
| R12 | `:95`, integer literal to `pyInt` | Definitional and mathematically sound; unused by this body. |
| R13 | `:96`, string literal to `pyStr` | Definitional; sound. |
| R14 | `:97`, `NoneVal => pyNone` | Definitional; sound. |
| R15 | `:99`, evaluate `type(...)` through `typeOf` | Built-in bridge; sound for the six modeled primitive constructors. |
| R16 | `:100`, evaluate `float(...)` through `pyFloatOf` | Built-in bridge whose value is result-bearing. Its concrete equations R25–R27 are not a faithful CPython-float connection. |
| R17 | `:101–102`, evaluate `.replace(...)` through `pyReplace` | Built-in bridge. On the used string receiver and literal comma/dot arguments, K `replaceAll` has the required pure all-occurrences behavior. |
| R18 | `:103–104`, evaluate one comparison through `pyCompare` | Built-in bridge; applicable to every comparison in the body. Its numeric meaning inherits the invalid exact-rational abstraction. |
| R19 | `:106`, `typeOf(pyInt) => int` | Total-function case; sound. |
| R20 | `:107`, `typeOf(pyFloat) => float` | Total-function case; internally consistent with the candidate representation. |
| R21 | `:108`, `typeOf(pyStr) => str` | Total-function case; sound. |
| R22 | `:109`, `typeOf(pyBool) => bool` | Total-function case; sound and unused. |
| R23 | `:110`, `typeOf(pyNone) => NoneType` | Total-function case; sound and unused for input. |
| R24 | `:111`, `typeOf(pyType) => type` | Total-function case; sound. |
| R25 | `:113`, `pyFloatOf(pyInt(I)) => pyFloat(I,1)` | **Materially unsound CPython bridge.** It asserts exact integer preservation for every K integer, whereas CPython `float` rounds large integers. The valid witness below makes a false return theorem provable. |
| R26 | `:114`, `pyFloatOf(pyFloat(N,D))` is identity | Exact-rational input assumption. It is internally sound only if `pyFloat(N,D)` already denotes the exact value of an actual Python float. The spec quantifies over arbitrary positive denominators, including values with no exact binary-float representation, and supplies no representation theorem. |
| R27 | `:115`, string float conversion delegates to exact decimal parsing | **Materially unsound CPython bridge.** CPython rounds decimal strings to binary float. The valid large-decimal witness below makes K select a different branch/result. |
| R28 | `:117–118`, `pyReplace` uses `replaceAll` | Trusted low-level string primitive. Sound for the used comma-to-dot replacement. |
| R29 | `:120–121`, equality of modeled type objects | Mathematical equality on type tags; sound for `type(x) == str`. |
| R30 | `:122–123`, rational equality by cross-product | Ordinary mathematics for positive-denominator exact rationals. It is sound inside that abstraction but exposes the wrong R25/R27 values to control flow. |
| R31 | `:124–125`, rational greater-than by cross-product | Ordinary mathematics for positive-denominator exact rationals. Same invalid Python bridge dependency as R30. |
| R32 | `:131–134`, strip a leading minus and parse with sign `-1` | Disjoint guarded decimal-parser case; sound for the supported simple decimal grammar. |
| R33 | `:135–137`, nonnegative/empty parse with sign `1` | Disjoint from R32. Its empty-string branch contributes to a false Python behavior outside the valid string-number domain. |
| R34 | `:139–141`, no-dot decimal as denominator 1 | Exact decimal arithmetic; sound for digit strings. |
| R35 | `:142–149`, dotted decimal to a power-of-ten denominator | Exact decimal arithmetic for a single well-formed dot and digit substrings. It is not CPython rounding semantics. |
| R36 | `:151`, empty digit sequence is zero | Makes `float("")` behave like zero through R33/R34, while Python raises `ValueError`. The concrete witness is outside the stated valid-string domain but records the narrower exception gap. |
| R37 | `:152`, nonempty digits via trusted `String2Int` | Low-level primitive for digit-only substrings. Exponent, whitespace, multiple-dot, and other Python-accepted/rejected forms are not modeled or proved. |
| R38 | `verification.k:9–32`, expand `theSolution` to the constructor program | Compile-time definitional macro, not an execution shortcut. Fresh expanded-KORE byte identity establishes exact syntactic correspondence. |

### Guards, overlaps, control, and state

R7/R8 are disjoint boolean cases. R32/R33 are disjoint on leading minus and
cover empty/nonempty prefixes. R34/R35 are disjoint on the first dot search;
R36/R37 are disjoint on empty/nonempty strings. `typeOf` is genuinely total
over `PyVal`. There are no rule priorities or simplifications that silently
preempt execution.

R10/R11 have the one broader-language overlap described in the table. The
actual environment contains only `a`, `b`, `a_value`, and `b_value`, so no
false intended-domain conclusion is attributed to that overlap.

Statement order is explicit through `~>`. Module installation occurs before
`invoke`; arguments are put in `<env>` before the body; assignments update
that map; conditions read the updated map; and return writes `<result>` and
terminates the top-level computation. There is no allocation or mutation of
input values. The `float`, `replace`, and comparison helpers are pure, so
atomic recursive `eval` does not reverse an observable side effect for this
program.

### Required false-conclusion witnesses

**Integer conversion rule R25 (with comparison R30/R31):**

```text
I = 9007199254740993
J = 9007199254740992
I > J
```

R25 creates exact `pyFloat(I,1)` and `pyFloat(J,1)`. R30 says they are unequal;
R31 says the first is greater; K returns `pyInt(I)`, and the universal
greater-integer claim closes with `#Top`. CPython instead has
`float(I) == float(J) == 9007199254740992.0`, so both the submitted and
canonical programs return `None`. This is a concrete false conclusion on the
intended input domain, not an untested theoretical concern. See
[16-unsound-float-bridge-witness.log](evidence/16-unsound-float-bridge-witness.log).

**String conversion rule R27:**

```text
a = "9007199254740993"
b = 9007199254740992
```

The string is a valid real-number representation. K parses it exactly and
returns the original string; both Python implementations round both converted
values to the same float and return `None`. See the
`ieee-string-rounding` case in
[13-concrete-semantics-compare.log](evidence/13-concrete-semantics-compare.log).

No rule encodes the desired larger-input answer directly, and there is no
unconstrained oracle. The failure is nevertheless decisive: the generated
semantics replaces the result-bearing CPython `float` operation with a
different exact-rational operation, and that difference reaches the formal
postcondition.

**Stage 5 result:** FAIL. The real body executes, but R25 and R27 are
materially unsound result-bearing bridges for valid submitted-program inputs.

## 6. Fresh non-vacuity test

No candidate vacuity artifact was trusted. A fresh
[spec-vacuity-audit.k](evidence/spec-vacuity-audit.k) changes claim 2's result
from `pyInt(I)` to the deliberately false `pyInt(I +Int 1)` while retaining
the satisfiable precondition `I >Int J`.

The witness `I=2, J=1` satisfies the precondition; both Python
implementations return `2`, not `3`. A `kprove --dry-run` against the fresh
definition exited 0, proving that the mutation parses and builds rather than
failing for an unrelated reason. See
[17-vacuity-build.log](evidence/17-vacuity-build.log).

The actual mutated proof exited 1 with `WarnStuckClaimState`. Its residual
contains the expected unmet implication `I #Equals I +Int 1`, and the final
modeled result is `pyInt(I)`. See
[18-vacuity-proof-failure.log](evidence/18-vacuity-proof-failure.log).

**Stage 6 result:** PASS. The K theorem is non-vacuous and
result-discriminating inside the candidate theory. This does not cure the
theory's false Python bridge.

## 7. Proven versus assumed accounting

### What the successful reachability proof actually establishes

Under the candidate-defined K language—not under CPython—it establishes that
the exact submitted constructor program:

1. returns `pyNone`, the first `pyInt`, or the second `pyInt` according to
   exact mathematical ordering of arbitrary K integers after the candidate's
   exact conversion;
2. returns according to exact cross-product ordering of arbitrary
   positive-denominator `pyFloat(N,D)` rationals; and
3. produces the stated result for the four fixed prompt examples.

The proof also establishes K termination to `.K` for those claims. It does not
establish universal behavior for strings or mixed types.

### Trust ledger

| Boundary | Dependents | Accounting |
|---|---|---|
| Trusted `py2mpy.py` transliteration | Program identity | Accepted as a problem-provided primitive; independent byte regeneration succeeded. |
| `theSolution` macro | All claims | Acceptable compile-time alias; fresh expanded KORE is byte-identical to `solution.mpy`. |
| K integer, boolean, string, map, equality, substring, length, search, exponentiation, and map-update primitives | All semantic execution | Ordinary low-level K trust boundary. No candidate rule changes their mathematics. |
| K `replaceAll` for comma-to-dot replacement | String examples | Acceptable low-level primitive for the used literal strings; finite concrete checks agree. |
| `String2Int` plus the candidate decimal parser | String conversion | Supports only the defined exact-decimal subset. It is not a theorem about CPython `float`. |
| Exact-rational `pyFloatOf` and cross-product comparison | Every symbolic numeric claim and all numeric control flow | **Illegitimate bridge to the real program.** It is program-result-bearing, has no bridge-free universal connection theorem, and has concrete opposite-result witnesses. |
| Canonical-to-submission implementation correspondence | Natural-language/implementation bridge | Source inspection plus 801 finite differential cases, zero mismatches. This supports but does not universally prove equivalence. |
| CPython IEEE-754 conversion, rounding, overflow, accepted numeric-string grammar, and exceptions | Real execution behavior | Not modeled. Rounding is not merely omitted: candidate rules contradict it on valid witnesses. |

There are no opaque symbols, fresh result oracles, proof-local helper
functions, simplification lemmas, priority rules, or auxiliary loop claims.
The candidate-provided compiled definitions, generation traces, and prose are
outside the trust boundary.

### Decision

The reconstruction proves a non-vacuous theorem about an exact-rational
mini-language and syntactically pins the submitted constructor program.
It is not a legitimate partial-correctness proof of the real generated Python
program. The formal integer-greater claim proves a result that is concretely
false for a satisfying, intended-domain input because the generated semantics
does not implement CPython `float`. General string and mixed-type obligations
are also absent. These are material soundness and adequacy failures, not thin
testing concerns or infrastructure uncertainty.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
