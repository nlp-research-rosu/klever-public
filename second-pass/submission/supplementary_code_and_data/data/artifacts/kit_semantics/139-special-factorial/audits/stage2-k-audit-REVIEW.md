# Independent adversarial audit: 139-special-factorial

## Outcome

The candidate contains a legitimate partial-correctness proof of the submitted
program for the full source-contract domain: every K integer `N >= 1`. I rebuilt
both definitions from source, proved the complete target module with a fresh
Haskell definition, mechanically pinned the entry claim to the trusted
regeneration of `solution.mpy`, audited every source declaration and rule, and
rejected a fresh false result mutation. No candidate-provided compiled
definition, log, trace, or proof report was used as proof authority.

The only assumptions are the normal toolchain trust boundary, the supplied MPY
semantics for the small reachable integer/control fragment, the trusted
translator, and a transparent mathematical induction from the accumulator
recurrence to the product of factorials. None is a proof-local oracle or an
execution bypass.

## 1. Input and provenance integrity

### Launcher record and campaign

`/audit-input.json` declares:

- `record_layout = pipeline-v3`
- `semantics_mode = SUPPLIED_SEMANTICS`
- problem `139-special-factorial`
- condition `kit-semantics`

I read every pipeline-v3 record required by the prompt: `/run.json`,
`/task.json`, `/generation-result.json`,
`/generation-evidence/invocation.json`, `metrics.json`,
`runtime-metrics.json`, `usage.json`, `codex-last.txt`, `codex-output.log`,
`prompt.txt`, and the complete structured trace. The JSONL trace has 445 valid
records: 315 response items, 127 event messages, and one each of session
metadata, turn context, and world state. A bounded semantic extraction records
all 16 agent messages and all 96 tool calls. These records were treated only as
untrusted construction history.

The `audit_campaign` object is exactly equal to
`/audit-campaign-lock.json`. The lock's independently computed SHA-256 is
`ad5dfcc006af70c4d0d2c6641f0878a6c54a266e9ad2b54cd225b2381a78d745`,
which equals the value recorded in `/audit-input.json`.

All direct recorded hashes match the mounted files, including the run, task,
result, invocation, prompt, canonical, translator, generation logs, metrics,
usage, and trace. Independently recomputed canonical tree digests also match
the stage result's candidate-workspace digest, the task/reference-semantics
manifest digest, and `usage.json`'s source-trace digest. Every
generation-result evidence hash also matches. The
`manifest` object embedded in `/audit-input.json` adds the synthesized `config`
field; after removing that one launcher-added field, it exactly equals
`/task.json`. The raw task-file hash matches its recorded hash.

Evidence:

- `evidence/01_provenance.py`
- `evidence/01_provenance_final.log` (command exit `0`)
- `evidence/01_trace_summary.py`
- `evidence/01_trace_summary.log` (command exit `0`)
- `evidence/01_provenance.log` (initial scan; its `file` utility probe was
  unavailable, but all required checks completed and the wrapper exited `0`)

### Trusted/candidate input comparison

The trusted `/reference/reference-semantics` tree is present, as required for
`SUPPLIED_SEMANTICS`. A recursive no-dereference comparison against
`/candidate/reference-semantics` exits `0`. The trees have identical entries
and bytes; there are no missing, additional, mistyped, symlinked, or special
entries. The candidate prompt and translator are byte-identical to
`/reference/prompt.py` and `/reference/py2mpy.py`.

The six required candidate proof artifacts are ordinary regular files:
`solution.py`, `solution.mpy`, `verification.k`, `spec.k`, `prove.sh`, and
`PROOF.md`. The entire candidate tree has no symlinks or special entries.
Candidate-built `runtime-kompiled` and `verification-kompiled` were ignored.
There is no infrastructure breach.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract and implementation

The trusted prompt defines, for a positive integer `n`, the Brazilian/special
factorial

```text
n! * (n-1)! * ... * 1!
```

