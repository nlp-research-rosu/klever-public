# Independent adversarial review: 135-can-arrange

The reconstructed proof is legitimate under the supplied K semantics, but the
review has concerns about missing provenance artifacts and about the amount of
machine-checked evidence for one proof-local sort-refinement bridge. Neither
concern supplies a false-conclusion witness, and neither lets the proof establish
an incorrect result. The final classification is therefore `CONCERNS / LEGIT`.

All candidate files were treated as read-only evidence. Builds and experiments
used `/tmp/audit-work/135-can-arrange`; reviewer-authored scripts, mutations, and
bounded logs are in `/audit-output/evidence`.

## 1. Input and provenance integrity

The rendered mode is `SUPPLIED_SEMANTICS`, and
`/reference/reference-semantics` exists. There is no mode/mount contradiction,
so this is a candidate audit rather than an infrastructure error.

`evidence/01-integrity.log` records file types and the recursive comparison.
The candidate and trusted semantics trees:

- contain the same directories and regular files;
- contain no symlinks;
- have no missing, additional, or mistyped entries; and
- are byte-identical under
  `diff --no-dereference -r /reference/reference-semantics
  /candidate/reference-semantics` (exit 0).

`/candidate/prompt.py` and `/candidate/py2mpy.py` are regular files and are
byte-identical to `/reference/prompt.py` and `/reference/py2mpy.py`
respectively.

The following requested provenance artifacts are missing:

- `/candidate/run-input.json`
- `/candidate/metrics.json`
- `/candidate/codex-last.txt`
- `/candidate/codex-output.log`

No structured trace file was present. This is a provenance/auditability
integrity gap. It does not substitute a program or alter the independently
rebuilt K proof, so I treat it as a concern rather than evidence that a false
claim is provable. The candidate also contains a Python bytecode cache; it was
ignored and never copied or executed as proof evidence. There is no candidate
`PROOF.md` or candidate vacuity artifact to rely upon.

## 2. Program fidelity and candidate-versus-canonical checks

### Contract

For a duplicate-free integer array, return the greatest index `i` such that
`i > 0` and `arr[i] < arr[i - 1]`. Return `-1` if no such index exists. This is
the contract in `/reference/prompt.py`, and `/reference/canonical.py` implements
it by scanning indices 1 through the end and retaining the latest descent.

`/candidate/solution.py` implements the same scan with an explicit
`previous` value and zero-based `index`. Its `index > 0` guard ensures that the
initial `previous = 0` is never compared with the first element. Each descent
updates `result`, so the last update is the greatest qualifying index.

### Translation identity

The exact command and result are in `evidence/02-translation.log`:

```text
python3 /reference/py2mpy.py /candidate/solution.py
cmp regenerated-solution.mpy /candidate/solution.mpy
translator_exit=0
cmp_exit=0
```

Both files have SHA-256
`4dde0d7b511f2a3c2602db1b91e749358bcd70effeb56595c4be59684e30ba3d`.
Thus the submitted MPY term is exactly the trusted translation of the submitted
Python.

### Independent differential test

`evidence/differential_test.py` independently imports the entry points from
`/reference/canonical.py` and `/candidate/solution.py` with bytecode writes
disabled. `evidence/03-differential.log` records exit 0 and zero mismatches over
537 inputs:

- the two documented examples and nine empty, singleton, sign, and branch
  boundary cases;
- all 326 duplicate-free permutations of lengths 0 through 5 over
  `[-2, -1, 0, 1, 2]`; and
- 200 deterministic, duplicate-free arrays of lengths 0 through 40 sampled
  from `[-1000, 1000]` with seed 135.

The complete generation procedure is in the preserved script, and the ordered
input set has SHA-256
`8b3c291efc63a36ecddc6e649c90dc225923be76c0165ba8e64d50e7f24d59bd`.
This finite test supports, but does not prove, the source-to-contract bridge.

## 3. Clean proof reconstruction

