# Independent adversarial review: 3-below-zero

## Outcome

The candidate contains a legitimate, result-constraining partial-correctness
proof of the submitted generated program on the intended domain of finite lists
of Python integers. Both positive claims were rebuilt from source and proved
independently with fresh definitions. The operational semantics executes the
actual translated body, and a false result mutation reaches a concrete
`BoolV(false)` state and is rejected.

The result is `CONCERNS / LEGIT`, rather than an unqualified pass, for two
non-fatal limitations:

1. `semantic.k` is deliberately a closed, task-specific entry-call harness.
   Some rules are syntactically broader than the one fixed program (notably the
   wildcard import rule, dedicated-variable lookups, and continuation-discarding
   return rule), although no such breadth enables a false conclusion for this
   program on the intended input domain.
2. The recursive `belowZeroFrom` postcondition is connected to execution by a
   universal K claim, but its equivalence to the English phrase “some running
   prefix is negative” is a straightforward informal structural-induction
   argument, not a second machine-checked prefix-sum theorem.

No candidate-provided build, cache, `#Top`, trace, or prose report was trusted.

## 1. Input and provenance integrity

The rendered mode and trusted mounts agree. This is
`GENERATED_SEMANTICS`, and `/reference/reference-semantics` does not exist.
There is therefore no supplied or hidden semantics baseline to use. The
candidate's generated semantics was reviewed on its own merits.

Required source artifacts are all present as regular files:

- `/candidate/solution.py`
- `/candidate/solution.mpy`
- `/candidate/semantic.k`
- `/candidate/verification.k`
- `/candidate/spec.k`
- `/candidate/prove.sh`
- `/candidate/prompt.py`
- `/candidate/py2mpy.py`

No symlink occurs anywhere under `/candidate`. The candidate prompt is
byte-identical to `/reference/prompt.py`, with SHA-256
`430706f794ffabb60ec5818ca7c9fdbd281b97ef9d3ac6d6ba140a7a2498f5a5`.
The candidate translator is byte-identical to `/reference/py2mpy.py`, with
SHA-256
`406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16`.

The candidate also contains extra generated material: `semantic-kompiled/`,
`semantic-llvm/`, `verification-haskell/`, `verification-kompiled/`,
`__pycache__/`, `kore-exec.tar.gz`, generation logs, metrics, and a structured
JSONL trace. These are not missing or mistyped required source artifacts, but
they are untrusted build/provenance evidence and were not copied into the fresh
proof workspace. There are no additional candidate helper `.k` files beyond
`semantic.k`, `verification.k`, and `spec.k`.

As untrusted claims, `run-input.json` identifies problem `3-below-zero`, the
`bare` condition, and no supplied semantics; `metrics.json` claims generator
exit 0; `codex-last.txt`, `codex-output.log`, and the structured trace claim two
successful proofs. Those claims were read but not relied upon.

Evidence:

- `evidence/stage1-integrity.log` — types, symlinks, mount boundary, hashes, and
  trace presence; exit 0.
- `evidence/stage1-untrusted-claims-final.log` — bounded copies/summaries of the
  untrusted provenance claims; exit 0.
- `evidence/stage1-untrusted-claims.log` — an initial reviewer-only extraction
  attempt exited 127 because `jq` is not installed. The shell-only extraction
  above replaced it; this has no bearing on the candidate.

There is no infrastructure-mode contradiction, so a candidate verdict is
appropriate.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a bank balance initially equal to zero, process the finite integer list in
order. Return `True` as soon as a nonempty running prefix has negative sum.
Return `False` if no running prefix is negative. A balance exactly equal to zero
is not below zero.

The trusted canonical program initializes `balance = 0`, adds each operation,
returns `True` immediately if `balance < 0`, and otherwise returns `False` after
the loop. `/candidate/solution.py` implements the same control flow, differing
only in the local iteration-variable name.

### Trusted regeneration

The submitted `solution.py` was translated in scratch with
`/reference/py2mpy.py`. The regenerated term is byte-identical to the submitted
`solution.mpy`; both have SHA-256
`9ffee3cf630e5a15d0fc1e32c990a029e920330f41b306516f1bcc0b5d44219d`.
Both Python files also compile.

Evidence: `evidence/stage2-translation.log`, exit 0.

### Independent differential test

`evidence/differential_test.py` independently imports the trusted canonical
entry point and the candidate entry point. It tested:

- the two documented examples;
- empty, singleton, immediate-negative, exactly-zero, and later-crossing cases;
- very large positive and negative integers;
- every list of length 0 through 5 over `[-3, -2, -1, 0, 1, 2, 3]`;
- 1,000 deterministic generated lists of lengths 0 through 30 and values in
  `[-10^9, 10^9]`.

After deduplication, all 20,583 cases returned the same value and type:
zero mismatches and zero non-Boolean candidate results.

Evidence:

- `evidence/differential-inputs.json` — the full test input corpus and scope.
- `evidence/differential-results.json` — per-case results.
- `evidence/stage2-differential.log` — exact command, summary, result SHA-256,
  and exit 0.

This is strong finite evidence for the implementation-to-canonical bridge, not
a substitute for the K proof.

## 3. Clean proof reconstruction

K version `v7.1.293` was used. Only source files copied into
`/tmp/audit-work/source` were used; no candidate `*-kompiled` directory, binary,
cache, or archive was reused.

### Fresh generated-semantics execution

The LLVM definition was freshly built with:

```text
kompile /tmp/audit-work/source/semantic.k --backend llvm --main-module SEMANTIC --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/proof/semantic-llvm-fresh
```

It exited 0 (`evidence/stage3-kompile-llvm.log`). The fresh definition then ran
the actual submitted `solution.mpy` on 13 normal and boundary inputs. These
cover empty and nonempty iteration, both conditional branches, early return,
post-loop return, exact-zero balance, later negative balance, and unbounded-size
integers. Every `krun` exited 0, terminated at `.K`, returned a `BoolV`, and
agreed with both Python implementations.

Evidence:

- `evidence/semantic_differential.py`
- `evidence/semantic-results.json`
- `evidence/stage3-semantic-execution-final.log`, 13 cases, zero mismatches,
  exit 0.

Two earlier preserved logs,
`stage3-semantic-execution.log` and
`stage3-semantic-execution-rerun.log`, show reviewer extractor failures: the
regular expression initially did not allow K's pretty-printed whitespace.
The underlying `krun` commands in those attempts all exited 0 and visibly
printed the right booleans. The corrected preserved script produced the final
passing comparison.

### Fresh positive proofs

The Haskell proof definition was freshly built with:

```text
kompile /tmp/audit-work/source/verification.k --backend haskell --main-module VERIFICATION --syntax-module MPY-SYNTAX --output-definition /tmp/audit-work/proof/verification-haskell-fresh
```

This exited 0 (`evidence/stage3-kompile-haskell.log`). Each target claim was
then run independently:

| Claim | Evidence | Exit | Output |
|---|---|---:|---|
| `SPEC.entry-reaches-loop` | `evidence/stage3-proof-entry.log` | 0 | `#Top` |
| `SPEC.loop-correct` | `evidence/stage3-proof-loop.log` | 0 | `#Top` |

Both required positive claims therefore satisfy the stated closure criterion.

## 4. Adequacy and real-program pinning

### Plain-language claims

`entry-reaches-loop` has no explicit `requires` clause. Its typed variable
`OPS` ranges over any `IntList`, while the other initial cells are fixed to
balance 0, current value 0, and `NoResult`. It says that the exact submitted
module executes its import, selected entry function, initial assignment, and
`for` iterable lookup, reaching the loop cut point with:

- the exact translated loop body;
- the entire `OPS` list still to process;
- the exact post-loop `Return(false)` continuation;
- balance 0 and no result.

`loop-correct` also has no explicit `requires`. It ranges over every
`B:Int`, `OPS:IntList`, original input, and current value, with `NoResult` and
the exact loop/control continuation. It says execution consumes that
continuation, resets the modeled local cells on function return, and puts
exactly `BoolV(belowZeroFrom(B, OPS))` in the result cell.

The first claim's right side is syntactically the second claim's left-side cut
point with `B = 0` (and the framed cells instantiated consistently).
Reachability transitivity therefore yields the whole-program statement:

```text
result = BoolV(belowZeroFrom(0, OPS))
```

for the exact translated module. The result is neither fresh nor
unconstrained, and there is no implication that weakens an equality into a
one-way property.

### Actual-program identity

The `Module(...)` term in `/candidate/spec.k:11` through line 20 contains every
constructor and literal in the trusted-regenerated `solution.mpy`. The
translator renders the empty `else` statement list as an empty list position;
the claim spells the same list identity as `.Stmts`. Fresh concrete execution
also parses and runs the submitted file directly. Thus the proof is attached to
the actual translated program, not a substitute body.

