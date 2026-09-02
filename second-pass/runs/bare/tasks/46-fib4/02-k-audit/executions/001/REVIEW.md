# Independent adversarial audit: 46-fib4

The candidate contains a legitimate, result-constraining modular K proof for
nonnegative integer inputs.  It proves the real translated program under a
small generated semantics; it does not replace execution with the requested
answer.  The disposition is **CONCERNS / LEGIT**, rather than PASS, because the
rolling mathematical model is connected to the prompt recurrence by an
audited informal induction and finite differential evidence, the all-`n >= 4`
entry theorem is represented as two machine-checked claims whose composition is
meta-level rather than one machine-checked entry claim, and several `[total]`
attributes are broader than their equations.

All candidate files and generation records were treated as untrusted.  Nothing
under `/candidate` was executed or modified.  Source used for execution was
copied to `/tmp/audit-work/46-fib4`; neither
`/candidate/semantic-kompiled` nor any candidate cache was copied or used.
Commands and outputs are in `/audit-output/evidence`.  The tool versions were K
v7.1.293 and Python 3.10.12
([tool-versions.log](evidence/tool-versions.log)).

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree.  `/reference` contains the three
regular files `canonical.py`, `prompt.py`, and `py2mpy.py`, and
`/reference/reference-semantics` is neither present nor a symlink.  This is the
required boundary for `GENERATED_SEMANTICS`; no hidden or inferred reference
semantics was used.

All required candidate source/provenance artifacts are regular files:
`run-input.json`, `metrics.json`, `codex-last.txt`, `codex-output.log`,
`prompt.py`, `py2mpy.py`, `solution.py`, `solution.mpy`, `semantic.k`,
`verification.k`, `spec.k`, and `prove.sh`.  The structured trace is one
regular JSONL file with 336 valid JSON records and no malformed line.  There
are no symlinked, mistyped, or missing required artifacts.  There are no other
candidate helper K source files.  The additional
`/candidate/semantic-kompiled/` directory is an untrusted generated build
artifact, not an integrity failure; it was deliberately excluded.

The candidate prompt and translator are byte-identical to the trusted mounts:

- prompt SHA-256:
  `96e26625e9d731f1fea4d5f87089c184ef579180d536f358509ce635fff242b7`;
- translator SHA-256:
  `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`;
- both `cmp` commands exited 0.

`run-input.json` claims problem `46-fib4`, condition `bare`, no supplied
semantics, and records the same trusted hashes.  `metrics.json` claims an
exit-0, non-timeout generation.  `codex-last.txt`, `codex-output.log`, and the
trace claim all candidate proofs closed.  Those claims were not relied on.
The exact checks, hashes, clean-copy commands, and JSON rendering are in
[stage1-2.log](evidence/stage1-2.log); the bounded trace inventory is in
[stage1-trace-summary.log](evidence/stage1-trace-summary.log) and its
reviewer-authored parser is
[provenance_trace_summary.py](evidence/provenance_trace_summary.py).

Stage 1 result: no provenance or semantics-boundary integrity failure.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a nonnegative integer index `n`, the prompt defines

`F(0)=0`, `F(1)=0`, `F(2)=2`, `F(3)=0`, and
`F(n)=F(n-1)+F(n-2)+F(n-3)+F(n-4)` for `n >= 4`.

The implementation must compute `F(n)` efficiently without recursion.  The
documented outputs are `F(5)=4`, `F(6)=8`, and `F(7)=14`.  Sequence indexing
supplies the implicit `n >= 0` domain; the prompt does not specify behavior for
negative integers.

The trusted canonical implementation maintains a four-element list.  Candidate
`solution.py` uses the equivalent scalar window `(a,b,c,d)`, handles indices
0--3 by four branches, starts `i=4`, updates
`e=a+b+c+d`, shifts the window, increments `i`, and returns `d`.  It is
iterative and covers every nonnegative integer.

### Translation identity

The trusted translator was copied from `/reference` and run on the scratch
copy of `solution.py`.  The regenerated and submitted `solution.mpy` files have
the same SHA-256,
`1c47bc669cedb3c4f2e69dbb62bf0976c4b82f699f7ff0155f4217062eefd498`,
and `cmp` exited 0.  Thus the submitted K constructor program is exactly the
trusted translation of the submitted Python source
([stage1-2.log](evidence/stage1-2.log)).

### Independent differential test