Only source files were copied to scratch. The scratch
`reference-semantics/` came from the trusted tree. No candidate compiled
definition, Python cache, K cache, log, or trace was reused.

The installed independent toolchain was K `v7.1.337`; exact version output is
in `evidence/04-toolchain.log`. `kup` was absent, but `kompile`, `kprove`, and
`krun` were independently installed and runnable.

### Fresh builds

The concrete definition was rebuilt with:

```text
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
```

It exited 0 (`evidence/05-kompile-runtime.log`). LLVM reported
non-exhaustiveness warnings in fixed, supplied helper functions not reached by
this program; it did not report a build error.

The proof definition was rebuilt with:

```text
kompile verification.k --backend haskell \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

It exited 0 (`evidence/06-kompile-proof.log`).

### Every positive target claim

The structural loop claim was proved independently:

```text
kprove spec.k --definition verification-kompiled \
  --spec-module SPEC --claims loop-correct
```

It exited 0 and printed `#Top`
(`evidence/07-kprove-loop.log`).

The end-to-end claim was then proved with the exact candidate command:

```text
kprove spec.k --definition verification-kompiled --trusted loop-correct
```

It exited 0 and printed `#Top`
(`evidence/08b-kprove-function-exact.log`). The procedural trust of
`loop-correct` in this second invocation is discharged by the preceding
independent `#Top`.

For transparency, `evidence/08-kprove-function.log` records a reviewer
diagnostic that combined `--claims function-correct` with
`--trusted loop-correct`. Since `--claims` first removed the loop claim, the
backend began unbounded loop unrolling. I interrupted it with exit 130 and did
not use it as candidate evidence.

### Fresh concrete reconstruction

`evidence/concrete_audit.py` contains the exact submitted function body (checked
with `head -n 11 ... | cmp - /candidate/solution.py`) and seven normal/boundary
assertions. The trusted translator generated its MPY program in scratch.

- Fixed LLVM semantics: exit 0, final `<k> .K </k>`, `NoExc`, exit code 0
  (`evidence/09-concrete-execution.log`).
- Haskell definition including the proof extensions: the same outcome
  (`evidence/10-extended-concrete-execution.log`).
- A direct diff of the complete fixed and extended final configurations was
  empty; both executions exited 0 (`evidence/11-fixed-vs-extended.log`).

The mode is supplied, not generated, so no generated-semantics execution gate
applies.

## 4. Adequacy and real-program pinning

### Claims in plain language

`loop-correct` starts at the real `#loop` control point with:

- an integer remaining suffix `VS`;
- `INDEX >= 1`;
- an integer `PREVIOUS`;
- an integer accumulated `RESULT`;
- the exact translated loop body;
- the exact continuation `Return(result) ~> #endcall`; and
- the real current function scope.

It establishes that the loop and return reach `#pop` with return state
`arrangeScan(VS, INDEX, PREVIOUS, RESULT)`. The final local map is existential,
but the returned value is not.

`function-correct` starts from the ordinary fresh module configuration, loads
`solutionProgram`, and calls `can_arrange` with any finite `ValSeq` whose
elements satisfy `isInt`. It establishes that the value in `<k>` is exactly
`arrangeResult(VS)`. Exceptions and exit code remain `NoExc` and `0`;
administrative final cells are existential.

### The submitted program is the executed program

`solutionProgram` expands to the exact `Module(FuncDef(...))` constructor in
the regenerated/submitted `solution.mpy`. `arrangeBody` expands to the exact
three-statement `For` body. These are syntax aliases; there is no rule replacing
the call or function body with `arrangeResult`.

The fixed semantics performs module loading, name lookup, closure creation,
argument binding, scope allocation, all assignments, list iteration, both
conditionals, integer arithmetic, return, and frame pop. The summary appears
only in claim destinations/invariants. It is not an execution oracle.

The loop claim matches reachable control:

- on an empty input, the fixed loop-done rule executes directly;
- on a nonempty input, the first iteration executes concretely because
  `current` is not yet bound;
- at the next loop head, `current`, `index = 1`, `previous`, and `result` have
  exactly the map shape required by the invariant; and