and gives `special_factorial(4) == 288`. The trusted canonical program maintains
an ordinary factorial accumulator and multiplies it into a second accumulator
for `i = 1..n`.

The candidate uses the same recurrence in a `while` loop:

```python
factorial = factorial * i
result = result * factorial
i = i + 1
```

It is a different surface loop form but the same algorithm. The loop executes
once at `n=1`, repeatedly for larger positive integers, and never executes for
nonpositive inputs.

### Trusted regeneration

In `/tmp/audit-work/reconstruction`, I ran:

```bash
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
cmp -s solution.mpy regenerated-solution.mpy
```

Both commands exit `0`. Submitted and regenerated `.mpy` files have the same
SHA-256,
`0c3b214dd2e101f2b7f6c6d881c50335503145f96fbfd1858f5b130d452a78c3`.

### Independent differential test

`evidence/02_differential.py` independently imports the trusted canonical and
the scratch-copied generated implementation. It checks:

- out-of-domain no-iteration cases `-3, -1, 0`;
- the positive boundary and first branch lengths `1, 2, 3`;
- the documented example `4`;
- fixed representatives through `50`;
- 30 distinct positive values generated with seed `139`, up to `75`;
- an independent `math.prod(math.factorial(...))` oracle on all positive cases.

The 38-input run reports `mismatch_count=0`, `n=4 -> 288`, `n=1 -> 1`, and
`n=2 -> 2`. Exact command and exit:

```bash
/audit-output/evidence/02_program_fidelity.sh
# exit 0
```

Evidence: `evidence/02_program_fidelity.sh` and
`evidence/02_program_fidelity.log`.

## 3. Clean proof reconstruction

I copied only source artifacts into `/tmp/audit-work/reconstruction`, copied
the semantics from the trusted `/reference` mount, and created new output
directories named `audit-runtime-kompiled` and
`audit-verification-kompiled`. No candidate cache or compiled definition was
copied or referenced. The independently observed tool version is K v7.1.293.

### Fresh concrete definition

Commands:

```bash
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-runtime-kompiled

krun regenerated-smoke.mpy --definition audit-runtime-kompiled
```

The trusted translator also reproduced `smoke.mpy` byte-for-byte before this
run. The LLVM build exits `0`. The concrete run consumes assertions for
`N=1..6`, exits `0`, and ends with `.K`, `NoExc`, empty stack, `noRet`, and
exit code `0`.

### Fresh proof definition and every positive claim

Commands:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition audit-verification-kompiled

kprove spec.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC

kprove summary-test.k \
  --definition audit-verification-kompiled \
  --spec-module SUMMARY-TEST
```

The Haskell build exits `0`. The complete `SPEC` command proves both
`loop-invariant` and `special-factorial`; it prints `#Top` and exits `0`.
The supporting module's twelve positive ground claims for both summary
functions at `N=1..6` also print `#Top` and exit `0`. Their
`WarnTrivialClaim` messages mean the ground functions simplified before a
reachability step; they are not failures.

The compiler warnings concern fixed, unused supplied-semantics helpers and are
accounted for in Stage 5. None occurs in candidate proof-local rules or on the
reachable program path.

Evidence: `evidence/03_reconstruct.sh` and
`evidence/03_reconstruct.log` (wrapper exit `0`, with exact outputs and
individual exit statuses).

## 4. Adequacy and real-program pinning

### Claims in plain language

`SPEC.loop-invariant` starts at the actual recurring internal loop head
`#while(...)`. Its precondition is:

```text
N >= 1, 1 <= I <= N + 1
```

with current locals `n=N`, `i=I`, `factorial=F`, and `result=R`. It executes
the exact three-statement source loop, consumes only that loop, preserves the
continuation and all framed cells, and finishes with:

```text
i         = N + 1
factorial = factorialAfter(I, N, F)
result    = productAfter(I, N, F, R)
```

`SPEC.special-factorial` starts from the standard empty module scope, trusted
builtins scope, empty heap and stack, normal return/exception state, and
`N >= 1`. It loads the exact translated function, calls its resulting binding
with `N`, and reaches:

```text
productAfter(1, N, 1, 1)
```

The final module binding remains present; the callee frame is deallocated; the
environment, allocator, heap, stack, return state, exception state, and exit
code are restored or constrained to their intended values. The result is not a
right-only free variable, tautology, or implication.

### Mechanical constructor-level program identity

`evidence/04_constructor_compare.py` removes only whitespace and compares the
trusted-regenerated complete `Module(FuncDef(...))` against the `#loadAll`
argument in the entry claim. It finds exactly one exact occurrence. It also
checks the exact `special_factorial` call, positive unbounded integer
precondition, and result recurrence. The check exits `0`.

Thus the claim mechanically pins the submitted function name, parameter,
binding, initializations, guard, all three ordered body assignments, and
return. No typing import or other normalization is omitted.

### Satisfiable states and concrete substitutions

`evidence/04_witnesses.k` supplies two fresh ground claims:

- loop witness `N=4, I=1, F=1, R=1, L=1`, ending at
  `factorial=24`, `result=288`, `i=5`;
- full entry witness `N=4`, returning the independent ground integer `288`
  rather than a symbolic summary.

Together they exhibit realizable states for both candidate preconditions. The
module prints `#Top` and exits `0`. Both trusted canonical Python and candidate
Python also return `288`. Ground summary proofs additionally establish:

```text
N=1 -> 1
N=2 -> 2
N=3 -> 12
N=4 -> 288
N=5 -> 34560
N=6 -> 24883200
```

The recurrence has the intended mathematical meaning. At loop head `I`, let
`F=(I-1)!` and `R=product(k!, 1 <= k < I)`, with the empty product equal to
one. The first assignment makes `F'=F*I=I!`; the second makes
`R'=R*F'=product(k!, 1 <= k <= I)`; the last makes `I'=I+1`. At exit
`I=N+1`, so `R=N!*(N-1)!*...*1!`. This is a direct induction over the same
recurrence, not an empirical oracle.

The body-sensitivity check materially changes the executed loop term to
`result = result * factorial + 1` while retaining the original summary. Fresh
`kprove` execution exits `1` with `WarnStuckClaimState` and the expected false
equality between:

```text
productAfter(..., R * (F * I) + 1)
productAfter(..., R * (F * I))
```

Evidence:

- `evidence/04_adequacy.sh`
- `evidence/04_adequacy.log` (exit `0`)
- `evidence/04_witnesses.k`
- `evidence/05_body_sensitivity.sh`
- `evidence/05_body_sensitivity.log` (the negative K command exits `1`; the
  validation wrapper exits `0`)

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/05_rule_inventory.py` inventories the assembled semantics, all 23
helper K files, `verification.k`, and `spec.k`. It records the complete
normalized source text, location, attributes, and audit disposition of every:

- 229 syntax declaration blocks;
- 699 ordinary/equational rules;
- 5 evaluation contexts;
- 1 configuration;
- 2 reachability claims.

There are 936 records. The inventory includes all function/total declarations,
all 45 rule priority attributes, all concrete and no-evaluator declarations,
all `owise` rules, and both macro kinds. There are no source
`[simplification]` or `[functional]` declarations. The complete enumeration is
in `evidence/05_rule_inventory.log`; the accompanying static scans are in
`evidence/05_static_checks.log`. Both wrappers exit `0`.

### Used construct/rule map

| Submitted construct | Fixed declarations and operational path |
|---|---|
| `Module`, statement lists | `syntax.k`; `core.k` `#loadAll`, head sequencing, empty sequence |
| `FuncDef`, `Params` | `functions.k` ordinary closure creation |
| `Call(Name(...), N)` | `core.k` name lookup; `call.k` callee then left-to-right argument evaluation and closure dispatch |
| parameter binding | `functions.k` plain-frame `#bindP` |
| integer literals and names | `core.k` literal and plain-scope lookup |
| `Assign` | `syntax.k` RHS strictness; `controls.k` plain current-scope update |
| `BinOp("*",...)`, `BinOp("+",...)` | `syntax.k` `seqstrict(2,3)`; `operators.k` dispatch; `int.k` exact integer equations |
| `Compare(...,"<=")` | two `operators.k` evaluation contexts, then `int.k` `<=Int` |
| `While` | `controls.k` `While -> #while`, guard evaluation, `#whileCond`, body, and recurring `#loopLbl` |
| `Return` | `syntax.k` strict value evaluation; `functions.k` return, frame pop, environment restoration, and frame deallocation |