### Satisfiable states and concrete substitutions

Examples satisfying `entry-reaches-loop` include `OPS = .IntList`,
`OPS = cons(1, cons(-1, .IntList))`, and
`OPS = cons(1, cons(-2, .IntList))`. A state satisfying `loop-correct` is, for
example, `B = 0`, `OPS = .IntList`, current 0, any well-sorted original input,
and `NoResult`.

The candidate summary reduces on those complete-entry inputs to:

| Operations | `belowZeroFrom(0, OPS)` | Canonical Python | Candidate Python |
|---|---:|---:|---:|
| `[]` | `false` | `False` | `False` |
| `[1, -1]` | `false` | `False` | `False` |
| `[1, -2]` | `true` | `True` | `True` |

`evidence/summary-ground.k` checks the three summary reductions in
configuration claims; the corrected run prints `#Top` and exits 0 in
`evidence/stage4-summary-ground-rerun.log`. The earlier
`stage4-summary-ground.log` records a reviewer attempt to use bare functional
claims, which this backend explicitly does not support; the configuration form
removes that tooling limitation.

`evidence/full-program-ground.k` separately executes the complete embedded
module for the same three cases. It prints `#Top` and exits 0 in
`evidence/stage4-ground-whole-program.log`. The Python values also appear in
the independent differential and semantic-execution evidence.

Every helper/loop claim consequently matches a reachable real control point,
and the two claims compose without a state mismatch.

## 5. Rule-by-rule static soundness review

### Local syntax and configuration inventory

`semantic.k` declares:

| Lines | Declaration and alternatives | Use |
|---|---|---|
| 6 | `Program ::= Module(Stmts)` | Exact translated module root |
| 7 | `Stmts ::= List{Stmt, ""}` | Ordered statement sequence |
| 8 | `Params ::= Params(Strings)` | Function parameter list |
| 9 | `Strings ::= List{String, ","}` | Import/parameter names |
| 11–17 | `Stmt ::= ImportFrom \| FuncDef \| Assign \| AugAssign \| For \| If \| Return` | Every submitted statement constructor |
| 19–22 | `Expr ::= Name \| Int \| Bool \| Compare` | Every submitted expression constructor |
| 23 | `CmpOp ::= CmpOp(String, Expr)` | One comparison link |
| 24 | `CmpOps ::= List{CmpOp, ","}` | Translator-preserved comparison chain syntax |
| 26–27 | `IntList ::= .IntList \| cons(Int, IntList)` | Finite list input model |
| 28–30 | `PyVal ::= IntV \| BoolV \| ListV` | Runtime values used by the target |
| 31 | `Result ::= NoResult \| PyVal` | Observable call result |
| 46–50 | `KItem ::= execStmts \| setBalance \| branch \| loop \| doReturn` | Internal control frames |

`verification.k:9` adds
`belowZeroFrom(Int, IntList):Bool [function, total]`.
There are no local `functional`, `opaque`, priority, `owise`,
`simplification`, or `concrete` declarations.

The configuration at `semantic.k:37` has exactly the needed state:
`<k>`, immutable `<input>`, local `<balance>`, local/current iteration value
`<current>`, and observable `<result>`. There is no unused heap, allocation,
I/O, exception, or call-stack cell.

The submitted term uses every one of these source constructors:
`Module`, `ImportFrom`, `FuncDef`, `Params`, `Assign`, `Name`, `Int`, `For`,
`AugAssign`, `If`, `Compare`, `CmpOp`, `Return`, and `Bool`. Each is declared
above and covered by the operational rules below. `Strings`, `Stmts`, and
`CmpOps` are the corresponding list sorts.

### Operational rule inventory

There are 22 local semantic rules. Each decision below is relative to the
selected minimal semantics and the one submitted program.