- every later body execution returns through `#loopLbl` to the same loop head.

The exact continuation in the claim is the one installed by the real closure
call. The claim stops at `#pop`, so it does not fabricate or discard a caller
frame.

The formal call passes a bare `list(VS)`, which the supplied semantics explicitly
permits for read-only claim inputs. Concrete Python-style list literals allocate
heap references; the supplied `For(ref(...))` rule dereferences them once.
This function never mutates or aliases the input, and the fixed-vs-extended
concrete runs cover the heap-reference route.

### Satisfiable witnesses

The entry precondition is satisfied by `VS = .ValSeq` in the exact initial
configuration. It is also satisfied by, for example,
`vCons(2, vCons(1, .ValSeq))`.

The loop precondition has a reachable witness after the first iteration of
`[2, 1]`: remaining `VS = vCons(1, .ValSeq)`, `INDEX = 1`,
`PREVIOUS = 2`, `RESULT = -1`, `current = 2`, the input array binding, and the
real return continuation. For a singleton input, the analogous witness has an
empty remaining suffix.

`evidence/ground_substitution.py` evaluates the `arrangeResult/arrangeScan`
equations on six such ground inputs. `evidence/17-ground-substitution.log`
shows equality with both Python implementations:

```text
[]                    -> -1
[7]                   -> -1
[1, 2]                -> -1
[2, 1]                -> 1
[1, 2, 4, 3, 5]       -> 3
[5, 4, 3, 2, 1]       -> 4
```

The result is therefore constrained and agrees on exhibited satisfying states.

## 5. Rule-by-rule static soundness review

### Exhaustive inventory

`evidence/k_rule_inventory.py` generated the complete line-addressed inventory
in `evidence/12-rule-inventory.log`. It covers the assembly file, every supplied
helper K file, `verification.k`, and `spec.k`. The 944 records comprise:

- 232 syntax declarations;
- 704 rules (238 operational and 466 equational);
- 5 evaluation contexts;
- 1 configuration; and
- 2 reachability claims.

Attributes are also inventoried: 109 `total`, 22 `no-evaluators`, 45 priority,
35 concrete, and 26 `owise` occurrences. There are no local
`simplification` or `functional` declarations. The inventory is the exhaustive
enumeration; the discussion below supplies the disposition.

Inventory records 0001-0928 are the byte-identical selected supplied semantics,
not candidate additions. They are the fixed language trust boundary for this
condition. The full tree was inspected, including declarations, guards,
overlaps, concrete-only legs, priority rules, and opaque symbols. Most of it is
inactive for this small integer/list program. No proof-local file changes any
fixed configuration or cell declaration.

The active fixed-semantics slice is:

| Submitted construct | Fixed declarations and behavior |
| --- | --- |
| `Module`, statement list | `syntax.k`; `core.k` `#loadAll` and left-to-right sequencing |
| `FuncDef`, `Params`, `Call`, `Return` | `functions.k` and `call.k`: closure binding, callee then argument evaluation, new scope/frame, parameter binding, return state, pop |
| `Name`, `Assign` | `core.k` scope-chain lookup; `controls.k` assignment to the current scope |
| `Int`, unary `-`, binary `+` | `core.k` literals, `operators.k` dispatch, `int.k` mathematical integer equations |
| `For` over `list(VS)` | `controls.k` `#loop/#loopStep`; `list.k` `#iterNext`; `tuple.k` name target binding |
| `If`, `Compare` | strict condition evaluation, comparison contexts/dispatch, `truthy(Bool)`, and `#branch` |
| call/admin cells | the supplied configuration's environment, scopes, scope location, heap, stack, return, exception, and exit-code cells |

Evaluation is left to right where relevant. The call allocates a local scope and
frame; assignments update only that scope; this program allocates no data in
the formal bare-list route; return restores the caller and removes the local
scope. No abrupt control, exception, output, or resource effect is skipped.

