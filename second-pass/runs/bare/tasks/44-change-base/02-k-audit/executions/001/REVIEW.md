# Independent adversarial audit: 44-change-base

## Executive decision

The candidate contains a fresh-reconstructible, non-vacuous reachability proof
of the exact submitted `solution.mpy` under its generated, idealized MiniPython
semantics. The proof does not replace execution with an oracle, and its sole
positive claim independently closes with `#Top`.

The result is not a clean pass. The formal theorem and candidate program return
`"0"` for `x = 0`, while the trusted canonical implementation returns `""`;
zero is admitted by the formal precondition and not excluded by the prompt.
Also, the semantics models an unbounded call stack: at `x = 2**1100, base = 2`
it returns normally, while default CPython execution of `solution.py` raises
`RecursionError`. These are intent/runtime-model limitations rather than a
vacuous proof, substituted program, result oracle, or false proof-local lemma.
Accordingly, the proof is legitimate but qualified.

All candidate prose, compiled definitions, logs, and traces were treated only
as untrusted claims. All executable artifacts were copied into
`/tmp/audit-work/44-change-base.Cjtazd/candidate-src`; candidate-provided
compiled definitions and bytecode were not copied or used. Reviewer evidence is
under `/audit-output/evidence/`.

## 1. Input and provenance integrity

### Rendered semantics boundary

The mode is `GENERATED_SEMANTICS`. `/reference/reference-semantics` does not
exist, so the trusted mounts do not contradict the rendered mode. No hidden or
inferred reference semantics was sought or used. See
`evidence/00-boundary-and-inventory.log` (exit 0).

### Candidate inventory and untrusted claims

The required source/delivery artifacts are present as regular files:
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`. The required untrusted run records
are also present: `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and one structured JSONL generation trace. There are no
symlinked candidate entries and no candidate helper K files.

The candidate additionally contains `__pycache__`, `semantic-kompiled`, and
`verification-kompiled`. They are untrusted generated artifacts, not source
integrity failures, and were excluded from the scratch copy. The exact copy
command is in `evidence/01-scratch-copy.log`.

The untrusted records claim a 579-second, exit-0 generation and an end-to-end
`#Top`. The structured trace contains 163 parseable records and repeats those
claims. They were indexed, not accepted as verification evidence; see
`evidence/02-untrusted-trace-index.log`.

### Trusted comparisons

The candidate prompt is byte-identical to `/reference/prompt.py`, SHA-256
`6c3987abb35a3e0bf61eb7bd7e709b0abecef72c47dcb61a6ba84b0d46d760a0`.
The candidate translator is byte-identical to `/reference/py2mpy.py`, SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.
Both `cmp` commands exited 0. See
`evidence/03-provenance-comparison.log`.

No required source artifact is missing, mistyped, changed from a trusted
counterpart where a trusted counterpart exists, or symlinked. There is no
infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and trusted canonical behavior

The prompt asks for `change_base(x: int, base: int)` to return the string
representation of `x` in `base`, says bases are less than 10, and gives:

- `change_base(8, 3) == "22"`
- `change_base(8, 2) == "1000"`
- `change_base(7, 2) == "111"`

It does not explicitly state `x >= 0` or `base >= 2`. The trusted canonical
starts with `ret = ""`, repeatedly prepends `str(x % base)` while `x > 0`,
and returns `ret`. Thus it implements the usual positive-input conversion for
valid bases but returns `""` for `x = 0`.

The candidate instead uses:

```python
if x < base:
    return str(x)
return change_base(x // base, base) + str(x % base)
```

For nonnegative `x` and bases 2 through 9, this is the standard recurrence,
except that its zero case is `"0"` rather than the canonical `""`.

### Trusted translation

Running the trusted translator over the scratch `solution.py` produced
`solution.regenerated.mpy` with the same SHA-256 as the submitted
`solution.mpy`,
`b24e22f9a8fa6426e18daa45874f69927cd37d6bafc9d57baa94ac29cdab51ad`.
`cmp` exited 0. See `evidence/04-translator-regeneration.log`.

