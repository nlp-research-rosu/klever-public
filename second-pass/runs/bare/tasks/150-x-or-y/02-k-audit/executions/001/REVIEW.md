# Independent adversarial review: 150-x-or-y

This review treats all material under `/candidate` as untrusted evidence. I did
not reuse candidate-provided kompiled definitions, caches, logs, traces, or
reported `#Top` results. Source artifacts were copied to
`/tmp/audit-work/build`, rebuilt there, and tested using reviewer-authored
artifacts under `/audit-output/evidence`.

The audit used the required Kit workflow in this order: `using-kit`,
`validating-proof`, and (because the rendered mode is `GENERATED_SEMANTICS`)
`writing-semantics`.

## 1. Input and provenance integrity

### Rendered semantics boundary

The trusted mount is consistent with `GENERATED_SEMANTICS`:

- `/reference/reference-semantics` does not exist and is not a symlink.
- I did not search for, infer, or use a hidden reference semantics.
- The only local K source files in the candidate are `semantic.k`,
  `verification.k`, and `spec.k`; there are no hidden helper K source files.

This is recorded in `evidence/01-provenance.log` (exit 0).

### Required artifacts and trusted identities

Every inspected required candidate artifact is a regular file, not a symlink:

`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`.

The two required identity comparisons passed byte-for-byte:

| Artifact | Candidate/trusted SHA-256 | Result |
|---|---|---|
| `prompt.py` | `d3c5a3ef8fbe608f4c6ddb2b0209fe20ac537b827fb3252e805681c6c92c3a14` | identical |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | identical |

No missing, changed, mistyped, or symlinked required artifact was found.
Candidate-generated `llvm-kompiled`, `semantic-kompiled`,
`verification-kompiled`, `__pycache__`, logs, and traces are additional
untrusted build/evidence artifacts. They were inventoried but excluded from all
reconstruction.

### Untrusted generation claims

I read the required metadata only as claims:

- `run-input.json` identifies problem `150-x-or-y`, condition `bare`, and says
  no semantics was supplied.
- `metrics.json` reports a successful, non-timeout generation.
- `codex-last.txt` claims four successful concrete runs, two successful proof
  commands, a Python oracle run, and translator identity.
- `codex-output.log` contains reported `#Top` text and a success marker.
- One structured JSONL trace is present. It is a regular file, all records
  parse as JSON, and its record-type counts and hash are in the provenance log.

None of those claims was used as proof evidence. They were reconstructed below.

Stage 1 result: **PASS**.

## 2. Program fidelity and candidate-versus-canonical checks

### Natural-language contract and canonical behavior

`/reference/prompt.py` asks for `x_or_y(n, x, y)` to return `x` exactly when
`n` is prime and `y` otherwise. The examples require:

- `x_or_y(7, 34, 12) == 34`;
- `x_or_y(15, 8, 5) == 5`.

`/reference/canonical.py` implements trial division over `range(2, n)`, with a
special case for `n == 1`. For positive integers it realizes the stated
contract. For `n <= 0`, the range is empty and its `for`-`else` returns `x`,
although such an integer is not prime. That trusted canonical/contract
disagreement is material to domain accounting below.

The candidate `solution.py` uses the standard square-root trial-division
algorithm:

1. return `y` when `n < 2`;
2. try divisors starting at 2 while `divisor * divisor <= n`;
3. return `y` on a divisor;
4. otherwise increment the divisor and ultimately return `x`.

This is a different but correct algorithm for mathematical integers. It also
fixes the canonical's `n <= 0` behavior relative to the written prime
contract.

### Trusted translation

I regenerated the constructor program with the trusted translator:

```text
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp -s regenerated-solution.mpy solution.mpy
```

The command exited 0. Both files have SHA-256
`49abec0a167b6884ce55b00cf1ecdd07e8079ef83570b131580ed884535181d2`.
See `evidence/03-translate.log`. Relevant translator mappings for constants,
names, binary operations, comparisons, function definitions, returns,
assignments, `if`, and `while` are preserved in
`evidence/23-translator-snippets.log`.

### Independent differential test

`evidence/differential_test.py` independently imports:

- the trusted `/reference/canonical.py` copy;
- the candidate `solution.py` copy;
- a separately implemented `math.isqrt` primality oracle.

It exercises the two documented examples; `n = -5, 0, 1, 2, 3, 4`; initial
loop-guard boundaries; first and later divisor branches; odd and larger perfect
squares; larger prime/composite cases; equal `x` and `y`; and a deterministic
generated set for every `n` from -20 through 500 with varied `x` and `y`.
There is no collection-valued empty case; `n = 0` is the relevant numeric
boundary.

