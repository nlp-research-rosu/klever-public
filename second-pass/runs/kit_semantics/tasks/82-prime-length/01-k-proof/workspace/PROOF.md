VALIDATED

## What is proven

Under the supplied `MPY` reference semantics, the `prime_length` closure in
`spec.k`, when called with any semantic string `str(CS)` whose structural
length is nonnegative, returns `primeNat(isLen(CS))`. The closure body is the
constructor-for-constructor translation of `solution.py`; lookup, argument
evaluation, `len`, integer operations, the loop, assignments, return, and frame
pop all execute using the unmodified reference rules.

This is a partial-correctness result: every terminating execution in the stated
domain returns the specified Boolean. The K claim does not assert termination.

`primeNat(N)` is true exactly when `N >= 2` and none of the candidates
`2, 3, ..., N - 1` divides `N`. That is the standard characterization of a
prime natural number. Therefore the returned Boolean says exactly whether the
input string's length is prime.

## Formal claim

The entry claim is `SPEC.prime-length`:

```k
<k>
  Call(Name("prime_length"), str(CS:IntSeq))
  => primeNat(isLen(CS))
</k>
requires isLen(CS) >=Int 0
```

The claim pins `Name("prime_length")` to the exact `closureVal` body generated
from `solution.py`, starts in the module environment with the supplied builtin
scope, and requires the final heap, stack, return state, exception state, and
exit code to equal their initial values. The function-local frame is created
and removed by the fixed call semantics.

`SPEC.loop-invariant` starts at the semantics' actual recurring control term,
the exact `#while(condition, body)` from the solution. With `n = N`,
`divisor = D`, and `prime = P`, it establishes that the loop's final `prime`
value is `trialPrime(N, D, P)`. Its domain is `N >= 0` and `D >= 2`.

## Proof-extension inventory

No operational bridge, priority rule, simplification rule, concrete rule,
opaque oracle, or trusted primitive is added by `verification.k` or `spec.k`.
Every program-defined operation executes under the fixed semantics.

### `trialPrime(Int, Int, Bool)` and its three equations

- Class: definitional summary.
- Semantic role: reasons about the Boolean accumulated by the loop; it never
  matches or replaces a program computation.
- Domain: every proof use has `D >= 2`. The equations cover `D >= N`,
  `D < N` with `pyMod(N,D) == 0`, and `D < N` with
  `pyMod(N,D) =/= 0`.
- Matched context: a pure `trialPrime(N,D,P)` term only; there is no
  continuation, binding, stack, or framed cell.
- Justification scope and containment: all integers `N,D` and Booleans `P`
  satisfying the selected guard. The three guards are exhaustive on `D >= 2`
  and pairwise disjoint. `D >= 2` excludes a zero divisor.
- State footprint: none.
- Value influence: supplies the loop claim's final `prime` value and,
  through `primeNat`, the entry claim's result.
- Value justification: the base equation returns the accumulated flag once
  there are no candidates left. Each step examines exactly the current `D`;
  a divisor makes the flag false, otherwise the flag is preserved. The
  recursive measure `N - D` strictly decreases while `D < N`.
- Dependents: `SPEC.loop-invariant`, `primeNat`, and
  `SPEC.prime-length`.
- Control validation: not applicable because this extension does not replace
  control.
- Value validation: the universal entry theorem connects fixed execution to
  the summary. Ground fixed-semantics executions produce distinct results at
  lengths 2 and 4; both opposite results are rejected by the mutation claims.

### `primeNat(Int)` and its unguarded equation

- Class: definitional summary.
- Semantic role: names the initial trial-division state
  `trialPrime(N, 2, N >= 2)`; it does not replace execution.
- Domain: all integers; its single unguarded equation is exhaustive.
- Matched context and justification scope: a pure `primeNat(N)` term for any
  integer `N`; there are no operational cells or frames.
- State footprint: none.
- Value influence: it is the entry claim's result.
- Value justification: `N >= 2` supplies the required lower bound for
  primality, and `trialPrime` checks every possible proper divisor.
