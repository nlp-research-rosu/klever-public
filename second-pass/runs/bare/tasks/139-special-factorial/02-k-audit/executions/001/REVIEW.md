# Adversarial proof audit: 139-special-factorial

The candidate contains a legitimate, result-constraining K reachability proof
of the exact submitted `solution.mpy` under its generated semantics. Fresh
reconstruction closes all three positive claims, and a fresh false
postcondition is rejected. The principal limitation is the bridge from that
minimal, unbounded-stack semantics to CPython: the submitted recursive
`solution.py` raises `RecursionError` at the in-domain input `n = 1000`, while
the iterative trusted canonical implementation returns the requested integer.
That is an adequacy concern, not a semantic rule that makes a false K conclusion
provable.

## 1. Input and provenance integrity

### Semantics-mode boundary

The rendered mode is `GENERATED_SEMANTICS`, and
`/reference/reference-semantics` is absent. The trusted mounts therefore do not
contradict the mode. No hidden or inferred reference semantics was used.

The candidate's top-level source artifacts are regular files. A recursive
`find -P` found no symlink anywhere below `/candidate`. All generation
deliverables needed by this audit are present: `solution.py`, `solution.mpy`,
`semantic.k`, `verification.k`, `spec.k`, and `prove.sh`. The candidate also
contains generated LLVM/Haskell definitions, logs, and a concrete-output file.
Those extra build products are untrusted evidence, were not copied into the
scratch source set, and were never used as definitions or caches.

The candidate prompt and translator are byte-identical to the trusted mounts:

| Artifact | Trusted SHA-256 | Candidate comparison |
|---|---|---|
| `prompt.py` | `be0a59f5cf0d2c13ca98ace59ca3a5bf4b8c4a153d42450c7cf6abb87d22d0c8` | byte-identical |
| `py2mpy.py` | `406485eac118431c08ef59f30f79dfa6aa9d5825408917fc5ce7c806e664db16` | byte-identical |

The complete type/hash/cmp record is
[stage1-integrity.log](/audit-output/evidence/stage1-integrity.log).

I read `run-input.json`, `metrics.json`, `codex-last.txt`,
`codex-output.log`, and the structured generation trace only as claims. In
particular, `codex-last.txt` claims that `prove.sh` exited zero and all three
proofs printed `#Top`; none of that was accepted without reconstruction. The
404-line JSONL trace parses completely, and its final message repeats the same
claim. See
[stage1-structured-trace-summary.log](/audit-output/evidence/stage1-structured-trace-summary.log)
and the bounded marker extraction in
[stage1-untrusted-claims.log](/audit-output/evidence/stage1-untrusted-claims.log).
The latter also records that `jq` was unavailable; the complete trace was
subsequently validated with the reviewer-authored Python parser, so this caused
no audit uncertainty.

No required source artifact is missing, changed, mistyped, or symlinked.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt specifies an integer `n > 0` and requires

`n! * (n-1)! * ... * 1!`.

The trusted canonical function maintains `fact_i = i!` and multiplies each
successive `fact_i` into `special_fact`; thus it returns exactly that product.
The relevant trusted sources are
[prompt.py](/reference/prompt.py:2) and
[canonical.py](/reference/canonical.py:18).

The submitted implementation uses two recurrences:

- `factorial(n) = 1` for `n <= 1`, otherwise
  `n * factorial(n-1)`;
- `special_factorial(n) = 1` for `n <= 1`, otherwise
  `factorial(n) * special_factorial(n-1)`.

For positive mathematical integers, those recurrences equal the required
product. The implementation is in
[solution.py](/candidate/solution.py:1).

### Trusted regeneration

In clean scratch, the exact command

```text
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
```

exited zero. Both the regenerated file and submitted `solution.mpy` have
SHA-256
`1d37d11e67fc48c6f8572fec6701a168293fee886e4499acc9ca78a6f0fa1cc0`,
and `cmp` exited zero. See
[stage2-regeneration.log](/audit-output/evidence/stage2-regeneration.log).

### Independent differential testing

The reviewer-authored
[differential_test.py](/audit-output/evidence/differential_test.py)
loads the trusted canonical entry point and scratch-copied candidate entry point
with separate import modules. Its inputs cover:

- the documented example `4`;
- out-of-contract empty-product probes `-1, 0`;
- both sides of the `<= 1` branch at `1, 2`;
- every positive input `1..25`;
- 32 deterministic generated values in `1..40`;
- helper boundaries `0, 1, 2, 5`;
- the positive resource-boundary witness `1000`.