| Line | Rule | Soundness decision |
|---:|---|---|
| 52 | `Module(SS) => execStmts(SS)` | Sound root-to-statement scheduling for the entry-call harness. |
| 54 | `execStmts(.Stmts) => .K` | Sound empty-sequence identity. |
| 55 | `execStmts(S SS) => S ~> execStmts(SS)` | Sound left-to-right statement order. |
| 58 | `ImportFrom(_, _) => .K` | Sound for the fixed, unused `typing.List` import. It is over-broad for arbitrary side-effecting imports outside this theorem. |
| 62–63 | Exact `below_zero(operations)` `FuncDef` to `execStmts(BODY)` | Sound as the explicitly documented entry invocation. It does not claim general Python module-definition behavior. |
| 65 | Balance assignment schedules `E` before `setBalance` | Preserves target evaluation order. |
| 66–67 | `IntV(I) ~> setBalance` writes balance | Sound for target `balance = 0`; non-integer assignment remains visibly unmodeled. |
| 69–71 | Exact balance `+= operation` | Sound direct bridge for two pure dedicated-cell lookups and K integer addition; updates only balance. |
| 73 | Exact `for operation in E` schedules `E` once before `loop(BODY)` | Preserves target iterable evaluation order. |
| 74 | Empty list ends the loop | Sound zero-iteration behavior. |
| 75–77 | `cons(I, IS)` writes current, runs body, then loops on `IS` | Sound ordered iteration and state update; body precedes recursion. |
| 79 | `If(E, THEN, ELSE)` evaluates `E` before `branch` | Sound target conditional order. |
| 80 | True branch executes `THEN` | Sound and disjoint from line 81. |
| 81 | False branch executes `ELSE` | Sound and disjoint from line 80. |
| 83 | `Return(E)` evaluates `E` before `doReturn` | Sound return-expression order. |
| 84–87 | A returned `PyVal` discards the remaining function continuation, clears modeled locals, and writes the result | Sound for this single active entry frame. Its arbitrary-suffix pattern is not evidence for nested calls or `finally`, neither of which is admitted or used here. |
| 89 | `Int(I) => IntV(I)` | Exact arbitrary-precision integer literal bridge. |
| 90 | `Bool(B) => BoolV(B)` | Exact Boolean literal bridge. |
| 91–92 | `Name("operations")` reads input | Correct exact parameter binding for this entry harness. |
| 93–94 | `Name("operation")` reads current | Correct after line 75 sets the loop target. Reading it outside that control path would not model Python's unbound-local error, a scope outside this fixed program execution. |
| 95–96 | `Name("balance")` reads balance | Correct after the initial assignment. |
| 100–102 | Exact one-link `balance < 0` comparison | Truthful direct bridge: both operands are pure, binding is pinned, `<Int` matches Python integer ordering, and the continuation is preserved. |

No operational rule fabricates the requested Boolean from an oracle or calls
`belowZeroFrom`. The proof-side summary is absent from `semantic.k`. Rules
that directly implement augmented addition or comparison replace only pure
lookups whose bindings and cells are explicit.

The rules have no harmful overlaps: empty/nonempty statement lists,
empty/nonempty integer lists, true/false branches, distinct literal
constructors, and the three distinct name strings are disjoint. There are no
priority interactions. Input is read-only; loop steps update current and
balance in program order; only return writes result and unwinds control.

`evidence/body_sensitivity.py` changes the supported initial literal from 0 to
1 and is translated by the trusted translator. On input `[-1]`, the original
term concretely returns `true`, while the changed term returns `false` under
the same fresh semantics. The exact commands and configurations are in
`evidence/stage5-body-sensitivity.log`, exit 0. This demonstrates that the
language rules execute the body and are not an answer-only shortcut.

### Proof-local function inventory

`verification.k` has one function and exactly two equations:

| Lines | Equation | Decision |
|---|---|---|
| 11 | `belowZeroFrom(_, .IntList) => false` | Correct: there is no remaining nonempty prefix to test. |
| 12–16 | On `cons(I, IS)`, return true if `B + I < 0`, else recurse from `B + I` over `IS` | Correct structural recurrence for negative nonempty running prefixes. |

The two constructor guards are disjoint and exhaustive over `IntList`.
Recursion strictly descends to `IS`, so `[total]` is justified. There is no
equation overlap, opaque value, proof-local rewrite of program control, or
unproved result oracle. The universal `loop-correct` reachability claim is the
connection theorem from fixed operational execution to this result-bearing
summary; the summary is not used to replace execution.

`evidence/stage5-static-inventory.log` records the extracted declarations,
attributes, rules, and claims. No rule is labeled materially unsound, so no
false-conclusion witness is asserted. The narrower reuse gaps for arbitrary
imports, unsupported call contexts, and out-of-order dedicated-variable reads
are explicitly excluded from the theorem and motivate the `CONCERNS` level.