- Dependents: `SPEC.prime-length`.
- Control validation: not applicable.
- Value validation: `SPEC.prime-length` is a universal execution connection;
  the two opposite-result probes and the independent finite differential test
  provide additional sensitivity evidence.

### `SPEC.loop-invariant`

- Class: derived reachability lemma/circularity.
- Semantic role: proves the fixed `#while` execution; it adds no operational
  rewrite.
- Domain: `N >= 0`, `D >= 2`, `P:Bool`, `S:Str`, environment 1, and the exact
  local scope containing `string`, `n`, `divisor`, and `prime`.
- Matched context: the exact recurring `#while` term and body, with the active
  continuation framed by `<k> ... </k>`. Other scope entries and all omitted
  configuration cells are framed and preserved by the reachability claim.
- Justification scope and containment: identical to the claim's match domain;
  there is no separate broadly matching rewrite.
- State footprint: the loop reads `n`, `divisor`, and `prime`; it writes only
  `divisor` and possibly `prime`. `string`, the continuation, environment,
  heap, stack, return state, exception state, and exit code are preserved.
- Value influence and justification: its final `prime` value is fixed by the
  exhaustive `trialPrime` equations.
- Dependents: `SPEC.prime-length`.
- Control validation: the focused invariant proof printed `#Top`; the final
  unfiltered proof re-proved it together with the entry claim. No bridge is
  present, so fixed-versus-extended bridge comparison is inapplicable.
- Value validation: lengths 2 and 4 give true and false respectively under
  fixed execution, and the opposite claims fail.

## Reproduction commands and actual outputs

`prove.sh` is the exact end-to-end runner. It completed with exit status 0.

Artifact generation and independent evidence:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete-smoke.py > concrete-smoke.mpy
python3 evidence.py
```

Actual output, exit 0:

```text
artifact identity: solution.mpy regenerated exactly
concrete smoke function AST: identical to solution.py
prompt examples: 4 passed
differential domain: string lengths 0..200
oracle: independent trial division through floor(sqrt(n))
mismatches: 0
```

Concrete LLVM build and execution:

```bash
kompile reference-semantics/semantics.k --backend llvm \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete-smoke.mpy --definition runtime-kompiled \
  | tee concrete-smoke.out
rg -U '<exc>\s+NoExc\s+</exc>' concrete-smoke.out
rg -U '<exit-code>\s+0\s+</exit-code>' concrete-smoke.out
```

Actual exit statuses were 0. The final configuration in
`concrete-smoke.out` contains:

```text
<k> .K </k>
<exc> NoExc </exc>
<exit-code> 0 </exit-code>
```

The LLVM compiler emitted warnings about non-exhaustive functions in unrelated
list, float, method, and subscript paths, plus unused variables in string
comparison rules. It still exited 0; none of those functions is reachable from
this program's `len(str)`, integer arithmetic, comparison, assignment, loop,
or call path.

Symbolic build and the required positive proof:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC \
  | tee positive-proof.out
rg -x '#Top' positive-proof.out
```

Actual output and status:

```text
#Top
```

`kprove` exited 0. This unfiltered command proves both claims in `SPEC`; the
entry claim uses the loop claim as a circularity.

Negative result-sensitivity commands:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.length-two-not-prime
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.length-four-prime
```

Both commands exited 1 as required. The first residual has `<k> true ~> .K`
against a false destination; the second has `<k> false ~> .K` against a true
destination. Both logs begin with `Warning (WarnStuckClaimState)` and end with
`[Error] Prover: backend terminated because the configuration cannot be
rewritten further.` Exact outputs are in `vacuity-two.log` and
`vacuity-four.log`.

Body-sensitivity command:

```bash
kprove spec-body-mutation.k --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION \
  --claims SPEC-BODY-MUTATION.mutated-length-two