[differential_test.py](evidence/differential_test.py) imports the trusted
`/reference/canonical.py` entry point and the independently copied generated
entry point by absolute path.  It tests:

- all indices 0--200;
- every explicit branch and loop boundary 0--5;
- all documented examples 5, 6, and 7;
- 100 deterministic generated indices in 0--1000 (seed 4604).

After deduplication this is 272 nonnegative inputs.  The command exited 0 with
zero mismatches; the complete input list and results are in
[stage1-2.log](evidence/stage1-2.log).  There is no container-valued “empty”
input for this function; `n=0`, which skips the loop and is the lowest sequence
index, was exercised.

Negative integers were deliberately characterized but excluded from the
sequence-index domain.  The candidate returns 0 for all tested negatives,
whereas the canonical Python implementation returns 2 for `-2` and raises
`IndexError` below `-4` because of Python list indexing.  No theorem below
claims negative behavior.

Stage 2 result: program and translation fidelity pass on the intended domain;
the negative-input scope restriction is explicit.

## 3. Clean proof reconstruction

The scratch directory initially contained only copied source, the trusted
translator, and its regenerated constructor file.  Fresh definitions were
built with:

```text
kompile semantic.k --backend llvm --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition semantic-llvm-kompiled

kompile semantic.k --backend haskell --main-module SEMANTIC \
  --syntax-module SEMANTIC-SYNTAX \
  --output-definition semantic-haskell-kompiled
```

Both exited 0.  LLVM reported non-exhaustive matches for the declared-total
`evalInt` and `evalBool`; those warnings are analyzed in Stage 5.

Fresh LLVM execution of the actual regenerated `solution.mpy` was compared
with independent Python execution at
`n = 0,1,2,3,4,5,6,7,10,20`.  Every `krun` exited 0, consumed `<k>` to `.K`,
and produced the same integer; the corrected harness reported zero mismatches
([semantic_crosscheck.py](evidence/semantic_crosscheck.py),
[stage3-concrete-corrected.log](evidence/stage3-concrete-corrected.log)).

Every positive claim was then selected and proved separately against the fresh
Haskell definition:

| Claim | `kprove` exit | Output |
|---|---:|---|
| `SPEC.fib4-spec-link` | 0 | `#Top` (also `WarnTrivialClaim`, as expected for a definitional link) |
| `SPEC.loop-correct` | 0 | `#Top` |
| `SPEC.fib4-inductive-init` | 0 | `#Top` |
| `SPEC.fib4-base-0` | 0 | `#Top` |
| `SPEC.fib4-base-1` | 0 | `#Top` |
| `SPEC.fib4-base-2` | 0 | `#Top` |
| `SPEC.fib4-base-3` | 0 | `#Top` |
| `SPEC.fib4-seven` | 0 | `#Top` |

The commands and complete bounded output are in
[stage3.log](evidence/stage3.log), driven by
[run_stage3.sh](evidence/run_stage3.sh).

Audit-harness disclosure: the first concrete-result parser used an
over-escaped whitespace regular expression.  Although its displayed K results
were correct and all eight proof invocations still ran and passed, that parser
reported false extraction mismatches and made the outer Stage 3 wrapper exit
1.  The one-line reviewer-script defect was corrected and rerun without
rebuilding or altering candidate source; the corrected concrete log exits 0
with ten equality records.  This is an audit-harness correction, not candidate
evidence or a candidate failure.

Stage 3 result: clean reconstruction passes.

## 4. Adequacy and real-program pinning

### Plain-language meaning of every claim

1. `fib4-spec-link`: for any `N >= 4`, with computation already finished and
   arbitrary environment, rewrites the result expression `fib4Spec(N)` to the
   initial rolling-window expression `advanceTo(0,0,2,0,4,N)`.  It executes no
   program and is purely definitional.
2. `loop-correct`: for `N >= 4`, `I >= 4`, and either `I <= N` or
   `I=N+1`, executing the exact submitted while-loop followed by `return d`
   from map values `(A,B,C,D,E,I,N)` consumes the computation and returns
   `advanceTo(A,B,C,D,I,N)`.  The final local map is existential because the
   contract constrains the return value, not final locals.  This is a
   circularity/loop-invariant claim.
3. `fib4-inductive-init`: for any `N >= 4`, executing `solutionProgram` from
   the initial empty environment reaches the exact real loop head plus
   `return d`, with `n=N`, window `(0,0,2,0)`, `e=0`, and `i=4`.  It is the
   finite initialization half and intentionally has not returned yet.
