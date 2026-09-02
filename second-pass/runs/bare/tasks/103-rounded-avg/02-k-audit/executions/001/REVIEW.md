# Independent adversarial audit: 103-rounded-avg

## Outcome

The candidate reconstructs cleanly and its claims are non-vacuous, but it does
not prove partial correctness of the real generated Python program over the
stated positive-integer domain. Its reached division rule models Python `/` as
an exact rational. CPython actually converts the quotient to binary64 (or
raises on overflow), and the difference changes the returned value on a
satisfying input. The successful K proof therefore establishes a theorem about
an idealized arithmetic interpreter, not the submitted program.

The decisive false-conclusion witness is
`N=M=9007199254740993 = 2^53+1`. It satisfies the
`integral-midpoint` precondition. K proves/executes
`result(binVal(9007199254740993))`; both `/candidate/solution.py` and the
trusted canonical implementation return the binary string for
`9007199254740992`. A second witness, `N=M=10**400`, makes both Python
implementations raise `OverflowError` while K fabricates a normal
`binVal(10**400)` result. These results are preserved in
[the concrete comparison log](evidence/logs/06-concrete-semantics-compare.log).

The audit used the mandated `using-kit`, `writing-semantics`, and
`validating-proof` procedures. In Kit terms, program identity and non-vacuity
pass, but Gate A (real-program semantics) fails.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree: this is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` does not exist. There is no infrastructure
breach.

All required candidate and trusted inputs are regular files, not symlinks or
mistyped entries. The candidate prompt is byte-identical to
`/reference/prompt.py` (SHA-256
`60808c911a60e25f559e0f929c49206062eb742f0e32ab431f5ba9daf280a694`);
the candidate translator is byte-identical to `/reference/py2mpy.py`
(`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`).
[The complete type/hash inventory](evidence/logs/01-stage1-inventory.log)
exited 0.

`run-input.json` claims problem `103-rounded-avg`, condition `bare`, no supplied
semantics, and the same prompt/translator hashes. `metrics.json` claims a
successful 411-second generation. `codex-last.txt`, `codex-output.log`, and the
structured trace claim that one aggregate `kprove` run printed `#Top`.
Those records were treated only as untrusted claims. The readable trace has 106
records; 30 reasoning records are encrypted, while tool calls, tool outputs,
patches, and messages are readable. The bounded extraction is
[here](evidence/logs/02-untrusted-trace-summary.log).

Candidate extras are two compiled-definition trees and `__pycache__` files.
They are ordinary files, but were ignored rather than trusted. There are no
candidate helper `.k` sources beyond `semantic.k`, `verification.k`, and
`spec.k`. `PROOF.md` and a candidate vacuity spec are absent, but neither was a
required bare-generation deliverable. No required source artifact is missing,
changed relative to a trusted counterpart, mistyped, or symlinked.

All execution used `/tmp/audit-work/103-rounded-avg`, populated only with
source copies. Nothing under `/candidate/*-kompiled` was reused.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For positive integers `n` and `m`, return `-1` if `n>m`. Otherwise compute the
average of every integer in the inclusive interval `[n,m]`, round to the
nearest integer using the Python behavior implemented by the trusted canonical
function (ties to even), and return that integer’s `bin(...)` string.

The generated implementation is:

```python
def rounded_avg(n, m):
    if n > m:
        return -1
    return bin(round((n + m) / 2))
```

For a nonempty consecutive integer interval, the exact mathematical average is
`(n+m)/2`, so this is a legitimate alternative algorithm. It preserves the
required signature and branch. Its use of Python `/`, however, is an actual
binary64 operation; that fact matters later when auditing the K semantics.

The trusted translator regenerated `solution.mpy` byte-for-byte:
both files have SHA-256
`9822e532b080a85f474e143358b95a1698466e969412d6aa5d951f35aaa544df`.
The exact command and `cmp` exit 0 are in
[the translation log](evidence/logs/03-translation-and-differential.log).

The independent differential script imports `/reference/canonical.py` and the
scratch copy of the generated entry point using separate module loaders. It
ran 2,711 cases:

- all four documented examples;
- 12 equality, reversed-interval, branch, and ties-to-even boundaries;
- five outside-domain robustness cases, kept separate from the verdict;
- 90 short-interval cases around `2^52`, `2^53`, `2^54`, `2^1022`,
  `2^1023`, and `10^400`;
- all 1,600 positive pairs in `[1,40]^2`;
- 1,000 seeded positive random pairs in `[1,10^6]^2`.

There were zero candidate-versus-canonical mismatches and zero example
failures. Exact generated inputs are preserved in
[differential-inputs.json](evidence/differential-inputs.json), with the command,
scope, seed, input hash, exit 0, and results in
[the same stage-2 log](evidence/logs/03-translation-and-differential.log).
This is finite implementation-fidelity evidence, not a proof.