Exact command:

```text
python3 /audit-output/evidence/differential_test.py
```

It exited 0 (`evidence/02-differential.log`) with:

- 17 documented/boundary cases plus 521 generated cases;
- zero candidate-versus-contract mismatches;
- zero candidate-versus-canonical mismatches for `n >= 1`;
- 23 observed candidate-versus-canonical mismatches for tested `n <= 0`.

For each `n <= 0` mismatch, the candidate returned `y`, matching the written
contract and independent prime oracle, while the canonical returned `x`.
Therefore this is not evidence that the generated implementation violates the
natural-language task. It is an ambiguity in using canonical equality as an
unqualified oracle because the prompt states no positive-only precondition.

Stage 2 result: **PASS with a documented canonical/domain concern**.

## 3. Clean proof reconstruction

### Isolation and toolchain

Only candidate source files were copied to `/tmp/audit-work/build`. No
candidate `*-kompiled` directory or cache was copied or referenced. The live
toolchain is K `v7.1.293` and Python `3.10.12`; see
`evidence/00-tool-versions.log`.

### Fresh generated-semantics build and concrete execution

Fresh LLVM build:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition llvm-audit-kompiled
```

Exit 0, `evidence/04-kompile-llvm.log`.

`evidence/concrete_compare.py` invoked that fresh definition and compared its
terminal `<result>` with direct candidate Python execution for ten cases:
`n = -1, 0, 1, 2, 3, 4, 9, 25, 97, 121`. These cover both early-return
outcomes, zero loop iterations, true and false inner branches, increment and
loop-back, later divisors, primes, and square boundaries. Every `krun` exited 0
and all ten results matched Python (`evidence/05-concrete-compare.log`).

Full terminal configurations are preserved for:

- normal prime input `n=7, x=34, y=12`, result `intVal(34)`:
  `evidence/18-krun-normal-full.log`;
- boundary input `n=0, x=34, y=12`, result `intVal(12)`:
  `evidence/19-krun-boundary-full.log`;
- reachable loop witness `n=9, x=13, y=29`, ending with divisor 3 and result
  `intVal(29)`: `evidence/25-krun-loop-witness.log`.

### Fresh proof-definition build

Fresh Haskell build:

```text
kompile verification.k --backend haskell \
  --main-module MPY-VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-audit-kompiled
```

Exit 0, `evidence/06-kompile-haskell.log`.

### Positive target proofs

The original source modules were first run without alteration:

| Target | Exact command | Exit/output |
|---|---|---|
| generalized loop claim | `kprove spec.k --definition verification-audit-kompiled --spec-module LOOP-SPEC` | 0, `#Top` |
| all three entry claims | `kprove spec.k --definition verification-audit-kompiled --spec-module SPEC` | 0, `#Top` |

See `evidence/07-kprove-loop.log` and
`evidence/08-kprove-spec-all.log`.

I then added labels only in a reviewer copy to check the concrete claims
separately:

| Claim | Exact command suffix | Exit/output |
|---|---|---|
| `n=7` example | `--spec-module SPEC --claims SPEC.example-seven` | 0, `#Top` |
| `n=15` example | `--spec-module SPEC --claims SPEC.example-fifteen` | 0, `#Top` |

See `evidence/10-kprove-example-seven-only.log` and
`evidence/11-kprove-example-fifteen-only.log`.

Filtering only the universal claim from the original combined module also
filters out the imported loop circularity on which it depends. I interrupted
that diagnostic after about 61 seconds; it is recorded, and not counted as a
target-proof result, in `evidence/09-kprove-universal-only.log`. I then created
`evidence/spec-universal-only.k`, which contains only the exact universal claim
and its exact imported loop lemma, omitting both concrete examples:

```text
kprove spec-universal-only.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-UNIVERSAL-ONLY
```

That isolated universal proof exited 0 and printed `#Top`
(`evidence/12-kprove-universal-isolated.log`). The loop lemma had already been
proved independently. Thus the universal theorem does not depend on either
example, and neither example depends on the universal theorem.

Stage 3 result: **PASS**.

## 4. Adequacy and real-program pinning

### Plain-language claims

There are four positive reachability claims.