### Independent differential test

`evidence/differential_test.py` independently imports
`/reference/canonical.py` and the scratch candidate. Its 742 unique inputs
cover the three examples; zero; `base - 1`, `base`, `base + 1`, and square
boundaries for every base 2–9; all `x` from 0 through 64 for every base; 200
deterministically generated cases with seed 440044; ordinary large values; and
inputs around Python's recursion limit.

The command exited 1 because it found 9 mismatches:

- Eight mismatches are `x = 0`, one for each base 2–9: canonical `""`,
  candidate `"0"`.
- At `x = 2**1100, base = 2`, the canonical loop returns a 1101-character
  binary string, while default CPython execution of the recursive candidate
  raises `RecursionError`.

The remaining 733 cases matched, including all documented examples. The
complete inputs and outcomes are in `evidence/05-differential.log`; the
mismatch-only index is `evidence/16-differential-summary.log`.

The zero divergence is material to intent adequacy because the formal claim
explicitly admits zero. The recursion divergence is a concrete boundary
between idealized unbounded-stack semantics and default CPython, not an
algorithmic base-conversion error at ordinary sizes.

## 3. Clean proof reconstruction

### Toolchain

The live independent toolchain is K v7.1.293. `kompile`, `krun`, and `kprove`
are `/usr/bin` executables. `kup` is unavailable, but the independent K
installation runs correctly. See `evidence/06-toolchain.log`.

### Fresh builds

From the source-only scratch copy, I ran:

```text
kompile --backend llvm semantic.k --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-kompiled
```

This exited 0 (`evidence/07-build-concrete-llvm.log`).

I separately ran:

```text
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled
```

This exited 0 (`evidence/08-build-proof-haskell.log`).

The scratch source hashes equal the original candidate source hashes; see
`evidence/14-static-source-index.log`. Neither build reused
`/candidate/semantic-kompiled` nor `/candidate/verification-kompiled`.

### Positive proof claim

`spec.k` contains exactly one positive reachability claim. I ran:

```text
kprove spec.k --definition audit-verification-kompiled \
  --spec-module SPEC
```

It printed `#Top` and exited 0. See
`evidence/09-positive-spec.log`.

### Fresh concrete generated-semantics execution

`evidence/concrete_semantics_compare.py` ran the fresh LLVM definition on the
three examples, both sides of the `x < base` boundary at bases 2 and 9, zero,
the candidate's larger `1234, 7` example, and the recursion-limit witness.
Every individual `krun` command exited 0.

For the 12 ordinary and branch-boundary cases, K agreed with `solution.py`.
At zero, K correctly agreed with the submitted candidate and disagreed with
the canonical. At `2**1100, 2`, K returned the 1101-character string while
default CPython raised `RecursionError`. The comparison wrapper therefore
exited 1 with:

```text
K_VS_CANDIDATE_MISMATCHES: 1
K_VS_CANONICAL_MISMATCHES: 2
```

This is preserved in `evidence/10-concrete-semantics.log`, with a compact
index in `evidence/17-concrete-summary.log`. It is not a K build/proof
infrastructure failure; it is evidence about the runtime abstraction.

## 4. Adequacy and real-program pinning

### Entry claim in plain language

Precondition: `X` is a mathematical integer with `X >= 0`; `B` is an integer
with `2 <= B <= 9`; `CONT` is an arbitrary K continuation.

Initial state: the `<k>` cell begins with a call to `change_base` in a
one-function module whose body is fully embedded in the claim, followed by
`CONT`.

Postcondition: execution reaches
`strVal(baseString(X, B)) ~> CONT`. The same continuation must be preserved.

`baseString` is defined by two equations:

```text
baseString(X, B) = Int2String(X)                         if X < B
baseString(X, B) = baseString(X / B, B) ++ Int2String(X % B)
                                                           if B <= X and B > 0
```

