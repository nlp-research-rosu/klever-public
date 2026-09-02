VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, `move_one_ball` is partially
correct for every finite list whose elements are mathematical integers.
Starting from the exact `move_one_ball` binding and exact translated body, the
call terminates in the Boolean `moveSpec(VS)` whenever it terminates.

`moveSpec(VS)` is:

- `true` for the empty list; and
- for a nonempty integer list, `true` exactly when the circular sequence has
  at most one strict descent.

For a finite sequence, at most one strict circular descent is equivalent to the
existence of a cyclic right shift that is nondecreasing. The formal theorem is
therefore aligned with the HumanEval contract. The prompt's uniqueness
guarantee is not needed by the implementation or theorem; the formal domain is
strictly broader and also includes duplicate integers.

This is a partial-correctness result in the sense of K reachability logic. A
separate total-correctness/termination theorem is not claimed.

## Formal claims

`spec.k` contains exactly the required whole-program claim plus one claim for
the program's one loop:

1. `SPEC.scan-loop` starts at the fixed semantics' exact
   `#loop(list(VS), Name("current"), scanBody)` configuration. With
   `previous = current = P`, accumulator `D`, `isInt(P)`, and `allInts(VS)`,
   it preserves the arbitrary continuation and all framed cells, changes
   `previous` and `current` to `lastAfter(P, VS)`, and changes `drops` to
   `scanDrops(D, P, VS)`.
2. `SPEC.move-one-ball` starts with
   `Call(Name("move_one_ball"), (list(VS), .Exprs))`, the module scope binding
   that name to `closureVal("arr", moveOneBallBody, 0)`, the real builtins
   scope, empty heap and stack, and `allInts(VS)`. It reaches `moveSpec(VS)`
   with the call frame fully popped and the initial external configuration
   restored.

The three loop obligations close as follows:

- Base: `scanDrops(D, P, .ValSeq) = D` and
  `lastAfter(P, .ValSeq) = P`.
- Step: the fixed iterator yields the head, the fixed assignment and integer
  comparison rules perform the accumulator update, and the circularity applies
  to the tail. The step equation for `scanDrops` is the same left fold.
- Whole program: the exact call reaches the exact loop head; the loop claim
  supplies the fold, the fixed rules add the last-to-first edge, return the
  comparison, and pop the frame.

## Proof-extension inventory

The inventory below was rebuilt from the final `verification.k` and `spec.k`.

### Compile-time AST aliases

`scanBody` and `moveOneBallBody` are `[macro]` syntax aliases, not runtime
rules and not operational bridges. Their expansions are the exact AST
constructors in `solution.mpy`. They introduce no value, state, control, or
exception behavior; after macro expansion every statement executes under the
fixed `MPY` rules.

### Definitional summaries

| Extension | Domain and equations | Matched context and state footprint | Value influence and justification | Dependents and validation |
|---|---|---|---|---|
| `allInts(ValSeq)` | All `ValSeq`; `.ValSeq` and `vCons` are disjoint and exhaustive; recursion consumes the tail. `[total]` is justified. | Pure function in any term context; reads/writes no configuration cell. | Defines the formal input predicate from the generated `isInt` predicate. It affects only guards. | Both claims and guarded summary equations. Constructor coverage was audited; the full proof closes. |
| `scanDrops(Int, Val, ValSeq)` | The empty equation applies for any prior value. The step equation applies when the prior and head values are integers and consumes the tail. It is intentionally not declared total outside the integer domain. | Pure function; no continuation, binding, heap, scope, return, exception, or output effect. | Returns the exact left-associated accumulator produced by `drops = drops + (current < previous)`. Each head contributes `1` iff its projected integer is less than its predecessor. | `scan-loop` and `moveSpec`. Its universal connection to program execution is the machine-checked `scan-loop` claim. Concrete true/false witnesses and differential tests provide additional finite evidence. |
| `lastAfter(Val, ValSeq)` | All prior values and all `ValSeq`; empty/cons cases are disjoint and exhaustive and recursion consumes the tail. `[total]` is justified. | Pure function in any context; no cells read or changed. | Names the prior value for an empty suffix and the last list element otherwise. It determines the post-loop locals and closing comparison. | `scan-loop`, the guarded comparison lemma, and `moveSpec`. The loop claim machine-checks the local-state connection. |
| `moveSpec(ValSeq)` | Empty equation guard `VS ==K .ValSeq`; nonempty equation guard `notBool (VS ==K .ValSeq) andBool allInts(VS)`. Guards are disjoint and cover the formal domain. The symbol is deliberately partial for nonempty non-integer sequences. | Pure final-result predicate; no operational context or state effects. | Empty maps to `true`. Nonempty maps the loop's exact full-list fold plus the closing last-to-first descent to `<= 1`. | Target of `move-one-ball`. The full K proof connects the exact function body to this value; the false-postcondition probe rejects its opposite for `[]`. |

### Derived lemmas