1. **Loop claim (`LOOP-SPEC`).** Starting exactly at the evaluation of the real
   loop guard, with the real loop body and the real trailing `return x`, an
   environment containing exactly `divisor=D`, `n=N`, `x=X`, and `y=Y`, empty
   result, and `D >= 2`, execution consumes the computation and returns `x` if
   no divisor from `D` through the square-root boundary is found, otherwise
   `y`. The final environment is intentionally existential and irrelevant to
   the return-value contract.

2. **Universal entry claim (`SPEC`, first claim).** For all K integers
   `N, X, Y`, from the initial empty environment and empty result, executing
   the exact submitted `x_or_y` constructor program consumes `<k>` and places
   `chooseVal(isPrime(N), X, Y)` in `<result>`.

3. **Prime example.** The same exact program at `(7, 34, 12)` returns
   `intVal(34)`.

4. **Composite example.** The same exact program at `(15, 8, 5)` returns
   `intVal(5)`.

The universal claim has no hidden `requires`: its formal domain is all
mathematical K integers for all three parameters. It does not quantify over
arbitrary Python objects.

### Satisfiable witnesses and substitutions

| Claim | Satisfying state/input | Claimed result | Candidate Python | Canonical Python |
|---|---|---|---|---|
| loop | `N=9,D=3,X=13,Y=29`, exact four-entry env, empty result | `primeFrom(9,3)=false`, hence 29 | whole entry reaches `D=3` and returns 29 | 29 |
| universal | `N=7,X=34,Y=12`, empty env/result | `isPrime(7)=true`, hence 34 | 34 | 34 |
| prime example | `7,34,12` | 34 | 34 | 34 |
| composite example | `15,8,5` | 5 | 5 | 5 |

The loop witness is reachable in the real program: at `n=9`, divisor 2 is
non-dividing, the assignment sets divisor 3, and the next guard is exactly the
loop claim's start configuration. The full run is in
`evidence/25-krun-loop-witness.log`.

At the additional universal witness `N=0`, the formal claim and candidate both
return `Y`; the canonical returns `X`. As judged in Stage 2, the formal claim
matches the written “prime/otherwise” contract there.

### Exact program pinning

The first `<k>` term in every entry claim is the submitted constructor program:
same function name and parameter order, initial `n < 2` branch, divisor
initialization, loop condition, divisor test, increment, and final return.

I independently rendered the claim's program as an external program term
(`evidence/claimed-program.mpy`), using the external list syntax's empty
position for the claim's explicit `.Stmts`, parsed both it and the submitted
`solution.mpy` to KORE with the fresh definition, and byte-compared the parsed
terms. Both parsed terms have SHA-256
`330bba1f8faf3a6e40bfa8d06593d59ede7289f47b1675fc4112394c0ba7e233`;
see `evidence/21-program-pinning-corrected.log`. The preceding
`evidence/20-program-pinning.log` records the harmless parser diagnostic that
`.Stmts` is internal K syntax, not accepted directly by the external program
parser.

The result is not free or tautological. `chooseVal` has exhaustive Boolean
equations to either `intVal(X)` or `intVal(Y)`, and the false-result mutation in
Stage 6 confirms that a wrong concrete result is rejected.

Stage 4 result: **PASS**.

## 5. Rule-by-rule static soundness review

Line-numbered copies of every relevant source are in
`evidence/13-source-listing.log`.

### Complete local syntax and attribute inventory

`semantic.k` declares:

- `Program`: `Module(Stmts)`;
- `Stmts`: a list of `Stmt`;
- `Stmt`: `FuncDef`, `If`, `While`, `Assign`, and `Return`;
- `Ids`: a comma-separated string list;
- `Expr`: `Int`, `Name`, `BinOp`, and `Compare`;
- `CmpOps`: a comma-separated `CmpOp` list;
- `CmpOp`: an operator string and right expression;
- `Val`: `intVal(Int)` and `boolVal(Bool)`;
- `KItem`: `exec`, `eval`, `store`, `binLeft`, `binApply`, `cmpLeft`,
  `cmpApply`, `branch`, `whileBranch`, and `doReturn`.

`verification.k` adds exactly three `[function]` symbols:

- `primeFrom(Int, Int) : Bool`;
- `isPrime(Int) : Bool`;
- `chooseVal(Bool, Int, Int) : Val`.

There are no local `[total]` declarations, `[functional]` declarations, opaque
symbols, priority rules, simplification rules, or proof-local operational
rewrites. There are no generated helper K files beyond these three K sources.

### Configuration

The configuration has exactly:

- `<k>` for the constructor program/current computation;
- `<env>` for local bindings;
- immutable input cells `<n>`, `<x>`, and `<y>`;
- `<result>` for the returned value.

There is no unused heap, call stack, I/O, exception, or allocation cell. This
is a one-function invocation semantics, not a general Python module semantics.
That representation is adequate for this program's used constructs.

### Mapping every submitted construct to behavior

| Used constructor/operator | Declaration | Rules |
|---|---|---|
| `Module(FuncDef("x_or_y", Params(...), BODY))` | `Program`, `Stmt`, `Ids` | S01 entry initialization |
| statement lists | `Stmts` | S02 empty, S03 head/tail sequencing |
| `If` | `Stmt` | S04 scheduling, S08/S09 Boolean branch |
| `While` | `Stmt` | S05 scheduling, S10/S11 loop/exit |
| `Assign(Name(...), ...)` | `Stmt`, `Expr` | S06 scheduling, S12 store |
| `Return` | `Stmt` | S07 scheduling, S13 abrupt function return |
| `Int`, `Name` | `Expr` | S14 literal, S15 lookup |
| `BinOp("*")`, `BinOp("%")`, `BinOp("+")` | `Expr` | S16/S17 evaluation order, S18-S20 operations |
| single `Compare` with `<`, `<=`, `==` | `Expr`, `CmpOps`, `CmpOp` | S21/S22 evaluation order, S23-S25 operations |

No used source construct is unmodeled or fabricated by a catch-all rule.

### All 25 ordinary semantic rules

| ID / source | Decision |
|---|---|
| S01 `semantic.k:51` | Sound harness entry for the exact function name/signature. It initializes exactly the three parameters from the input cells and executes the supplied body. It intentionally models invocation rather than Python's act of defining a module-level function. |
| S02 `:62` | Sound: executing an empty statement list is no computation. |
| S03 `:63` | Sound left-to-right statement sequencing via `S ~> exec(SS)`. |
| S04 `:65` | Sound `if` scheduling: condition first, then a branch continuation. |
| S05 `:66` | Sound `while` scheduling: condition first, retaining condition and body for re-evaluation. |
| S06 `:67` | Sound assignment scheduling for the only used target form, `Name`. |
| S07 `:68` | Sound return scheduling: evaluate the expression before return. |
| S08 `:70` | Sound true branch: execute `THEN`, then the represented rest. |
| S09 `:72` | Sound false branch: execute `ELSE`, then the represented rest. Guards are disjoint from S08. |
| S10 `:75` | Sound true loop step: execute body, reevaluate condition, recur. |
| S11 `:77` | Sound false loop exit. Disjoint from S10. |
| S12 `:80` | Sound store: after a value is obtained, update the named map binding and preserve the framed continuation. |
| S13 `:83` | Sound for this one-frame function: after a returned value and `doReturn`, clear all remaining function computation and set the initially empty result. Every reachable target return has a trailing `exec(...)` continuation, so the `_REST` requirement is met. |
| S14 `:86` | Sound integer literal conversion. |
| S15 `:87` | Sound lookup of the exact environment binding, preserving computation. |
| S16 `:90` | Sound binary-expression left-first scheduling. |
| S17 `:92` | Sound right-operand evaluation after the left integer value. |
| S18 `:94` | Sound unbounded integer addition. |
| S19 `:95` | Sound unbounded integer multiplication. |
| S20 `:96` | Sound modulo for nonzero right operand. In the real loop the divisor starts at 2 and increases, so zero is unreachable. |
| S21 `:99` | Sound scheduling for the submitted single comparisons. Chained comparisons are declared by the list syntax but deliberately unmodeled; none is used. |
| S22 `:101` | Sound right-side evaluation after the left integer value. |
| S23 `:103` | Sound integer `<`. |
| S24 `:104` | Sound integer `<=`. |
| S25 `:105` | Sound integer equality. |

Evaluation order is explicit. The target expressions are pure, but the rules
still preserve Python's left-before-right order. Statements are sequential;
the loop rechecks its guard after the assignment; return discards the remaining
function continuation; the only mutation is the environment update. K and
Python integers are both unbounded in this scope, and every modulo divisor on
the real path is positive.

The semantics is intentionally partial outside the target subset. Examples
include chained comparisons, arbitrary assignment targets, general function
calls, nested call frames, exceptions, and a bare top-level return with no
continuation. `writing-semantics` permits that minimality because none is used
by the submitted program and unmatched constructs stop rather than receiving a
fabricated value.

### All seven verification equations