On the formal domain, these cases are disjoint and exhaustive. In the
recursive case, `B >= 2` makes `X / B < X`, so the mathematical recurrence
descends.

### Exact program identity and control flow

The `Module(FuncDef(...))` term in `spec.k` lines 11–25 matches the trusted
regeneration of `solution.mpy` lines 1–13, including:

- function name and two parameter names;
- the `x < base` test;
- the one-argument `str(x)` call;
- the empty `else` statement list;
- the later recursive return;
- left-to-right `//`, recursive call, `%`, `str`, and string concatenation.

The `.mpy` surface syntax renders the empty `else` list by an empty position;
the claim writes the same list explicitly as `.Stmts`. There is no substituted
helper program.

There is no separate loop/helper claim. The sole entry claim is used
coinductively for the real recursive `call`; quantifying `CONT` lets it match
the recursive call while the caller's `str(x % base)` and concatenation
continuation remain pending. The operational rules preserve that continuation.
A separate ground continuation-sensitivity claim executes
`change_base(8, 3)` followed by a prefix-concatenation continuation and proves
the result `"P22"`; it printed `#Top` and exited 0. See
`evidence/spec-context.k` and `evidence/15-context-proof.log`.

The result is constrained to the locally defined `baseString(X, B)`. It is not
a free result variable, a tautology, an implication with a missing converse, or
an opaque symbol shared between an execution shortcut and the postcondition.
No rule rewrites the program call directly to `baseString`.

### Satisfiable instances

`X = 8`, `B = 3`, `CONT = .K` satisfies the precondition and gives formal,
candidate, and canonical result `"22"`.

`X = 0`, `B = 2`, `CONT = .K` also satisfies the precondition. The formal
postcondition and candidate both give `"0"`, while the trusted canonical gives
`""`. Other ground instances are recorded in
`evidence/claim_instances.py` and `evidence/13-claim-instances.log`.

Thus the claim pins and constrains the submitted program, but its stated
domain/result does not perfectly pin the canonical behavior.

## 5. Rule-by-rule static soundness review

### Local declaration inventory

`semantic.k` declares:

1. `Program`: `Module(Stmts)`.
2. `Stmts`: a whitespace-separated `List{Stmt, ""}`.
3. `Stmt`: `FuncDef(String, Params, Stmts)`,
   `If(Expr, Stmts, Stmts)`, and `Return(Expr)`.
4. `Params`: exactly two string names.
5. `Exprs`: comma-separated `List{Expr, ","}`.
6. `Expr`: `Name(String)`, `Int(Int)`,
   `BinOp(String, Expr, Expr)`, `Compare(Expr, CmpOp)`, and
   `Call(Expr, Exprs)`.
7. `CmpOp`: `CmpOp(String, Expr)`.
8. `Value`: `intVal(Int)`, `strVal(String)`, and `boolVal(Bool)`.
9. The function `appendStmts(Stmts, Stmts)`.
10. Internal `KItem` symbols: `call`, `exec`, `eval`, `branch`, `cmpLeft`,
    `cmpRight`, `binLeft`, `binRight`, `toString`, `callArgLeft`, and
    `callArgRight`.

`verification.k` declares the function
`baseString(Int, Int) : String`.

There are no local `[total]` declarations, `[functional]` declarations,
opaque symbols, priority rules, or `[simplification]` rules. The only local
`[function]` symbols are `appendStmts` and `baseString`. Imported K
constructors and built-ins remain part of the K trust boundary.

The configuration has only a `<k>` cell. The immutable program and local
binding map are explicit arguments to internal control terms. That is
sufficient for this stateless source program: it has no assignment, heap,
allocation, I/O, mutation, or exception handler. Recursive caller state is
retained in K continuations.

### Used-construct coverage