| Extension | Complete guard and context | Derivation and overlap check | State/value influence | Dependents and validation |
|---|---|---|---|---|
| `applyCmp("<", A:Val, B:Val) => {A}:>Int <Int {B}:>Int [simplification]` | Any pure `applyCmp` term, under `isInt(A) andBool isInt(B)`. It is context-independent and accepts no configuration cells. | This is the supplied `MPY-INT` equation `applyCmp("<", I1:Int, I2:Int) => I1 <Int I2` after guarded sort projection. Where it overlaps the supplied equation, both right sides are identical. | Refines only the value of an already selected fixed integer comparison; it does not skip lookup, operand evaluation, control, or state. | The loop step. The fixed loop still evaluates both names and the `Compare` node before this pure simplification. |
| `applyCmp("<", A, lastAfter(P, VS)) => ... [simplification]` | Any pure comparison with that exact right operand, under `isInt(A) andBool isInt(P) andBool allInts(VS)`. | Structural induction on `VS` shows `lastAfter(P, VS)` is an integer: base returns integer `P`; step replaces it with the integer head and recurses. The resulting comparison is therefore the same supplied integer equation. Its overlap with the general lemma has the identical projected comparison. | Determines the closing edge only; no operational cells or control are matched. | The post-loop comparison in `move-one-ball`; the full proof, true/false K cases, and differential oracle validate the dependent result. |

Neither lemma is an operational bridge: both rewrite pure semantic functions
after fixed lookup and operand evaluation. There are no proof-local k-cell
rules, priority rules, abrupt-control rules, opaque result oracles, or rules
that replace a user-defined call.

### Auxiliary reachability claim

`SPEC.scan-loop` is a derived reachability lemma/circularity.

- Domain: `isInt(P) andBool allInts(VS)`.
- Complete matched control context:
  `#loop(list(VS), Name("current"), scanBody)` with an arbitrary preserved
  continuation through the `<k> ... </k>` frame.
- Binding context: environment `L`, parent `0`, and exactly the five real
  locals `arr`, `first`, `previous`, `current`, and `drops`. The exact map
  rules out the closure-cell binding path that does not exist for this
  module-level capture-free function.
- State footprint: reads the current local scope; writes only `current`,
  `previous`, and `drops`; preserves `arr`, `first`, the outer scope map,
  continuation, heap, heap counter, scope counter, stack, return state,
  exception, and exit code.
- Context containment: the claim itself is quantified over the arbitrary
  preserved continuation and framed cells it accepts. It does not introduce
  return, frame popping, exceptions, break, or continue.
- Value justification: `scanDrops` and `lastAfter` have constructor-decreasing
  equations, and `kprove` checks the base and one-step/circularity obligations
  under fixed list iteration and assignment semantics.
- Dependents: `SPEC.move-one-ball`.
- Validation: focused `kprove` returned `#Top`; when that claim was
  deliberately filtered out during bounded diagnosis, the entry trace
  repeatedly unrolled real list steps, showing that no hidden operational
  shortcut replaces the loop.

## Exact commands and actual results

The reproducible command record is `prove.sh`. The complete captured run is in
`prove-run.out` and `prove-run.err`.

### Translation identity

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 py2mpy.py solution.py | cmp - solution.mpy
```

Actual result: all three commands exited `0`; `cmp` printed no differences.

### Concrete LLVM build and execution

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual result: both commands exited `0`. `krun` ended with:

```text
<k> .K </k>
<stack> .List </stack>
<ret> noRet </ret>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The LLVM compiler printed only warnings originating in the supplied reference
semantics (non-exhaustive total-function warnings and unused variables); it
reported no error.

### Haskell proof build and positive target proofs

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.scan-loop
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual results:

```text
kompile: exit 0
focused scan-loop kprove: #Top, exit 0
full SPEC kprove:         #Top, exit 0
```

The full command proves every claim in `spec.k`. The Haskell build printed only
the supplied `str.k` unused-variable warnings.

### Gate A false-postcondition mutation

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit `1` with `WarnStuckClaimState`. The residual `<k>` cell
contains `true ~> .K`, which does not unify with the deliberately false target.
`prove.sh` recorded:

```text
EXPECTED FAILURE: false-postcondition mutation exit 1
```

### Gate A body-sensitivity mutation

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit `1` with `WarnStuckClaimState`. After changing only the
empty branch to `return False`, the residual `<k>` cell contains
`false ~> .K`, which does not unify with the original true target.
`prove.sh` recorded:

```text
EXPECTED FAILURE: body mutation exit 1
```

### Independent differential evidence

```bash
python3 differential_tests.py
```

Actual output and exit:

```text
prompt_cases=5 unique_cases=5914 duplicate_cases=1093 mismatches=0
exit 0
```

The independent oracle constructs every cyclic rotation and compares it with
Python's `sorted` result. It does not use `scanDrops`, `lastAfter`, `moveSpec`,
or the descent-count equations.

### End-to-end recorded workflow

```bash
./prove.sh
```

Actual result: exit `0`, with two `#Top` markers, both expected mutation
failures, and zero differential mismatches.