An initial reviewer logging wrapper accidentally redirected its own status text
into the regenerated `.mpy`; that non-candidate mismatch is transparently
preserved in `evidence/logs/03a-reviewer-logging-error.log` and was superseded
by the clean byte-identity run above.

## 3. Clean proof reconstruction

K 7.1.293 was available independently. From the source-only scratch copy I
built:

- an LLVM concrete definition from `semantic.k` with main module `SEMANTIC`
  and syntax module `MPY-SYNTAX`; exit 0
  ([log](evidence/logs/04-build-concrete-llvm.log));
- a Haskell proof definition from `verification.k` with main module
  `VERIFICATION` and syntax module `MPY-SYNTAX`; exit 0
  ([log](evidence/logs/05-build-proof-haskell.log)).

Every positive claim was then selected independently with:

```text
kprove spec.k \
  --definition /tmp/audit-work/103-rounded-avg/verification-audit-kompiled \
  --spec-module SPEC --claims SPEC.<label> --output pretty
```

All eleven exited 0 and printed an exact `#Top`: `reversed`,
`integral-midpoint`, `half-even-down`, `half-even-up`, the four program
examples, and `render-3`, `render-15`, `render-26`. Per-claim command logs are
`evidence/logs/07-proof-<label>.log`. An aggregate rerun also exited 0 with
`#Top` ([log](evidence/logs/08-proof-all-claims.log)). The rendering claims
emit `WarnTrivialClaim` because their ground function terms are normalized
during claim preparation; their independent selection still closes.

Fresh `krun` agrees with both Python implementations on ordinary, reversed,
singleton, equality, adjacent-reversal, and both half-even boundary cases. The
same executable comparison then finds the two intended-domain numeric
mismatches stated in the outcome. Its exit 1 means “mismatches found,” not a K
tool or parser failure.

A first version of the reviewer result parser failed to recognize whitespace
in otherwise successful K configurations; it is preserved as
`06a-reviewer-result-parser-error.log`. The corrected comparison is the cited
`06` log. `06b-pre-overflow-case.log` preserves the corrected run before the
overflow witness was added.

Thus the mechanical reconstruction gate has a split result: all positive
claims close under the supplied theory, but the freshly rebuilt generated
semantics does not execute the real program faithfully.

## 4. Adequacy and real-program pinning

### Plain-language claims

All program claims start from `<k> boot(roundedAvgProgram,N,M) </k>`,
`<env> .Map </env>`, and `<result> noResult </result>`, and require termination
at `.K` with exact final bindings for `"n"` and `"m"`.

- `reversed`: for positive `N,M` with `N>M`, return integer `-1`.
- `integral-midpoint`: for positive `N<=M` and even `N+M`, return
  `binVal((N+M)/2)`.
- `half-even-down`: for positive `N<=M`, odd `N+M`, and even floor midpoint,
  return the floor midpoint as `binVal`.
- `half-even-up`: for positive `N<=M`, odd `N+M`, and odd floor midpoint,
  return floor-plus-one as `binVal`.
- The next four claims fix the prompt inputs and results `(1,5)->3`,
  `(7,5)->-1`, `(10,20)->15`, and `(20,33)->26`.
- The last three claims rewrite the observer at `binVal(3)`, `binVal(15)`,
  and `binVal(26)` to the prompt’s concrete strings, leaving the empty
  environment and `noResult` unchanged.

The specifications do not read `solution.mpy` directly; they call the
nullary function `roundedAvgProgram`. I extracted that function’s constructor
RHS and parsed it, after replacing K’s internal empty-list unit `.Stmts` with
the equivalent empty surface sequence. `kast` produced byte-identical KORE for
that RHS and the submitted `solution.mpy`, hash
`663f7655ca10dd6bdb07199e0cc88c095e47f49fdf5114768228ce5ccfd27b4d`;
`cmp` exited 0. See
[the pinning log](evidence/logs/09-program-pinning.log) and the preserved KORE
files under `evidence/artifacts/`. The failed attempt to pass `.Stmts` through
the external program scanner is preserved as
`09a-reviewer-internal-list-unit-parser-error.log`; it is not a candidate
failure.

`roundedAvgProgram` is therefore the real translated program, not a substituted
answer. There are no loop or helper claims. The operational rules execute both
real branches and the actual nested `bin(round((n+m)/2))` expression. Each
destination fixes the return constructor and payload; no result variable is
free, and no postcondition is a tautology or one-way implication.