The run had 67 cases and one mismatch. All ordinary, branch, example, and
generated cases matched. At `n = 1000`, the canonical implementation returned
an integer with 3,910,725 bits, while `solution.py` raised `RecursionError`
under Python 3.10.12's recursion limit of 1000. The test intentionally exits
one on any mismatch. Exact inputs, value fingerprints, command, and status are
in
[stage2-differential.log](/audit-output/evidence/stage2-differential.log).

This mismatch is not a different mathematical recurrence. It shows that the
candidate rewrite is not operationally equivalent to the iterative canonical
function for every positive CPython input. Because the requested theorem is
partial correctness and the generated K language deliberately uses an
unbounded algebraic call stack, I treat this as an explicit implementation/model
adequacy limitation rather than a false proof rule.

## 3. Clean proof reconstruction

Only regular source files were copied to
`/tmp/audit-work/139-special-factorial`. No candidate `*-kompiled` directory,
binary, parser output, cache, or timestamp was copied or referenced.
Post-run `cmp` checks confirm that every positive-build source still matches
the candidate byte-for-byte and that the scratch translator still matches the
trusted mount; see
[stage3-scratch-source-integrity.log](/audit-output/evidence/stage3-scratch-source-integrity.log).

### Fresh definitions

These exact builds succeeded:

```text
kompile semantic.k --backend llvm --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-llvm-kompiled

kompile semantic.k --backend haskell --main-module MPY \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-semantic-haskell-kompiled
```

Both exited zero. The only diagnostics are deprecation warnings for `=> .` at
the two empty-statement rules; they do not change meaning. Full records:
[stage3-build-llvm.log](/audit-output/evidence/stage3-build-llvm.log) and
[stage3-build-haskell.log](/audit-output/evidence/stage3-build-haskell.log).

### Fresh generated-semantics execution

The reviewer-authored
[concrete_semantics_compare.py](/audit-output/evidence/concrete_semantics_compare.py)
ran the freshly translated `solution.mpy` through the fresh LLVM definition for
`n = -1, 0, 1, 2, 4, 6`. Every `krun` exited zero and returned the same integer
as both Python implementations: respectively `1, 1, 1, 2, 288, 24883200`.
The negative and zero values are boundary probes, not additions to the formal
domain. Commands, complete configurations, and comparisons are in
[stage3-concrete-semantics.log](/audit-output/evidence/stage3-concrete-semantics.log).

### Fresh positive proofs

Each target was run independently against the fresh Haskell definition:

| Target | Modular proof use | Exit | Output |
|---|---|---:|---|
| `SPEC.factorial-call` | no trusted claim | 0 | `#Top` |
| `SPEC.special-factorial-call` | previously proved `factorial-call` reused with `--trusted` | 0 | `#Top` |
| `SPEC.program-correct` | both previously proved call claims reused with `--trusted` | 0 | `#Top` |

The exact commands and complete outputs are
[stage3-proof-factorial.log](/audit-output/evidence/stage3-proof-factorial.log),
[stage3-proof-special-factorial.log](/audit-output/evidence/stage3-proof-special-factorial.log),
and
[stage3-proof-program.log](/audit-output/evidence/stage3-proof-program.log).
The `--trusted` uses are modular lemma reuse, not unproved assumptions: the
same exact universal claims were closed in the preceding fresh runs.

## 4. Adequacy and real-program pinning

### Plain-language claim meanings

1. `factorial-call`: for every positive `N`, in the exact submitted function
   map, evaluating `factorial(n)` when the caller binds `n` to `N` reaches the
   tagged return event `factorialSpec(N)`. It preserves the arbitrary caller
   continuation, caller environment remainder, call stack, and result cell.
2. `special-factorial-call`: under the analogous positive-input state,
   evaluating `special_factorial(n)` reaches a tagged return of
   `specialFactorialSpec(N)`, with the same caller-state preservation.
3. `program-correct`: for every positive `N`, initializing the exact submitted
   module with empty functions, environment, stack, and result loads the two
   submitted functions, executes the designated entry point, empties the
   computation and call stack, restores the empty environment, and places
   `specialFactorialSpec(N)` in the result cell.

The claims are in [spec.k](/candidate/spec.k:6).

### Exact program identity

I independently parsed and macro-expanded both submitted `solution.mpy` and
the proof's `solutionProgram` symbol with the fresh Haskell definition. The two
KORE terms are byte-identical and have SHA-256
`4bcf273c99d4c84b19f621c546d509be683c5e422eb5c6df6f525a025dd7513a`.
Both `kast` commands and `cmp` exited zero. See
[stage4-program-pinning.log](/audit-output/evidence/stage4-program-pinning.log).