| ID / source | Domain and decision |
|---|---|
| V01 `verification.k:9` | `primeFrom(N,D)=true` when `N < D*D`. Correct for actual `D>=2`: the search interval is empty. |
| V02 `:11` | `primeFrom(N,D)=false` when within the square bound and `D` divides `N`. Correct for actual `D>=2`. |
| V03 `:13` | Otherwise advance to `D+1`. Correct and descending toward V01 for actual `D>=2`. |
| V04 `:17` | `isPrime(N)=false` for `N<2`. This matches the written mathematical contract. |
| V05 `:19` | For `N>=2`, begin divisor search at 2. |
| V06 `:23` | Select `intVal(X)` for true. |
| V07 `:24` | Select `intVal(Y)` for false. |

For `D>=2`, V01-V03 are pairwise disjoint, exhaustive, and terminating: either
`D*D>N`, `D` divides `N`, or `D` increments. V04/V05 and V06/V07 are likewise
disjoint and exhaustive. No equation is marked `[total]`; in particular,
`primeFrom(N,0)` may be partial because its guards attempt modulo zero. That
case is outside every use: the loop claim requires `D>=2`, and `isPrime` starts
at 2.

The English comment that `primeFrom` means “no divisor in the inclusive range
from D” is only valid on the proof's `D>=2` domain. For example,
`primeFrom(100,-11)` takes V01 although the ordinary signed interval
`[-11,10]` contains divisors. This is an off-domain reusability/gloss gap, not
an unsound entry-proof rule: no entry or loop precondition permits such a `D`,
and it cannot enable a false conclusion for any intended input. I therefore do
not label it unsound. Narrowing the syntax or guards would improve reuse.

Reviewer finite evidence independently compared these helper equations with a
separate divisor-range definition for every `N=-20..500` and `D=2..30`:
15,109 cases, including both true and false outcomes, with zero mismatches.
See `evidence/helper_math_check.py` and `evidence/24-helper-math.log`. This is
supporting evidence, not the universal proof.

### Claims as proof extensions

The loop claim is a derived auxiliary reachability theorem, not an ordinary
semantic rule. Its matched context is exact:

- exact loop guard and body;
- exact trailing `exec(Return(Name("x")))`;
- exact four-entry environment;
- exact input and result cells;
- guard `D>=2`;
- no arbitrary continuation frame or omitted observable cell.

It has three cases corresponding to V01-V03. The non-dividing case performs
real semantic steps, increments `D`, then re-enters the same claim, which is the
guarded loop circularity permitted by partial-correctness reachability. The
base and divisor cases execute the fixed semantics to `x` and `y`
respectively. `evidence/07-kprove-loop.log` is therefore the required
bridge-free connection proof between real loop execution and `primeFrom`.

The universal claim invokes that proved exact loop lemma after the actual
assignment sets `D=2`; it does not contain a rule rewriting program execution
to `isPrime`. The proof helpers appear only in mathematical summaries and
postconditions. There is no fresh or opaque result-bearing oracle, no
one-way implication standing in for equality, and no task-answer rule that
preempts execution.

As an additional body-sensitivity check, I changed the divisor branch from
`return y` to `return x` while retaining the original concrete result
obligation at `n=9, x=13, y=29`. The mutation parsed successfully, then the
proof exited 1 and displayed the changed program's actual `intVal(13)` against
the required `intVal(29)`. See
`evidence/spec-body-sensitivity.k`,
`evidence/16-body-sensitivity-dry-run.log`, and
`evidence/17-body-sensitivity-kprove.log`.

No local rule was found that can enable a false entry conclusion on the
intended integer domain. Consequently there is no unsoundness claim requiring
a false-conclusion witness.

Stage 5 result: **PASS**, with the noted off-domain helper-gloss limitation.

## 6. Fresh non-vacuity test

The candidate supplied no `spec-vacuity.k`; I created a fresh auditor mutation
at `evidence/spec-vacuity.k`. It executes the exact submitted program at the
satisfiable prime input:

```text
n = 7, x = 34, y = 12
```

but changes the result-bearing obligation from the true `intVal(34)` to the
false `intVal(35)`.

Build/parse check:

```text
kprove spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module AUDIT-VACUITY --dry-run
```

Exit 0; see `evidence/14-vacuity-dry-run.log`.

Proof:

```text
kprove spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module AUDIT-VACUITY
```

Exit 1 with `WarnStuckClaimState`; see
`evidence/15-vacuity-kprove.log`. The residual is meaningful and directly
result-constraining:

```text
<k> .K </k>
<result> intVal ( 34 ) ~> .K </result>
```

The real computation terminated normally with 34 and could not unify with the
mutated destination 35. This is not a parser error, missing import, timeout,
unreachable mutation, or unrelated crash.

Stage 6 result: **PASS**.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Relative to the source `semantic.k`, standard imported K domains, and the
seven proof-helper equations, the successful universal claim establishes:

> For every K integer `N`, `X`, and `Y`, if the exact submitted
> `solution.mpy` program is placed in the stated initial configuration with an
> empty environment and empty result, its partial-correctness execution
> consumes the computation and returns `X` when `isPrime(N)` is true and `Y`
> when it is false.

Here `isPrime` is not opaque: it is defined to be false below 2 and otherwise
to search divisors from 2 through the square-root boundary. The proof also
establishes the exact generalized loop summary and both prompt examples.
Final local environment contents are deliberately not proven, because the
postcondition existentially frames them and the task observes only the return
value.

This is a partial-correctness result. Termination is not the theorem being
claimed, although the concrete algorithm's positive, monotonically increasing
divisor gives a straightforward informal termination argument for every
integer `N`.

### Trust and assumption ledger

| Boundary | Dependents | Assessment |
|---|---|---|
| K `INT`, `BOOL`, `STRING`, `MAP`, list syntax, K sequencing, parser, Haskell/LLVM backends | all builds, executions, proofs | Standard low-level proof TCB; acceptable and explicit. |
| Trusted mounted `py2mpy.py` maps CPython AST to constructor terms | real-program identity | Authority-designated trusted input; byte identity was checked and output regenerated. |
| Entry configuration treats `Module(FuncDef(...))` as invocation with integer input cells | all entry claims | A deliberate generated-semantics harness, not full Python module/call semantics. Exact for this target; supported by static inspection and concrete comparison. |
| Generated operational semantics matches Python for the used subset | bridge from K theorem to `solution.py` behavior | Exhaustively reviewed by construct/rule and tested on ten branch/boundary cases. Still an individually generated model, not a formal CPython refinement theorem. |
| Built-in integer arithmetic, especially `%Int` on positive divisors, matches Python integer arithmetic | loop condition and divisor test | Acceptable standard primitive boundary; actual divisors are always positive. |
| Number-theoretic fact: an integer `N>=2` is prime iff it has no divisor from 2 through `floor(sqrt(N))` | bridge from `isPrime` to the English word “prime” | Standard ordinary mathematics, argued informally rather than proved in a separate K theorem; supported by 15,109 helper checks and 538 end-to-end differential cases. |
| Formal parameters are K integers | universal theorem scope | The prompt has no explicit type annotation. This matches the examples/usual HumanEval integer reading but does not prove behavior for arbitrary Python values of `x` or `y` (even though the Python implementation merely returns them). |
| Trusted canonical behavior | candidate-versus-reference bridge | Exact agreement on all tested `n>=1`; disagreement for tested `n<=0`, where the candidate agrees with the written prime contract. The absence of an explicit positive-only prompt domain is a documented ambiguity. |
| Finite differential and concrete tests | empirical support only | Reproducible and broad for this small program, but not substituted for K reachability proof or a universal CPython correspondence theorem. |

There are no candidate-defined opaque symbols, unconstrained fresh
result-bearing values, empirical operational bridges inside K, or unproved
proof-local rewrites. The existential final environment does not affect the
return result.

### Gate and verdict rationale

- **Real-program soundness:** passes. The actual translated body executes; the
  loop summary has an independently closed exact-context connection claim; all
  positive targets close under a clean rebuild; false result and changed body
  probes fail for the expected terminal-value mismatches.
- **Intent adequacy:** legitimate for the integer reading of the prompt. The
  mathematical primality bridge is standard, but informal; the formal K
  theorem does not cover arbitrary Python object inputs; and the trusted
  canonical conflicts with the written contract for `n<=0`.
- **Evidence auditability:** passes. Scripts, inputs, exact commands, exit
  statuses, bounded outputs, mutations, and source listings are preserved
  under `/audit-output/evidence`.

The proof is therefore legitimate and result-constraining, not vacuous or
execution-bypassing. The appropriate result is `CONCERNS / LEGIT`, rather than
`PASS`, because the bridge from an individually generated integer-only
semantics to the untyped natural-language/Python task is not a universal CPython
refinement theorem, and the trusted prompt and canonical disagree on
nonpositive `n`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