4. `fib4-base-0` through `fib4-base-3`: from the initial state with the fixed
   argument, the actual program terminates with `fib4Spec(0)` through
   `fib4Spec(3)` respectively.
5. `fib4-seven`: the actual program at argument 7 terminates with 14.

For `N >= 4`, the destination of `fib4-inductive-init` is syntactically the
`A=0,B=0,C=2,D=0,E=0,I=4` instance of `loop-correct`; its precondition follows
from `N >= 4`.  The loop result is exactly the right-hand side of
`fib4-spec-link`.  Transitivity of the two proved reachability facts therefore
gives the entry theorem
`solutionProgram(N) => result(fib4Spec(N))`.  The four base claims cover the
remaining nonnegative inputs.  This is a valid modular reachability argument,
but the candidate does not include a single separately machine-checked
composite entry claim for symbolic `N >= 4`; that is one reason for the
CONCERNS rating.

### Real-program pin

The proof's `<k>` uses the local symbol `solutionProgram`.  Its only rule
expands it to the complete constructor tree at `semantic.k:46-72`.  Static
comparison with `solution.mpy:1-33` shows every branch, initialization,
assignment, loop expression, shift, increment, and return in the same order;
empty branch lists are represented explicitly as `.Stmts`.  This is a
definitional alias, not a summary or answer oracle.

The pin has three independent checks:

- trusted regeneration is byte-identical to submitted `solution.mpy`;
- direct `krun solution.mpy` and `krun solution-alias.mpy` produced identical
  complete configurations for `n=0,2,3,4,7,10`;
- mutating the actual constructor body at the `n==2` return from 2 to 3 changed
  concrete K execution from 2 to 3.

The exact commands and outputs are in [stage4.log](evidence/stage4.log), with
[pinning_crosscheck.py](evidence/pinning_crosscheck.py) and the preserved
[solution-mutated.mpy](evidence/solution-mutated.mpy).  The proof alias would
of course have to be updated if the submitted source changed; the byte
identity check is the source-to-alias bridge for this fixed submission.

### Satisfiable preconditions and ground substitution

[adequacy_witnesses.py](evidence/adequacy_witnesses.py) records a satisfying
state for every claim: `N=7` for the spec link; loop witnesses both at
`I=4,(A,B,C,D)=(0,0,2,0)` and at the exit boundary
`I=8,(A,B,C,D)=(2,4,8,14)`; `N=4` for initialization; arguments 0--3 for the
base claims; and argument 7 for the ground example.  Every substituted
result agrees with both Python implementations, with zero mismatches
([stage4.log](evidence/stage4.log)).

The return value is never free: the base and ground claims fix it directly,
and the loop claim fixes it to a recursively defined integer function.

Stage 4 result: adequate and pinned, with the documented modular-composition
limitation.

## 5. Rule-by-rule static soundness review

The complete numbered source and mechanical declaration inventory are in
[stage5-inventory-corrected.log](evidence/stage5-inventory-corrected.log).
The first inventory attempt had only an over-escaped final `rg` expression and
exited 2 after already dumping the sources; the corrected inventory exits 0.

### Local syntax and configuration inventory

`SEMANTIC-SYNTAX` declares:

- `Program`: `Module(Stmts)` and the exact-program alias `solutionProgram`;
- separator-free `Stmts`;
- `Stmt`: `FuncDef`, `Return`, `Assign`, `If`, and `While`;
- one-string `Params`;
- `Exp`: `Int`, `Name`, `BinOp`, and `Compare`;
- `CmpOp`: an operator string and right expression.

`SEMANTIC` additionally declares `Result` (`noResult` or `result(Int)`) and the
control item `exec(Stmts)`.  Its configuration has exactly the needed cells:
`<k>` for control, `<arg>` for the supplied integer, `<env>` for locals, and
`<result>` for the observable return.  There is no unused heap, stack, I/O, or
allocation cell.

Every constructor in `solution.mpy` is covered: `Module/FuncDef/Params` by the
entry rule; statement-list sequencing by `exec`; each `If` is the
`Name == Int` form; assignments have a `Name` target; all RHSs use `Int`,
bound `Name`, or `BinOp("+",...)`; the loop is `Name <= Name`; and every return
uses a supported integer expression.