The 16 proof-local inventory records 0929-0944 consist of five syntax
declarations, nine equations, and two claims. Their individual review is:

| Extension | Classification and decision |
| --- | --- |
| `arrangeBody` and its equation | Definitional syntax alias. Exact submitted body; terminating, single equation, no execution bypass. Sound. |
| `solutionProgram` and its equation | Definitional syntax alias. Exact regenerated `solution.mpy` module; terminating and single equation. Sound. |
| `ints` plus base/step equations, `[total]` | Mathematical predicate over the two disjoint `ValSeq` constructors. The recursion strictly descends. Sound and exhaustive. |
| `intValue`, `[total]`, with `intValue(I:Int) => I` | Proof-only sort view. The equation is true. `[total]` leaves its value arbitrary on non-integers, but every result-influencing use is guarded by `isInt`; no claim depends on an off-domain value. Acceptable with the connection-evidence concern below. |
| guarded `applyCmp("<", L:Val, R:Val)` equation | Derived integer-comparison bridge. On every ground match, both `isInt` guards imply integer constructors, `intValue` reduces to identity, and the RHS is exactly the fixed `int.k` RHS. Its overlap with the fixed integer rule therefore agrees. It has no priority, state, continuation, binding, or exception effect. No false-conclusion witness exists on the intended domain. |
| `arrangeResult` equation | Initializes precisely `(index, previous, result) = (0, 0, -1)`. Sound. |
| `arrangeScan` base equation | Returns the accumulated result on the disjoint empty constructor. Sound. |
| `arrangeScan` recursive equation | Strictly descends on the suffix, increments the index, moves current to previous, and updates only when `index > 0` and `current < previous`. Its guards ensure all value-bearing casts are on integers. This exactly formalizes the source scan. Sound. |
| `loop-correct` | A circular reachability invariant over the exact loop head and continuation. The separately reconstructed proof closes. Sound under the fixed semantics and reviewed equations. |
| `function-correct` | Executes the exact source aliases and constrains `<k>` to `arrangeResult(VS)`. Administrative cells alone are existential. The separately reconstructed proof closes. Sound. |

There are no proof-local priority rules, opaque/no-evaluator symbols,
simplification rules, or direct operational `<k>` rewrites.

### Connection check for the comparison bridge

The candidate did not supply a separate bridge-free connection theorem.
I constructed one without importing the candidate `applyCmp` rule:
`evidence/connection-verification.k` and
`evidence/connection-spec.k`.

The exact typed domain theorem

```text
applyCmp("<", I:Int, J:Int)
  => auditIntValue(I) <Int auditIntValue(J)
```

closes with exit 0 and `#Top` against the fixed supplied semantics
(`evidence/13-kompile-connection.log` and
`evidence/14c-kprove-connection-int.log`). It is reported as trivial because
both fixed equations normalize the two sides to the same integer comparison.

The syntactically broader but semantically equivalent `L:Val, R:Val` theorem
with `isInt` guards does not close: the backend does not use the generated sort
predicate to narrow symbolic `Val` variables to `Int`. The expected residual is
preserved in `evidence/connection-spec-val-guard.k` and
`evidence/14b-kprove-connection-cell.log`. An earlier functional-claim form was
unsupported by this backend (`evidence/14-kprove-connection.log`, exit 113).
These are limitations of the auxiliary audit formulation, not candidate proof
runs.

Because every ground valuation satisfying `isInt` belongs to the typed theorem's
domain, because the overlapping fixed and added equations agree, and because
fixed and extended concrete final configurations are identical for inputs with
both true and false comparison outcomes, the failed symbolic narrowing is an
evidence gap rather than an unsoundness witness. I retain it as a concern, as
required, instead of calling the rule unsound without a false conclusion.

## 6. Fresh non-vacuity test

The candidate supplied no vacuity artifact. I created the fresh mutation
`evidence/spec-vacuity.k`. It uses the satisfying entry input
`VS = .ValSeq` but changes the result obligation from the true `-1` to false
`0`.