## Gate results

### Gate A — PASS

- A1 program identity: `solution.mpy` is freshly regenerated and byte-compared;
  `moveOneBallBody`/`scanBody` expand to its exact AST. The entry claim fixes
  the `move_one_ball` binding to that exact closure and executes name lookup,
  argument binding, body, return, and pop. The body mutation is rejected.
- A2 operational state: there are no operational bridges. The loop claim
  states and proves its exact local writes and preserves every framed cell.
  The entry claim requires successful frame cleanup, `NoExc`, empty stack, and
  exit code `0`.
- A3 binding/evaluation/control: the target begins at a real `Call(Name(...))`
  in the exact module scope. Fixed rules evaluate the argument, select the
  closure, allocate and bind the frame, run the loop, return, and pop it.
  Neither derived lemma matches a k-cell or introduces control.
- A4 consistency: function cases are disjoint, exhaustive on every declared
  total domain, and structurally decreasing. Partial functions are explicitly
  guarded to the integer input domain. The two comparison lemmas agree on
  every overlap with each other and with `MPY-INT`.
- A5 non-vacuity: `[]` realizes the precondition and evaluates to `true`;
  `[3, 5, 4, 1, 2]` realizes it and evaluates to `false`. The deliberate false
  result for `[]` is rejected with exit `1`.

### Gate B — PASS

- Input alignment: the prompt guarantees a finite list of unique integers.
  `allInts(VS)` covers all such inputs and more; uniqueness is not assumed.
- Language model: K `Int` and CPython `int` are both unbounded mathematical
  integers for the used operations. Only finite list reads, strict integer
  comparisons, Boolean-to-integer addition, locals, calls, and returns are
  material. The claim's bare list value is the reference semantics' intended
  read-only proof representation; the implementation does not mutate or
  observe list identity.
- Summary/property: scanning the full list counts every internal strict
  descent (the first-vs-first contribution is zero), and the final addition
  counts the closing last-to-first edge. If a nondecreasing rotation exists,
  the circular sequence can have a descent only at that rotation's cut. In the
  converse direction, zero descents is already nondecreasing, and with one
  descent, cutting immediately after it gives a nondecreasing rotation.
- Implementation alignment: both prompt examples, the empty and singleton
  boundaries, a one-linear-descent counterexample, exhaustive unique
  permutations through length 7, and duplicate samples agree with the
  independent rotation oracle.

### Gate C — PASS

- Every proof-local equation, simplification lemma, macro, and claim is
  inventoried above with its domain, context, state/value influence,
  justification, dependents, and validation.
- `prove.sh`, the two mutation specs, `concrete_tests.py`,
  `concrete_tests.mpy`, and `differential_tests.py` exist and reproduce every
  evidence claim.
- Formal facts, mathematical adequacy reasoning, finite empirical evidence,
  trust assumptions, and exclusions are separated in this report.

## Trust boundary

| Trusted component | Why outside this theorem | Influence | Dependents | Evidence |
|---|---|---|---|---|
| Supplied read-only `reference-semantics/` and K v7.1.293 toolchain | They define and execute the logic in which the reachability theorem is checked. | Value, binding, control, state, exceptions, and proof execution. | All claims. | Exact LLVM/Haskell builds, concrete execution, positive proofs, and negative probes. No supplied file was modified. |
| Supplied `valSeqAt` `[total]` function | The reference semantics intentionally totalizes list access. The theorem uses only index `0` on a path known nonempty. Constructor equations fix every concrete in-bounds value; out-of-bounds behavior is irrelevant. | Selects `first`, hence comparisons and final result. | `moveSpec` and `move-one-ball`. | Nonempty guard, fixed semantics equations, concrete K tests, and independent differential tests. |
| Partial-correctness interpretation | K reachability proves the postcondition for terminating executions, not termination. | Termination only; no returned value is left unconstrained. | Both claims. | The loop structurally consumes a finite `ValSeq`, and all concrete/differential runs terminate, but no separate liveness theorem is claimed. |

No external sort, float primitive, digest, I/O operation, opaque
program-derived oracle, or trusted proof-local operational bridge is used by
the formal claims. Python `sorted` appears only in the independent finite test
oracle.

## Empirically supported facts

- The seven K concrete assertions in `concrete_tests.py` execute successfully
  under the required LLVM `MPY-KRUN` definition.
- The independent Python oracle reports no mismatch for the five named cases,
  all 5,914 permutations of `range(n)` for `0 <= n <= 7`, and all 1,093 lists
  of length `0` through `6` over `{-1, 0, 1}`.
- These runs support concrete semantics/intent alignment only. Universal
  program-to-summary correctness comes from the K claims, not from testing.

## Excluded behavior

- Non-integer elements are outside the formal precondition.
- Exceptional list access, mutation of `arr`, alias-sensitive identity,
  concurrency, I/O, and external state are outside the source program and
  theorem.
- The theorem does not model resource exhaustion or implementation limits.
- A separate termination proof is not included.