This path uses unbounded K integers, not floats or machine integers. Evaluation
order is the translator's AST order plus the supplied `strict`/`seqstrict`
attributes and explicit comparison/call contexts: RHS before assignment,
binary operands left-to-right, comparison left then right, callee before
arguments, and arguments left-to-right.

The only state changes are the module function binding, callee frame
allocation, parameter/local map writes, stack push/pop, environment switch,
and frame deallocation. Heap and exception cells remain unchanged. Return
discards the remainder of the callee body, then restores the exact saved
continuation; this matches the submitted control flow.

### Overlaps, priorities, opaque values, and proof-local rules

`verification.k` contributes exactly:

- two `[function,total]` integer symbols;
- four guarded equations;
- no priority, simplification, concrete, opaque/no-evaluator, `Call`, `While`,
  `Return`, or other operational rule.

For each summary, `I > N` and `I <= N` are disjoint and exhaustive over K
integers. The base equation returns the existing accumulator. The step equation
increments `I`, uses exactly the program's new factorial in the product update,
and decreases `max(N-I+1,0)`. The two functions are truthful definitional
summaries. They do not match any MPY AST or any configuration cell and therefore
are not operational bridges.

The fixed semantics has 45 explicit priority rules. Every one was inspected.
On this path:

- cell-reference lookup/write priorities require `"$cells"` or a `cellRef`,
  neither of which can occur in the ordinary submitted closure frame;
- heap dereference rules require `ref`, while the program creates only integer
  values and no heap objects;
- list, tuple, dict, string-method, sort, assertion, and subscript priorities
  require constructors absent from `solution.mpy`;
- math and MD5 call interceptions require an `Attribute` callee with fixed
  names, disjoint from `Call(Name("special_factorial"),...)`;
- the generic call and comparison `owise` rules therefore select the intended
  plain closure and integer paths.

The fixed tree contains opaque/no-evaluator primitives for floats, sorting,
MD5, and other tasks. None appears in `solution.mpy`, either claim, either
summary, or any reachable value/cell. No proof conclusion depends on an
interpretation of those symbols. Likewise, LLVM compilation reports six
non-exhaustive totality warnings in unused fixed helpers:
`mapStrVS`, `floorFI`, `toF`, `ceilF`, `joinCodes`, and `valSeqAt`. Their
constructors cannot be reached by this integer-only program. `[total]` does not
create a task answer, and no warned helper contributes to claim closure.

I make no unsound-rule finding. In particular, I found no rule capable of
enabling a false conclusion on any allowed positive-integer execution. The
supplied semantics is intentionally only a Python subset outside this
dependency slice; rules for unused language features are not evidence for or
against this theorem. Within the reachable slice, configuration, evaluation
order, scope updates, call/return, loop control, and integer operations match
the program and ordinary mathematics.

## 6. Fresh non-vacuity test

I did not reuse the candidate's `spec-vacuity.k`. The reviewer-authored
`evidence/06_false_result.k` keeps the exact program and loop invariant but
changes the entry destination from:

```text
productAfter(1, N, 1, 1)
```

to:

```text
productAfter(1, N, 1, 1) + N
```

This is false throughout the precondition because `N >= 1`. The explicit
satisfying witness `N=4` has canonical/candidate result `288` but mutated
destination `292`.

Commands and results:

```bash
kprove audit-false-result.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run
# exit 0: mutation parses and builds

kprove audit-false-result.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT
# exit 1
```