### All 14 semantic rules

1. `solutionProgram => Module(...)` is the exact AST alias described above.
   It embeds the program body, not the answer, and does not skip execution.
2. Module entry binds the single parameter to `<arg>` in an initially empty
   map and schedules the complete body.  This matches the submitted one-entry
   module.
3. `exec(.Stmts)` terminates an empty statement sequence.
4. Assignment evaluates the RHS against the pre-update map, updates only the
   named local, and then schedules the rest.  Sequential rule applications
   give Python's left-to-right statement order and the intended rolling shift.
5. The equality-true `If` rule schedules `THEN` before `REST`.
6. The equality-false `If` rule schedules `ELSE` before `REST`.
   Their integer guards `==Int` and `=/=Int` are disjoint and exhaustive.
7. The `<=`-true `While` rule schedules one body and then the same loop plus
   trailing statements.
8. The `<=`-false rule schedules the trailing statements.  Guards `<=Int` and
   `>Int` are disjoint and exhaustive.
9. `Return` evaluates its pure expression, stores the result, and discards the
   remaining function continuation.  There are no calls, nested frames,
   cleanup actions, exceptions, or side-effecting expressions in the modeled
   language, so its abrupt-control footprint is correct for every reachable
   submitted state.
10. `evalInt(Int(I),M)=I` is true.
11. `evalInt(Name(X),M)=M[X]` is true when the binding pattern matches; every
    used name is bound before evaluation.
12. `evalInt(BinOp("+",L,R),M)` is integer addition of recursively evaluated
    operands.  Expressions are pure, so there is no omitted evaluation-order
    effect.
13. `evalBool` for `==` is mathematically correct.
14. `evalBool` for `<=` is mathematically correct.  `evalBool` is not called
    by any operational rule or proof claim; branch rules implement their exact
    used comparison forms directly.

The model uses K's unbounded `Int`, matching Python integers for these
operations.  There is no modeled output, exception, allocation, mutation
outside local bindings, or function call because the submitted program uses
none.

### Verification functions and all seven equations

`advanceTo(A,B,C,D,I,N)` is declared `[function,total]`.

1. If `I>N`, it returns `D`.
2. If `I<=N`, it shifts the window, appends `A+B+C+D`, increments `I`, and
   recurses.

The guards partition all integer pairs.  The recursive branch strictly
increases `I` toward the base condition, so it terminates for fixed `N`.  The
equations are non-overlapping and faithfully describe one real loop step.

`fib4Spec(N)` is declared `[function,total]`.

3--6. Its four ground equations return 0, 0, 2, and 0.
7. For `N>=4`, it starts `advanceTo` from `(0,0,2,0,4,N)`.

The five applicable domains are disjoint and cover exactly the theorem domain
`N>=0`.  None of these functions rewrites a program term.  `advanceTo` is
connected to real loop execution by `loop-correct`; use of the same function
in that claim is not an opaque oracle because its exhaustive equations match
the concrete state transition one-for-one.

There are no local priority rules, simplification rules, `[concrete]` rules,
`[owise]` rules, `[functional]` declarations, fresh values, or opaque local
symbols.  The eight reachability claims inventoried in Stage 4 are the only
claims.

### Narrow coverage defects, not witnessed unsound conclusions

Three `[total]` annotations are broader than their defining equations:

- `evalInt` has no equation for `Compare`, arbitrary binary operators, or an
  unbound `Name`;
- `evalBool` has no equation for non-`Compare` expressions or operators other
  than `==` and `<=`;
- `fib4Spec` has no equation for `N<0`.

Ground uncovered terms include
`evalInt(Compare(Int(0),CmpOp("==",Int(0))),.Map)`,
`evalBool(Int(0),.Map)`, and `fib4Spec(-1)`.  LLVM explicitly warned that the
first two declarations are non-exhaustive.  These are real declaration/coverage
defects and reduce reusability, but they are not reached by the submitted
program or any positive claim.  No false result, branch, state, or exception on
the intended domain can be derived from them, so this review does **not** label
them materially unsound.  They are recorded as the narrower evidence gap
required by the audit instructions.

No rule encodes a requested Fib4 output for symbolic input, fabricates state,
replaces a property-bearing program computation by an unconstrained value, or
bypasses the submitted control flow.

Stage 5 result: sound on every used construct and theorem state; non-material
over-broad totality declarations remain a concern.