```

This replaces the function body with `return False` but retains the true
length-two destination. It exited 1 as required. `body-mutation.log` contains
`WarnStuckClaimState` and the residual `<k> false ~> .K`.

## Gate results

### Gate A — PASS

- A1: `Call(Name("prime_length"), ...)` performs real lookup of the exact
  closure body. No rule intercepts the call. The body mutation is rejected.
- A2: there are no operational bridges. The entry claim observes and preserves
  the heap, heap allocator, stack, return state, exception state, and exit
  code. Function locals are removed by the fixed frame-pop rule.
- A3: fixed rules perform callee lookup, argument evaluation, builtin lookup,
  parameter binding, left-to-right expression evaluation, loop control, return,
  and frame restoration. The invariant matches the exact recurring `#while`
  context and preserves its continuation.
- A4: the proof-local equations are exhaustive on every use, their guards are
  disjoint, the divisor is nonzero, and recursion advances `D`.
- A5: `str(iCons(97,iCons(98,.IntSeq)))` is a realizable length-two witness.
  Its false-result mutation fails. A distinct length-four witness returns
  false, and its true-result mutation also fails.

### Gate B — PASS

- B1: the prompt requires a string. The formal domain is every finite
  `str(CS:IntSeq)`; `isLen(CS) >= 0` is a structural invariant of all such
  terms, not an excluded class of strings. Non-string Python values are
  outside the prompt and theorem.
- B2: the program uses only string length, mathematical integers, Booleans,
  and local control. The semantic string stores one sequence element per
  abstract character for the formal input, so character values do not affect
  the result. Concrete `Str` literals in the supplied semantics are ASCII-only,
  but literal construction is not part of the formal call boundary.
- B3: `trialPrime` scans every integer from 2 through `N-1`, retaining true
  exactly when none divides `N`, with `N >= 2` required initially. This is
  precisely the standard prime-number property, not merely an empirical name
  for the program result.
- B4: the implementation, formal summary, four prompt examples, and boundary
  cases agree.

### Gate C — PASS

- C1: the trust ledger below names every component outside the theorem and its
  influence.
- C2: all claimed generated artifacts, concrete tests, differential tests,
  positive output, mutation specs, and logs exist. `prove.sh` reproduces them
  and enforces their statuses.
- C3: formal, conditional, empirical, and excluded conclusions are separated
  in this report.

## Trust boundary

- `reference-semantics/`: fixed, supplied operational semantics. It affects
  value, control, state, and exceptions in both formal claims. Every claim
  depends on it. It is not proved equivalent to CPython here; the theorem is
  explicitly conditional on it. Evidence: required LLVM execution of the exact
  solution body and agreement with CPython/oracle cases.
- K v7.1.293, its Haskell reachability backend, and its SMT reasoning are
  trusted to implement the reported `#Top` result. All claims depend on this
  toolchain. Evidence: successful compilation, positive proof, and
  discriminating negative probes.
- Mathematical integer arithmetic and the standard characterization of
  primality by absence of divisors in `2..N-1` are the interpretation used for
  intent adequacy. They affect the human-facing meaning, not program control.

There is no task-local trusted primitive, opaque value, or operational bridge.

## Empirically supported facts

- The four prompt examples pass in CPython.
- CPython execution of `solution.py` agrees with an independently written
  square-root trial-division oracle for every string length from 0 through 200,
  with zero mismatches.
- LLVM `krun` executes an AST-identical copy of the function on ten cases:
  lengths 0, 1, 2, 3, 5, 6, 7, 7, 11, and 12. All assertions terminate with
  `NoExc` and exit code 0.
- These finite checks support translation and model adequacy only; the
  universal result comes from `kprove`, not from testing.

## Excluded behavior

- Inputs that are not Python strings.
- Total-correctness/termination as a formal K claim. The implementation plainly
  advances `divisor` from 2 to `n`, but the reachability theorem is partial
  correctness.
- Complexity or resource bounds.
- A proof that the supplied reference semantics or the K/SMT implementation is
  itself correct.
- Concrete non-ASCII string-literal translation, which the supplied semantics
  does not support. The formal function-input theorem is over arbitrary
  semantic strings and depends only on their sequence length.