Every precondition is satisfiable. Ground witnesses are:
`(7,5)` for `reversed`, `(1,5)` for `integral-midpoint`, `(2,3)` for
`half-even-down`, `(1,2)` for `half-even-up`, the four example states
themselves, and `3`, `15`, `26` for the rendering states. Both Python
implementations agree with those claimed results. Exact state records and
comparisons are in
[the witness log](evidence/logs/10-claim-witnesses.log).

That same log substitutes the satisfying integral witness
`N=M=9007199254740993` and disproves real-program adequacy:

```text
claimed K payload:        9007199254740993
generated Python payload: 9007199254740992
canonical Python payload: 9007199254740992
```

The formal claim is strongly result-constraining, but it constrains the wrong
result because of the language model.

## 5. Rule-by-rule static soundness review

The exhaustive inventory is
[rule-inventory.md](evidence/rule-inventory.md); the independent declaration
scan is [here](evidence/logs/13-static-declaration-scan.log).
There are no candidate-generated helper K files.

### Inventory summary

`semantic.k` contains:

- syntax declarations S1–S12 for `Module`, statement/parameter/string lists,
  the three statement forms, six expression forms, comparison lists, four
  runtime value constructors, two result constructors, and five control
  constructors;
- six `[function]` symbols: `eval`, `unary`, `binary`, `compare`,
  `callBuiltin`, and `roundValue`;
- the `<py>` configuration with only `<k>`, `<env>`, and `<result>`;
- exactly 24 local rules R1–R24.

`verification.k` contains three `[function]` symbols and five equations:
`roundedAvgProgram` (VF1), `renderBinary` (VF2), and the three
`unsignedBits` cases (VF3–VF5).

Neither file contains `[total]`, `[functional]`, `[opaque]`, priority,
`[simplification]`, `strict`, or `seqstrict` declarations. There are no local
lemmas, proof-only operational bridges, circularities, or loop summaries.
`spec.k` contains only its eleven claims.

### Construct and control coverage

Every constructor in `solution.mpy` is declared and reached:
`Module/FuncDef/Params/Stmts` use S1–S5 and R1–R3;
`If/Compare/Name/CmpOp` use S3, S6, S8–S9 and R4–R6, R10, R13, R18;
`Return/UnaryOp/Int` use S3, S6 and R7–R9, R11, R15; and the nested
`Call/Name/BinOp/Int` terms use S6–S7 and R9–R10, R12, R14, R16–R17,
R19–R24. Missing semantics for an unused Python construct is not alleged.

Boot binds exactly two actual formal names. Statement-list rules are disjoint
at empty versus nonempty lists. The condition is evaluated before branch
selection; true/false selection rules are disjoint. Return evaluates its
expression, writes the sole result cell, and discards the remaining function
continuation, matching both real return paths. Name lookup is limited to a
present map binding. The semantics has no heap, allocation, I/O, exceptions,
or call stack because ordinary executions of this exact top-level pure
function need none. Argument/subexpression order is not explicit, but every
used subexpression and builtin is pure, so no submitted execution can observe
an order difference.

The four exact-rational rounding guards are disjoint: below half, above half,
and equality partitioned by floor parity. For positive numerator and
denominator 2 they cover every reached exact `ratVal`. `unsignedBits` has
disjoint cases `0`, `1`, and `I>=2`; the recursive argument decreases and
`Int2String(I%2)` is `"0"` or `"1"`.

### Materially unsound rule cluster

R17 is:

```text
binary("/", intVal(I), intVal(J)) => ratVal(I,J)  requires J != 0
```

R19 and R21–R24 then round that exact rational. The equations R21–R24 are
ordinary correct mathematics *for the invented exact `ratVal`*, but R17 is
false as a semantic conclusion about the Python `/` expression actually
executed. Python first creates a binary64 result; `round` receives that float.
The false-conclusion witness is within every stated input restriction:

```text
N = M = 9007199254740993
I = N+M = 18014398509481986, J = 2
K exact quotient/round:      9007199254740993
CPython quotient/round:      9007199254740992
```

This cluster enables the proved `integral-midpoint` destination
`binVal(9007199254740993)`, which the real terminating program falsifies. The
overflow witness additionally demonstrates omitted exception behavior.
Priority or reachability cannot cure this: R17 is the only reached division
rule, and both witnesses satisfy the entry claim.

R20 maps external Python `bin` to the abstract constructor `binVal(I)`.
VF2–VF5 define a correct nonnegative string observer, and all ordinary tested
cases agree with Python `bin`. This is an understandable low-level
representation boundary rather than a task-answer shortcut. It is nevertheless
result-bearing: the program claims stop at `binVal`, and only three ground
rendering claims connect that representation to literal strings. Without the
numeric defect this would be a documented intent/representation limitation,
not an independently witnessed false rule on the intended successful-result
domain.