## 6. Fresh non-vacuity test

The reviewer-created [spec-vacuity.k](evidence/spec-vacuity.k) changes the
reachable base-2 result obligation from 2 to 3.  Its initial state has argument
2, empty environment, and `noResult`, so it is realizable without a
precondition.

First,

```text
kprove spec-vacuity.k --definition semantic-haskell-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

exited 0, establishing that the mutation parsed and built.  The actual proof
command exited 1 with `WarnStuckClaimState`; the residual configuration had
`.K`, environment `"n" |-> 2`, and `result ( 2 )`, so failure was exactly the
unmet false result obligation, not a parser error, timeout, missing import, or
unreachable mutation.  The reviewer wrapper then exited 0 after checking both
the warning and residual ([stage6.log](evidence/stage6.log),
[run_stage6.sh](evidence/run_stage6.sh)).

Stage 6 result: non-vacuity passes.

## 7. Proven versus assumed accounting

### What the reachability proof establishes

Under the audited generated semantics:

- for input 0, 1, 2, or 3, the exact submitted program terminates with the
  corresponding base value;
- for every integer `N>=4`, the exact submitted program reaches the real loop
  with window `(0,0,2,0)` at index 4, and the loop/return computation produces
  `advanceTo(0,0,2,0,4,N)`;
- by the `fib4Spec` equation, that result is `fib4Spec(N)`;
- the concrete input 7 returns 14.

Therefore, by reachability transitivity, the machine-checked claims establish
partial correctness of the exact submitted program for every nonnegative
integer with respect to `fib4Spec`.  The proof constrains the returned integer;
it does not merely state termination or permit an existential result.

### Trust ledger and limitations

| Boundary | Role and dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, and built-in `Int`, `Bool`, `String`, and `Map` modules | Parsing, arithmetic, maps, concrete execution, and all proofs | Standard low-level toolchain trust boundary; acceptable. |
| Trusted `/reference/py2mpy.py` | Connects `solution.py` to `solution.mpy` and the proof alias | Byte identity was independently checked; acceptable for this fixed source. |
| Generated Python-subset semantics | Connects constructor execution to Python behavior | Every used construct was statically reviewed and concretely cross-checked.  This is not a universal CPython equivalence theorem, but is an acceptable, explicit generated-semantics boundary for this small pure program. |
| `solutionProgram` AST alias | Connects spec entry states to the actual submitted constructor program | Exact local definition plus byte identity, direct/alias full-state comparisons, and body sensitivity.  Acceptable; not an oracle. |
| K `advanceTo` equations | Mathematical result of the real loop | Total, disjoint, descending, and machine-connected to execution by the circular `loop-correct` claim.  Acceptable. |
| Rolling model versus the prompt's four-term recurrence | Connects `fib4Spec` to natural-language intent | Informal induction: at loop index `i`, the window is `(F(i-4),F(i-3),F(i-2),F(i-1))`; one update preserves it and exit returns `F(N)`.  Supported by zero mismatches on 272 canonical inputs, but no separate K theorem states this recurrence equivalence.  Legitimate but a documented concern. |
| Composition of initialization and loop claims | Gives the symbolic `N>=4` entry theorem | The configurations unify exactly and reachability is transitive, but no one-piece composite claim was rerun.  Standard and sound meta-reasoning, with reduced audit convenience. |
| Trusted canonical implementation and differential tests | Empirical source/intent and semantics bridges only | Finite evidence, never used as a substitute for K proof. |
| `[total]` holes | Only unused syntax or `N<0` | Concerning declaration quality but irrelevant to every proved intended-domain execution; not used to prove a false conclusion. |
| Input-domain interpretation | All entry coverage | The proof covers `n>=0`; negative behavior is excluded and demonstrably differs from incidental canonical list-index behavior.  This matches ordinary sequence-index intent but is a documented scope choice. |

The proof does not establish behavior for negative or non-integer inputs, full
CPython exceptions/types, or a general reusable Python language.  It is a
partial-correctness proof; neither `PROOF.md`, candidate logs, the trace,
concrete tests, nor differential tests were treated as formal proof.

Final gate accounting:

- real-program soundness: pass;
- intended nonnegative Fib4 result: pass, with an informal recurrence bridge;
- evidence reproducibility: pass;
- non-vacuity: pass;
- remaining limitations are non-material to legitimacy but warrant CONCERNS.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