| Submitted construct | Declaration | Rules that supply behavior |
|---|---|---|
| `Module`, `FuncDef`, `Params` | `Program`, `Stmt`, `Params` | function lookup/binding R3 |
| statement sequence and empty `else` | `Stmts` | R1–R2, R4–R8 |
| `If` | `Stmt` | R6–R8 |
| `Return` | `Stmt` | R5 |
| `Name` | `Expr` | R10 |
| `<` comparison | `Compare`, `CmpOp` | R11–R13 |
| `//`, `%`, string `+` | `BinOp` | R14–R18 |
| built-in `str` call | `Call`, `Exprs` | R19–R20 |
| recursive two-argument call | `Call`, `Exprs` | R21–R23 and R3 |

The `Int` source literal syntax/rule is present but unused by the submitted
program. Missing behavior for other operators, call shapes, and Python
constructs is visible as a stuck term and is not a defect under the generated
minimal-semantics boundary because the submitted program does not use them.

### Exhaustive rule inventory and decisions

| ID and location | Rule | Decision |
|---|---|---|
| R1, `semantic.k:37` | `appendStmts(.Stmts, SS) => SS` | Correct empty-list identity. |
| R2, `semantic.k:38` | Move the head of a nonempty list and recurse on its tail. | Correct, structurally descending, disjoint from R1; together R1–R2 cover all `Stmts`. |
| R3, `semantic.k:59–65` | Match the one-function module, function name, and two parameters; create a fresh map and `exec` the exact body. | Correct binding for the fixed program and preserves the framed continuation. It intentionally models an unbounded abstract stack; it is not exact default-CPython resource behavior. Concrete scope witness: `X=2**1100, B=2` returns in K but raises `RecursionError` in CPython. |
| R4, `semantic.k:67` | Empty statement execution returns `strVal("")`. | Never reached by the submitted body for any formal-domain input because both control paths encounter a `Return`. Python fall-through would return `None`, so this is an over-broad unused-subset rule. There is no intended-input witness through the real program; it is recorded as a scope gap, not labeled an unsound proof rule. |
| R5, `semantic.k:72` | `Return(E)` discards the remaining current statements and evaluates `E`. | Correct for the fixed subset. The outer call continuation remains framed, so return exits the current body without discarding caller work. |
| R6, `semantic.k:74–78` | Evaluate the `If` condition before branching, retaining then/else/rest and environment. | Correct evaluation order and state retention. |
| R7, `semantic.k:79–83` | True branch executes `THEN` followed by `REST`. | Correct. `appendStmts` supplies sequencing. |
| R8, `semantic.k:84–88` | False branch executes `ELSE` followed by `REST`. | Correct; for the submitted empty `ELSE`, this reaches the later recursive `Return`. R7 and R8 are disjoint. |
| R9, `semantic.k:91` | Evaluate `Int(I)` to `intVal(I)`. | Correct but unused by this program. |
| R10, `semantic.k:92` | Evaluate `Name(X)` by map lookup. | Correct for the fixed bound names `x` and `base`. Unbound-name exceptions are outside the used subset and would instead stick. |
| R11, `semantic.k:95–99` | Begin a comparison by evaluating its left operand. | Correct left-to-right order. |
| R12, `semantic.k:100–104` | After the left value, evaluate the right and retain the left value. | Correct binding/order. |
| R13, `semantic.k:105–106` | For integer `<`, compute `boolVal(I <Int J)` from saved left `I` and current right `J`. | Correct; operand order is not reversed. |
| R14, `semantic.k:109–113` | Begin a binary operation with the left operand. | Correct left-to-right order. |
| R15, `semantic.k:114–118` | Evaluate the right operand while retaining the left. | Correct; caller environment/program are preserved. |
| R16, `semantic.k:119–121` | Saved-left `I // J` becomes `I /Int J` when `J != 0`. | Correct on the formal nonnegative domain. Python/K rounding differences for negatives and zero-division exceptions are outside the formal domain. |
| R17, `semantic.k:122–124` | Saved-left `I % J` becomes `I %Int J` when `J != 0`. | Correct on the formal nonnegative domain; the divisor is always `B >= 2`. |
| R18, `semantic.k:125–126` | Saved-left string `S` plus right string `T` becomes `S +String T`. | Correct operand order and value. |
| R19, `semantic.k:129–133` | One-argument `Call(Name("str"), ARG)` evaluates `ARG`, then `toString`. | Correct for the fixed builtin binding and source environment. It deliberately does not model rebinding of `str`, which the fixed source cannot perform. |
| R20, `semantic.k:134` | `intVal(I) ~> toString()` becomes `strVal(Int2String(I))`. | Correct for all integer values reached; in the formal program these are digits 0–8 or the base-case `X` 0–8. |
| R21, `semantic.k:136–140` | A two-argument direct-name call evaluates its first argument. | Correct for the recursive call. The one-argument builtin rule is arity-disjoint. |
| R22, `semantic.k:141–145` | After argument 1, evaluate argument 2 and retain argument 1/program. | Correct Python argument order for the used call. Callable-name resolution is fixed and side-effect-free here. |
| R23, `semantic.k:146–150` | After argument 2, invoke `call(PGM, F, V1, V2)`. | Correct for the fixed recursive binding and preserves the remaining caller continuation. |
| V1, `verification.k:11–12` | `baseString(X,B) => Int2String(X)` if `X < B`. | Truthful base case on the formal domain, where `0 <= X < B <= 9`. It defines zero as `"0"`, which matches the candidate but not the trusted canonical. It does not replace program execution. |
| V2, `verification.k:14–16` | Recursive quotient/remainder equation when `B <= X` and `B > 0`. | Truthful and descending on the formal domain `B >= 2`. Its written guard also admits `B = 1`, where it does not descend; that is outside every claim precondition. With no intended-domain false witness, this is recorded as an over-broad termination/coverage gap rather than an unsound conclusion used by the proof. |