VF1 is a definitional program constant whose exact AST identity was checked;
it does not summarize or skip the body. No rule encodes the rounded-average
answer directly, introduces an oracle, or bypasses the submitted control flow.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact. In scratch I created
[spec-vacuity-audit.k](evidence/artifacts/spec-vacuity-audit.k), containing the
realized initial input `(1,5)` but mutating the required result from
`binVal(3)` to `binVal(4)`.

The separate dry run compiled the mutation successfully and exited 0
([log](evidence/logs/11-vacuity-dry-run.log)). The proof command then exited 1
with `WarnStuckClaimState`; its terminal configuration contains
`result(binVal(3))`, while the preserved mutation requires `binVal(4)`.
[The expected-failure log](evidence/logs/12-vacuity-expected-failure.log)
records the exact command, statuses, residual, and checks.

An initial reviewer check expected the backend residual to print both the
reached and destination values. This backend prints the reached state and the
mutation source location, so that overly strict harness result is preserved as
`12a-reviewer-residual-format-assumption.log` and superseded by the correct
artifact-plus-residual check.

Non-vacuity passes: the theory discriminates a false result. That does not
validate the theory’s model of Python arithmetic.

## 7. Proven versus assumed accounting

### What `#Top` actually establishes

Under the candidate’s K theory and K’s standard libraries, the exact
constructor program deterministically:

- returns `intVal(-1)` on positive reversed bounds;
- otherwise adds unbounded integers, stores the division operands as an exact
  rational, applies exact ties-to-even rounding, and returns that integer in
  `binVal`;
- produces the four claimed prompt-example payloads; and
- renders the three fixed `binVal` examples to their literal strings.

The four universal claim guards collectively cover all positive K integers.
The proof does not establish that `ratVal` has CPython float semantics, that
exceptions are preserved, or that the abstract `binVal` postcondition is a
literal Python string for all inputs.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K compiler, LLVM/Haskell backends, reachability engine, and standard `INT`, `BOOL`, `STRING`, `MAP` modules | Every execution and claim | Ordinary unavoidable tool/primitive trust boundary. Fresh independent builds reduce cache/provenance risk. |
| K integer arithmetic, map lookup/update, string concatenation, `Int2String` | R1, R10, R15–R18, R21–R24, VF2–VF5 | Acceptable low-level primitives for their declared K meanings. |
| Trusted `py2mpy.py` transliteration | Program identity | Trusted mounted input; byte identity and regenerated `.mpy` were checked. |
| `roundedAvgProgram` equation | Every program claim | Acceptable definitional constant; parsed KORE identity proves it pins the submitted artifact. |
| Automatic `boot` harness for one two-argument top-level function | Every program claim | Acceptable minimal execution harness for this exact module and signature. It is not a general Python module semantics. |
| Exact `ratVal` interpretation of Python `/` and exact `roundValue` composition | All valid-interval universal claims and three valid examples | **Illegitimate.** It affects the final value and exception behavior; the two preserved intended-domain witnesses refute it. |
| `binVal(I)` as Python `bin(I)` representation, plus VF2–VF5 | Every successful postcondition and rendering claim | Concerning but not shown false for intended nonnegative results. Equations and finite checks support it; the program theorem remains phrased in the abstraction. |
| Mathematical identity “average of `[n,m]` is `(n+m)/2`” | Implementation-to-contract bridge | Correct ordinary mathematics for nonempty integer intervals, but does not erase CPython binary64 behavior. |
| 2,711-case canonical differential | Generated implementation versus canonical | Finite empirical support only. It cannot validate the K arithmetic model; indeed both Python sides jointly disagree with K at the precision witness. |

There are no local opaque symbols, fresh uninterpreted result oracles,
proof-local simplification lemmas, or operational bridges that skip a
program-defined body.

### Kit gates and decision

- Gate A, real-program soundness: **FAIL**. A1 program identity passes,
  control/state fidelity passes on the submitted paths, and A5 non-vacuity
  passes; numeric semantic fidelity fails with a concrete false returned value.
- Gate B, intent adequacy: **FAIL**. The positive-integer precondition matches
  the prompt, but the generated language model does not match Python’s numeric
  representation or overflow behavior. The `binVal`-to-string bridge is also
  only partially formalized.
- Gate C, auditability: **PASS for this review’s evidence**. Commands, inputs,
  statuses, and bounded outputs are preserved. Finite tests are not credited
  as universal proof.

Because a reached semantics rule makes a false result claim provable for a
satisfying intended-domain input, this meets the requested
`FAIL / NOT_LEGIT` boundary despite clean `#Top` reconstruction and a successful
non-vacuity mutation.

VERDICT: FAIL
LEGITIMACY: NOT_LEGIT