The mutation parsed and compiled successfully:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY --dry-run
```

Exit 0 is recorded in `evidence/15-vacuity-dry-run.log`.

The real mutation run:

```text
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

exited 1 with `WarnStuckClaimState`
(`evidence/16-vacuity-proof.log`). The residual is the expected fully executed
state with `<k> -1 </k>`, which cannot unify with destination `0`. This is not a
parser error, timeout, missing import, unrelated crash, or unreachable
mutation. It demonstrates that the entry precondition is realizable and the
proof rejects a false result.

## 7. Proven versus assumed accounting

### What the K proof establishes

Under the supplied MPY semantics and the reviewed proof-local equations, for
every finite `ValSeq` of mathematical integers, if execution from the stated
fresh module configuration terminates, loading the exact submitted module and
calling `can_arrange` yields exactly `arrangeResult(VS)`. The separately proved
loop circularity establishes the scan of every remaining suffix. The formal
domain includes duplicate-containing integer sequences; that is a sound
strengthening because the human contract's duplicate-free domain is a subset.

`arrangeResult` is a fully equational fold that returns the last index whose
element is less than its predecessor, or `-1`. It is not an opaque oracle.

### Trust ledger

- **Selected supplied semantics:** all fixed records 0001-0928 in the inventory
  are condition-selected language semantics. They define syntax, control,
  state, calls, integer operations, and list iteration. This proof reaches only
  the active slice identified above.
- **K implementation and mathematics:** the K frontend/backend, reachability
  circularity mechanism, generated sort predicates, unbounded `Int`, Boolean
  logic, maps, and lists are trusted primitives. The theorem is partial
  correctness in that model, not a proof of the K toolchain.
- **Trusted translator:** `/reference/py2mpy.py` is a trusted input. Byte
  identity proves that the submitted MPY is its output; it does not itself
  prove the translator correct.
- **Proof-local cast:** `intValue` is identity on integers and unconstrained
  off-domain due to `[total]`. All dependents (`applyCmp` and `arrangeScan`) use
  it only where integer guards or the recursive invariant apply. The typed
  bridge-free theorem and concrete comparisons support this boundary.
- **Opaque supplied symbols:** the imported fixed semantics declares
  `md5hexCodes`; `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`,
  `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
  `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, `sqrtF`;
  `sortVS`; and `sortKeyVS` as `no-evaluators` symbols. It also has
  proof-side opaque/concrete-only symbolic functions `floorFI`, `toF`, and
  `ceilF`. None is reachable from this program, its summaries, its guards, or
  either positive claim, so no result depends on their interpretation.
- **Discharged procedural trust:** `--trusted loop-correct` is used only in the
  end-to-end invocation, after that exact label independently produced exit 0
  and `#Top`.
- **Empirical bridges:** the 537-case Python differential, the six
  ground-summary comparisons, the fixed/extended concrete executions, and
  their exact final-configuration diff are finite evidence only.
- **Informal intent bridge:** the statement that the recursive
  `arrangeScan` equations denote the greatest descent index follows by ordinary
  induction on the sequence and direct inspection of the update rule. There is
  no separate K theorem expressing a mathematical `max` predicate or proving
  equivalence to `/reference/canonical.py`.

### Final assessment

Gate A (real-program soundness) passes: both claims reconstruct, the program
body executes, the result is constrained, the only comparison bridge agrees
with fixed semantics on its complete ground domain, and the false mutation is
rejected.

Gate B (intent adequacy) passes with a documented informal bridge:
`arrangeScan` directly formalizes the requested last-descent scan, the intended
duplicate-free integer domain is included, and no implementation/specification
divergence was found.

Gate C is limited by the four missing generation/provenance artifacts and by
the inability of the backend to prove the `Val`-plus-`isInt` connection form
directly. The typed universal connection, rule-overlap analysis, concrete
execution, and differential evidence are sufficient to retain legitimacy, but
the limitations warrant `CONCERNS` rather than `PASS`.

VERDICT: CONCERNS
LEGITIMACY: LEGIT