## 6. Fresh non-vacuity test

`evidence/spec-vacuity.k` is reviewer-authored. It preserves the exact
loop/control obligation but changes the result to the false constant
`BoolV(true)`. A satisfying counterexample is:

```text
B = 0
OPS = .IntList
result initially NoResult
```

The real continuation executes `Return(false)`, so the mutated destination is
false for that reachable state.

The mutation first built successfully:

```text
kprove /tmp/audit-work/source/spec-vacuity.k --definition /tmp/audit-work/proof/verification-haskell-fresh --spec-module SPEC-VACUITY --dry-run
```

This exited 0 (`evidence/stage6-mutation-build.log`). The actual proof command,
recorded in `evidence/stage6-mutation-proof.log`, exited 1 with
`WarnStuckClaimState`. Its residual has `OPS #Equals .IntList`, `.K`, and
`<result> BoolV(false) </result>`, which does not unify with the mutated
`BoolV(true)` destination. The failure is therefore the expected reachable
unmet result obligation, not a parser error, missing import, timeout, or
unreachable mutation.

## 7. Proven versus assumed accounting

### What is machine-checked

Under the audited generated semantics and K built-ins:

1. the exact translated module reaches its exact loop cut point for every
   finite `IntList`;
2. from that cut point, for every K integer starting balance and every finite
   remaining list, execution returns exactly the recursive
   `belowZeroFrom` Boolean;
3. by exact cut-point composition, the submitted entry program returns
   `belowZeroFrom(0, OPS)`;
4. the proof rejects a reachable false result obligation.

This is at least the requested partial-correctness result. The theorem domain is
finite lists of mathematical integers. It does not cover Python inputs that
violate the `List[int]` contract, integer subclasses with overloaded behavior,
arbitrary imports, nested calls, exceptions, or other unused Python constructs.

### Trust ledger

| Boundary | Influence and dependents | Assessment/evidence |
|---|---|---|
| K parser, compiler, Haskell/LLVM backends, reachability logic, cells, K sequences, and constructor lists | All builds, execution, and proofs | Standard toolchain trust boundary; version and fresh commands recorded. |
| Built-in `INT`, `BOOL`, `STRING`, `K-EQUAL`, `+Int`, `<Int`, and `#if` | Arithmetic, comparison, helper result, both claims | Acceptable low-level primitives, not task-answer oracles. |
| Trusted `/reference/py2mpy.py` | Source-to-term identity | Mandated trusted input; fresh output is byte-identical to the submitted term. |
| `IntList` as a finite Python `List[int]` and K `Int` as Python's ordinary arbitrary-precision integer value | Language-model adequacy and all inputs | Appropriate for the stated intended domain; concrete boundary tests include huge integers. |
| Generated task-specific entry harness | Connection from the translated module to an invocation of `below_zero(operations)` | Audited rule by rule and body-sensitive; intentionally not a reusable whole-Python semantics. |
| Structural reading of `belowZeroFrom(0, OPS)` as “some nonempty running prefix sum is negative” | Natural-language intent | Informal induction: empty is false; at each head test the new prefix, otherwise recurse from the new balance. Direct and convincing, but not a separately formalized prefix-list theorem. |
| Trusted canonical Python implementation | Intent oracle for testing only | 20,583 zero-mismatch differential cases; not used to close the K proof. |
| CPython execution and 13 K concrete runs | Empirical source/semantics bridge | Supports the tested cases only; not substituted for the universal K claim. |

There are no opaque symbols, fresh result-bearing values, external calls, or
empirical equations contributing to claim closure. `belowZeroFrom` is not
assumed: its equations define it, and `loop-correct` universally connects real
loop execution to it.

### Gate summary

- Real-program soundness: **PASS**. Exact body, state, control, universal
  connection claim, satisfiable states, body sensitivity, and false-result
  rejection are established.
- Intent adequacy: **PASS with documented limitation**. The intended
  `List[int]` behavior and zero boundary align, while the last
  recurrence-to-English bridge is informal and the semantics is intentionally
  task-specific.
- Trust/evidence auditability: **PASS**. Exact commands, statuses, bounded logs,
  scripts, complete differential inputs/results, and trust boundaries are
  preserved under `/audit-output/evidence/`.

The limitations do not permit a false conclusion for the submitted program on
the intended domain, so the proof remains legitimate.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