The failure is a meaningful `WarnStuckClaimState`, not a parser error, timeout,
or unrelated crash. Its residual requires the impossible equality:

```text
productAfter(2, N, 1, 1) + N
#Equals
productAfter(2, N, 1, 1)
```

and retains `N >= 1`. Evidence:
`evidence/06_false_result.k`, `evidence/06_nonvacuity.sh`, and
`evidence/06_nonvacuity.log` (validation wrapper exit `0`).

## 7. Proven versus assumed accounting

### What the successful reachability proof establishes

For every K integer `N >= 1`, from the fully specified normal module
configuration in `SPEC.special-factorial`, fixed MPY execution:

1. loads the exact trusted-regenerated submitted function;
2. resolves and calls that exact binding with `N`;
3. evaluates every initialization, guard, lookup, multiplication, addition,
   assignment, loop-control step, and return in the submitted body;
4. restores the caller configuration with no exception and exit code zero;
5. leaves the returned K computation exactly
   `productAfter(1,N,1,1)`.

The proved loop circularity universally connects fixed execution of the exact
loop body to the exhaustive accumulator recurrence. Ordinary induction then
identifies that recurrence with `N!*(N-1)!*...*1!`. The formal domain is
unbounded; it is not a finite-size, example-only, or bounded-unrolling theorem.

This is partial correctness in the Kit sense. It does not independently prove
CPython termination, resource availability, or behavior for zero, negative,
boolean, float, or other non-contract inputs.

### Trust ledger

| Boundary | Effect and dependents | Assessment |
|---|---|---|
| K v7.1.293 compiler, Haskell/LLVM backends, SMT/runtime, and integer hooks | All machine-checking and concrete K evidence | Standard unavoidable proof-tool trust; acceptable |
| Trusted supplied MPY semantics | Meaning of the reachable module/scope, integer, assignment, call/return, and loop rules | Recursively integrity-checked and exhaustively reviewed on the reachable slice; acceptable |
| Trusted `py2mpy.py` | Translation from submitted Python AST to MPY constructors | Byte regeneration plus constructor-level mapping verifies the actual artifact used; semantic correctness of the trusted translator remains a named baseline assumption; acceptable |
| `factorialAfter`, `productAfter` | Final accumulator and returned result | Not assumed or opaque: exhaustive, disjoint, terminating equations plus the machine-proved loop claim fix their values |
| Recurrence-to-contract induction | Interprets the formal returned recurrence as the natural-language product of factorials | Transparent base/step argument over the exact program updates; acceptable, with finite differential evidence only as corroboration |
| Fixed opaque symbols and warned unused total helpers | None | No reachable dependent claim or value; irrelevant to this theorem |
| Canonical/Python and LLVM differential checks | Program/intent and concrete-semantics corroboration on recorded inputs | Finite empirical evidence only; not substituted for the K proof |

There is no externally trusted result-bearing primitive, empirical bridge, or
opaque program-derived value on the theorem's result path. There is no
operational bridge to require a separate context-containment theorem. The loop
claim itself is the universal fixed-semantics connection for the two truthful
summaries.

### Gate results and decision

- Gate A (real-program soundness): PASS. The exact body executes; proof-local
  equations are true; state/control are preserved; preconditions are
  satisfiable; body and false-result mutations are rejected.
- Gate B (intent adequacy): PASS. `N >= 1` is the complete prompt domain, K
  integer arithmetic matches the relevant Python integer model, and the formal
  recurrence is the requested special factorial.
- Gate C (trust/evidence auditability): PASS. Inputs, source inventory,
  commands, exit statuses, positive outputs, ground witnesses, differential
  scope, and negative residuals are preserved under `/audit-output/evidence`.

The candidate therefore meets `PASS / LEGIT`: it is a sound,
result-constraining proof of the real generated program over the full material
source-contract domain, with no material adequacy gap.

VERDICT: PASS
LEGITIMACY: LEGIT