The helper claims match actual control flow:

- the factorial body saves the current `n`, decrements the local `n`, makes
  the recursive call, and multiplies by the saved value, exactly matching the
  recurrence in `factorialSpec`;
- the special-factorial body first calls the submitted factorial function,
  decrements local `n`, recursively calls itself, and multiplies the two
  returned values, exactly matching `specialFactorialSpec`;
- the `returned(F,V,KONT)` observation in each helper claim is the event
  generated by popping the corresponding `frame(F,ENV,KONT)`. It is not a
  free or opaque value.

There are no loop claims. The two recursive helper claims are the real
recursive control summaries.

### Satisfiable preconditions and concrete substitutions

Concrete witness states exist:

- for each helper, choose `N = 1`, the exact `solutionFunctions` map,
  environment `"n" |-> 1`, empty caller stack, `noResult`, and any concrete
  continuation such as `finish`;
- for `program-correct`, choose `N = 1` in the declared initial
  configuration.

These are ordinary ground K maps/stacks and satisfy every stated side
condition. Moreover, the concrete `N = 2` program reaches recursive call
contexts covered by both helper claims.

Ground substitution gives:

| `N` | Claimed special result | Fresh K | Canonical Python | Candidate Python |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 |
| 4 | 288 | 288 | 288 | 288 |
| 6 | 24883200 | 24883200 | 24883200 | 24883200 |

The complete machine record is the concrete-semantics log cited in Stage 3.
The returned value is therefore constrained by a recursive mathematical
function and actual execution; it is neither a free variable, tautology, nor
one-way implication.

## 5. Rule-by-rule static soundness review

The exhaustive local-source extraction is in
[stage5-source-inventory.log](/audit-output/evidence/stage5-source-inventory.log).
There are no generated helper K files beyond `semantic.k`, `verification.k`,
and `spec.k`.

### Local syntax and configuration inventory

`MPY-SYNTAX` declares:

- `Pgm`: `Module(Stmts)`;
- `Stmts`: a list of `Stmt`;
- `Stmt`: `FuncDef`, `Return`, `If`, and `Assign`;
- one-string `Params`;
- `Expr`: `Int`, `Name`, `BinOp`, `Compare`, and `Call`;
- `CmpOp(op,right)`;
- stored `function(parameter,body)`.

`MPY` additionally declares:

- `Result`: `noResult` or `result(Int)`;
- `Frame`: function tag, saved caller map, and saved K continuation;
- algebraic `CallStack`: empty or `push(Frame,CallStack)`;
- internal K items `init`, `load`, `start`, `eval`, `exec`, `execStmt`,
  `binLeft`, `binRight`, `cmpLeft`, `cmpRight`, `branch`, `enter`, `assign`,
  `continueInt`, `continueBool`, `returned`, `returning`, and `finish`.

The configuration has exactly the state used by the submitted program:
`<k>`, function map, local environment map, call stack, and result. There is no
heap, I/O, exception, object, or allocation cell.

Every constructor in `solution.mpy` is covered:
`Module`, `FuncDef`, `Params`, `If`, `Compare`, `Name`, `CmpOp`, `Int`,
`Return`, `Assign`, `BinOp("-")`, `BinOp("*")`, and direct-name `Call`.
The grammar admits some unused forms more broadly (arbitrary operator strings,
arbitrary assignment expressions, and arbitrary call expressions), but
unsupported cases have no fallback rule and visibly stick; no rule fabricates
a value for them.

### The 26 operational rules in `semantic.k`