### Overlap, totality, state, and proof-extension conclusion

The operational rules are separated by front symbol, value type, operator
string, boolean, or call arity. No priority is needed and no harmful overlap
was found. `appendStmts` is covered and terminating on all lists.
`baseString` has disjoint/exhaustive guards and descends for every use under the
entry precondition. Division/modulo guards are satisfied because `B >= 2`.

The local environment map is newly constructed for each call. The caller map
needed after a recursive result is held by `binLeft`; there are no source state
updates to lose. Calls evaluate arguments left-to-right. Return discards only
the current body's remaining statements and preserves the outer continuation.
The context proof in Stage 4 confirms an observable continuation is preserved.

`baseString` is a definitional summary, not an operational bridge: no semantic
rule rewrites a source call or expression to it. It has no opaque or fresh
interpretation. The entry reachability claim itself is the connection theorem
between exact execution and the summary. Therefore no task answer is smuggled
through an unconstrained oracle.

No rule was labeled materially unsound on the intended idealized semantics.
The two narrower gaps have explicit scope: unused fall-through semantics and
`B = 1` in the summary guard. The concrete `2**1100` witness establishes the
separate CPython resource-model limitation.

## 6. Fresh non-vacuity test

No candidate `spec-vacuity.k` was present. I authored
`evidence/spec-vacuity.k`, preserving the exact program and precondition but
changing the required result to:

```text
strVal(baseString(X, B) +String "0") ~> CONT
```

This is meaningfully false. For the satisfying witness `X = 0, B = 2`,
execution and the original postcondition produce `"0"`, while the mutation
requires `"00"`.

First:

```text
kprove spec-vacuity.k --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, confirming successful parsing/building
(`evidence/11-vacuity-dry-run.log`).

Then the same command without `--dry-run` exited 1 with
`WarnStuckClaimState`. The residual explicitly contains the unmet condition:

```text
#Not ( { Int2String ( X ) +String "0" #Equals Int2String ( X ) } )
```

See `evidence/12-vacuity-proof.log`. This is the expected reachable
postcondition failure, not a parser error, missing import, timeout, or unrelated
crash. The original proof is non-vacuous and result-discriminating.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the rebuilt K definition, for every mathematical integer `X >= 0`, every
integer base `2 <= B <= 9`, and every K continuation `CONT`, execution of the
exact submitted `.mpy` module from:

```text
call(PGM, "change_base", intVal(X), intVal(B)) ~> CONT
```

reaches:

```text
strVal(baseString(X, B)) ~> CONT
```

as a partial-correctness reachability claim. The `#Top` does not by itself
prove the candidate comment's stronger phrase “Total functional correctness,”
does not establish default-CPython resource behavior, and does not prove
equivalence to the trusted canonical at zero.

### Trust ledger

| Boundary | Dependents/effect | Assessment |
|---|---|---|
| K v7.1.293 parser, kompilers, LLVM/Haskell backends, and reachability prover | All build, execution, and proof results | Necessary low-level trust boundary; independently rebuilt with exact logs. |
| Imported `INT`, `BOOL`, `STRING`, `MAP`, list syntax, and builtins `/Int`, `%Int`, comparisons, `Int2String`, map lookup, and `+String` | Arithmetic, digits, environments, and the final string | Acceptable standard K primitives. Their used nonnegative cases have ordinary mathematical meanings and concrete checks. |
| Trusted `/reference/py2mpy.py` | Link from `solution.py` to `solution.mpy` | Strong evidence: trusted regeneration is byte-identical. |
| Generated MiniPython operational semantics | Link from `.mpy` execution to Python behavior | Statically audited for every used construct and concretely agrees on all ordinary tested cases. It remains an idealized language model, not a complete CPython semantics. |
| Unbounded abstract call stack | Normal result for arbitrarily large formal `X` | Concerning but generic runtime abstraction. Concrete witness `2**1100, 2`: K returns, default CPython raises `RecursionError`. The theorem should be read under the unbounded-stack assumption or with an input-size bound. |
| Mathematical integers/strings and omitted resource exhaustion | Numeric/string behavior and termination resources | Conventional formalization boundary; it excludes finite memory, stack, and implementation resource limits. |
| `baseString` equations | Final result meaning | Not opaque and not assumed: equations are explicit, disjoint, covered, and descending on the claim domain. Their identification with positional base notation is an ordinary informal mathematical bridge, not a second K theorem. |
| Prompt-to-formal-domain bridge | Restriction to `X >= 0`, bases 2–9 | Concerning adequacy limitation: the prompt only explicitly says bases are less than 10. The lower bounds and nonnegative `X` are reasonable numeral-system assumptions but are not stated in the prompt. |
| Trusted canonical behavior | HumanEval reference intent | Material zero discrepancy: canonical `""` versus proved candidate `"0"` for every base 2–9. Finite differential evidence supports equivalence for 733 other tested cases but cannot erase this mismatch or prove universal equivalence. |

There are no local opaque symbols, externally supplied result oracles, assumed
program helpers, proof-local operational bridges, priority overrides, or
unproved simplification lemmas.

### Gate accounting and decision

- Real-program soundness under the selected generated semantics: **pass**.
  The exact program executes, the continuation and state footprint are
  preserved, the result summary is connected by the entry claim, and a false
  result mutation is rejected.
- Intent/language adequacy: **limited**. The canonical zero behavior differs,
  the prompt-to-precondition bridge is partly implicit, and the generated
  semantics abstracts from CPython recursion limits.
- Trust/evidence auditability: **pass with the limitations above made
  explicit**. Commands, statuses, inputs, and bounded outputs are preserved.

This corresponds to a sound-but-limited proof: legitimate for the exact
submitted program in the stated idealized semantics, but not a PASS-level proof
of canonical/default-CPython behavior over the entire unbounded precondition.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