| Lines | Rule inventory and judgment |
|---|---|
| 70 | `init(Module(SS),N)` sequences `load(SS)` then `start(N)`. Sound as the explicit task harness. |
| 72 | Empty `load` terminates. Sound. |
| 73-75 | Loading a `FuncDef` updates the function map and continues in source order. This gives later definitions the expected overwrite behavior. |
| 77-78 | `start(N)` calls the designated submitted entry point and then `finish`. This is task-specific harnessing, not an encoded result. |
| 80 | Empty statement execution terminates. Sound. |
| 81 | Nonempty statement execution is left-to-right. Sound. |
| 83 | `If` evaluates its guard before branching. Sound. |
| 84-86 | True Boolean guard executes the then-list. Sound and disjoint from the next rule. |
| 87-89 | False Boolean guard executes the else-list. `B` versus `notBool B` is exhaustive and disjoint for `Bool`. |
| 91 | `Return(E)` evaluates `E` and installs the return marker. Sound. |
| 92 | Name assignment evaluates the RHS first. Sound for every assignment used by the program. |
| 93-94 | Assignment updates the current local environment and resumes its exact continuation. Sound. |
| 96 | Integer literal yields its integer. Sound. |
| 97-98 | Name lookup obtains the mapped integer or sticks if absent. Sound; no default value is invented. |
| 100-101 | Binary operation evaluates its left operand first. Sound. |
| 102-103 | After the left value, the right operand is evaluated and the saved left value is retained. Sound. |
| 104-105 | Multiplication returns left times right. Sound over K mathematical integers. |
| 106-107 | Subtraction returns left minus right. Sound over K mathematical integers. |
| 109-110 | Comparison evaluates its left operand first. Sound. |
| 111-112 | `<=` then evaluates its right operand while saving the left integer. Sound. |
| 113-114 | `<=` returns the Boolean `left <= right`. Sound. |
| 116 | A direct-name call evaluates its sole argument before entry. This is exactly the only call shape submitted. |
| 117-120 | Function entry selects the named body, installs a one-parameter local map, and saves function tag, caller map, exact continuation, and stack. Sound for the used non-closure, one-argument functions. |
| 122-124 | A computed return discards the remainder of the current function, restores the saved caller environment, pops exactly one frame, and emits the tagged returned value. This implements Python return control and preserves the computed value. |
| 126 | The tagged return resumes the saved continuation with that same value. Sound. |
| 128-129 | `finish` can set the observable result only from `noResult`, and uses the computed entry return unchanged. Sound. |

These rules preserve left-to-right evaluation, parameter binding, local
mutation, recursive frame nesting, return unwinding, and the only observable
result. There are no priorities or overlapping operational rules with
different right-hand sides. Internal `returning` is intentionally allowed to
discard an arbitrary remaining statement suffix because Python `return` exits
the current function; the top saved frame fixes the caller continuation and
state.

The model is deliberately narrower than general Python. In particular, direct
calls consult the function map rather than modeling arbitrary local shadowing,
and normal `None` fallthrough is absent. Neither behavior is exercised:
`solution.py` never binds a function name locally, and all reachable branches
of both functions return. These are coverage limitations, not false conclusions
on the intended program/domain.

### The six rules and declarations in `verification.k`

`factorialSpec` and `specialFactorialSpec` are the only local K functions. Both
are declared `[function,total]`; there is no separate `[functional]` or opaque
declaration.

| Lines | Rule inventory and judgment |
|---|---|
| 10-11 | `factorialSpec(N) = 1` for `N <= 1`. Mathematically true for the stated extension and includes the positive base `N=1`. |
| 12-13 | `factorialSpec(N) = N * factorialSpec(N-1)` for `N > 1`. The recursive argument strictly decreases to the base. |
| 15-16 | `specialFactorialSpec(N) = 1` for `N <= 1`. Mathematically true for the stated extension and positive base. |
| 17-19 | `specialFactorialSpec(N) = factorialSpec(N) * specialFactorialSpec(N-1)` for `N > 1`. The recursive argument strictly decreases. |
| 22-39 | `solutionFunctions` macro expands to exactly the two submitted stored functions. It does not rewrite execution or produce a result. |
| 42-60 | `solutionProgram` macro expands to exactly the submitted module; fresh KORE comparison proves source identity. |

For each total function, the guards `N <= 1` and `N > 1` are disjoint and
exhaustive over K `Int`; there is no overlap disagreement or uncovered
totalization case. The recursive equations descend for every recursive case.
The special recurrence uses the independently constrained factorial recurrence,
not an opaque symbol.

There are no local priority rules, simplification rules, `owise` rules, opaque
symbols, fresh values, or operational bridges from program syntax directly to
the specification functions. The `[symbol(...)]` annotations give stable K
labels; they do not make values opaque.

### Claim/static proof-extension inventory

The three reachability claims are derived execution summaries, not ordinary
semantic rewrites. Their complete domains include the exact function map,
positive guard, caller environment binding, arbitrary saved caller state, and
explicit continuation. Their right sides retain every observable cell and use
the precise `returned` event generated by the operational rules.

The factorial claim is proved without trusted claims. The special claim's use
of the factorial claim is contained in the latter's universal context. The
program claim reuses both previously proved call claims over matching exact
contexts. No helper body is replaced by an unconstrained oracle, and no claim
pins only a textual function name while ignoring the function map.

I found no materially unsound local rule. Accordingly, there is no false-rule
witness to report. The narrower evidence/model gaps are the explicitly
task-specific `start` harness, direct-name/single-argument language subset, and
absence of CPython resource exceptions; none permits a wrong integer result for
the submitted AST in the modeled positive domain.

## 6. Fresh non-vacuity test

The fresh reviewer mutation is
[spec-vacuity.k](/audit-output/evidence/spec-vacuity.k). It changes only the
entry result obligation from

`result(specialFactorialSpec(N))`

to

`result(specialFactorialSpec(N) +Int 1)`.

This is demonstrably false for the satisfying input `N = 1`: actual execution
returns `1`, while the mutation requires `2`.

The mutation's `kprove --dry-run` exited zero, showing that it parsed and built
against the fresh definition. See
[stage6-mutation-dry-run.log](/audit-output/evidence/stage6-mutation-dry-run.log).
The actual proof exited one with `WarnStuckClaimState`, not a parser error,
timeout, missing import, or unrelated crash. Its residual has a completed
configuration with `result(1)` under the satisfiable constraints
`N <= 1` and `N > 0`; that is the expected unmet result obligation. See
[stage6-mutation-proof.log](/audit-output/evidence/stage6-mutation-proof.log).

The positive theorem is therefore non-vacuous and discriminates an incorrect
result.

## 7. Proven versus assumed accounting

### What the successful proof establishes

Under the local MPY semantics and K's built-in mathematical integer, Boolean,
map, and reachability machinery, the exact submitted `solution.mpy` has the
following partial-correctness property:

For every mathematical integer `N > 0`, execution from the declared empty
initial state reaches a completed state whose result is
`specialFactorialSpec(N)`, with the two exact functions loaded, empty local
environment, and empty call stack. The two universal call claims additionally
establish exact recursive results and caller-state restoration for arbitrary
matching continuations, stacks, environments, and result cells.

The equations define `factorialSpec(N)` as ordinary factorial on positive
integers and define `specialFactorialSpec(N)` as the product of those factorials
from `N` down to `1`. Thus the K result matches the mathematical contract,
subject to the trust and adequacy boundaries below.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293 parser, compiler, Haskell/LLVM backends, and circularity implementation | All builds, execution, and reachability closure | Necessary low-level proof-tool trust; fresh dual-backend reconstruction and false-mutation behavior support it. Versions are recorded in [toolchain-versions.log](/audit-output/evidence/toolchain-versions.log). |
| Built-in K `Int`, `Bool`, `Map`, and K-sequence operations | Arithmetic result, guards, environments, continuations | Acceptable fixed primitives. They are standard mathematical/unbounded abstractions, not task-answer rules. |
| Trusted `/reference/py2mpy.py` | Bridge from `solution.py` to submitted AST | Acceptable mounted translator boundary; fresh output is byte-identical. |
| Candidate-generated MPY operational rules | Meaning of every submitted AST construct | Not merely assumed: exhaustively audited and concretely tested on normal/boundary cases. They remain a generated model rather than a full Python semantics. |
| `factorialSpec` and `specialFactorialSpec` equations | Every helper and final result | Truthful, total, disjoint, terminating mathematical definitions; no opaque interpretation. |
| Modular `--trusted` helper claims | Closure of later special/program claims | Acceptable theorem reuse because each exact universal helper claim first closed independently with exit zero and `#Top`. |
| Recurrence-to-English product equivalence | Natural-language intent | Ordinary informal induction: base product is 1 and each step multiplies by `N!`. It is not a separate K theorem, so it is an explicit informal intent bridge. |
| Generated semantics versus CPython runtime | Whether modeled execution covers actual resource exceptions | Concerning limitation. The K stack is unbounded and has no `RecursionError`; the differential witness `n=1000` shows actual CPython divergence from the iterative canonical implementation. |

There are no opaque symbols, empirical result oracles, hidden reference
semantics, or proof rules that directly inject the requested answer.
Differential and concrete testing support only the tested execution bridge;
they are not used as substitutes for the universal K proof.

### Decision

Gate A (real-program soundness and non-vacuity) passes under the generated MPY
semantics. Gate B has a documented runtime-adequacy limitation: actual CPython
can raise `RecursionError` on positive inputs that the unbounded K model
executes mathematically. Gate C is auditable: all fresh commands, statuses,
bounded outputs, scripts, source comparisons, and the negative mutation are
preserved under `/audit-output/evidence/`.

The proof is therefore legitimate but carries concerns rather than qualifying
for an unqualified pass.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
