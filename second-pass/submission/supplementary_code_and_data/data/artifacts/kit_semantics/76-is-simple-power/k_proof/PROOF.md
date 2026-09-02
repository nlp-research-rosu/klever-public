VALIDATED

## What is proven

Under the supplied `MPY` semantics, calling the exact translated body of
`is_simple_power` with any two K `Int` values `X` and `N` returns
`simplePower(X, N)`.  The predicate is the integer-power property

`there exists an integer exponent e >= 0 such that N**e == X`.

The K result is a partial-correctness result.  Termination for this particular
program also follows mathematically: all degenerate bases return before the
loop, and every taken loop iteration for `|N| >= 2` exactly divides a nonzero
`X` by `N`, strictly decreasing its absolute value until the guard is false.

## Formal claims

`spec.k` has two claims:

1. `SPEC.loop-invariant` starts at the supplied semantics' recurring `#while`
   configuration.  Its actual local frame contains exactly `x` and `n`.
   Assuming `x != 0` and `|n| >= 2`, it establishes that the final
   `x == 1` exactly when `simplePower` held of the loop-entry values.
2. `SPEC.is-simple-power` invokes the exact closure body translated from
   `solution.py`.  It constrains the returned Bool to
   `simplePower(X, N)` for all mathematical integers, with every final
   configuration cell preserved exactly.

The loop obligations are:

- Base: if `pyMod(X, N) != 0`, the loop exits without changing `X`; only
  `X == 1` represents exponent zero.
- Step: if `pyMod(X, N) == 0`, the body stores `X / N`; the circularity
  applies at the next loop head, and exact-factor folding re-establishes the
  original summary.
- Entry discharge: the five branches handle `x == 1`, bases `0`, `1`, and
  `-1`, and `x == 0`; the remaining path establishes the invariant's
  `x != 0` and `|n| >= 2` precondition.

## Proof-extension inventory

### `simplePower(Int, Int)` equations

- Class: definitional summary.
- Semantic role: names the intended mathematical result; it never matches or
  replaces a Python computation.
- Domain: all pairs of K integers.
- Matched context: only a `simplePower` term; no continuation, call stack,
  binding, or configuration cell is matched.
- Coverage: `X == 1`; then, under `X != 1`, bases `0`, `1`, and `-1`; then
  `|N| >= 2`, split into `X == 0` or nonzero and exact/non-exact divisibility.
- Overlap: the guarded partitions are disjoint.  The factor-fold
  simplification overlaps the recursive equation only with the same result.
- Descent: on the recursive domain, exact division by a base of magnitude at
  least two strictly decreases `abs(X)`; `X == -1` is not exactly divisible
  there.
- State footprint and control: none.
- Value influence: fixes the target Bool and the loop invariant's final-state
  relation.
- Value justification: exponent-zero and degenerate-base cases are explicit;
  otherwise `N**e == X` for `e > 0` iff `N` divides `X` and
  `N**(e-1) == X/N`.
- Dependents: both claims.
- Validation: the complete K proof, 5,025 independent differential cases,
  concrete MPY execution, and the rejected false-result mutation.

### Nondivisible-base simplification

- Exact extension:
  `((X ==Int 1) ==Bool simplePower(X,N)) => true` when `|N| >= 2` and
  `pyMod(X,N) != 0`.
- Class: derived lemma.
- Semantic role and matched context: simplifies only this mathematical Bool
  equality; it matches no operational term or cell.
- Justification scope: on the guard, `X == 0` is impossible.  `X == 1` is the
  exponent-zero case; every other value is false by the exhaustive
  nondivisible equation.
- State footprint/control: none.
- Value influence: discharges the loop base obligation.
- Dependents: `SPEC.loop-invariant`, hence the entry claim.
- Validation: the focused invariant proof prints `#Top`; the false-result
  probe is rejected.

### Exact-factor simplification

- Exact extension:
  `simplePower(X,N) => simplePower(X /Int N,N)` when `X != 0`,
  `|N| >= 2`, and `pyMod(X,N) == 0`.
- Class: derived lemma.
- Semantic role and matched context: normalizes a mathematical summary in the
  form produced by operational floor division; it does not rewrite `BinOp`,
  `#while`, lookup, assignment, return, or any configuration cell.
- Justification scope: exact divisibility makes Python floor division equal
  to mathematical `X/N`; the guard also implies `X != 1`, so this is exactly
  the recursive defining equation.
- Context containment/state/control: no operational context or state is
  matched.
- Value influence: discharges the loop inductive obligation.
- Dependents: `SPEC.loop-invariant`, hence the entry claim.
- Validation: equation overlap has the same right-hand side, the focused
  invariant proof prints `#Top`, and the independent multiplier oracle has
  zero mismatches.

### `SPEC.loop-invariant`

- Class: machine-checked derived reachability lemma/circularity.
- Semantic role: reasons about the fixed `#while` execution; it is not an
  operational rewrite in `verification.k`.
- Domain and matched context: `X != 0`, `|N| >= 2`, exact local frame
  `x |-> X`, `n |-> N`, parent scope `0`, any environment location `L`,
  and the framed continuation and otherwise preserved configuration.
- Justification scope/context containment: the claim is proved over exactly
  that framed domain by the fixed semantics.  The loop reads `x,n`, writes
  only local `x`, and preserves the continuation and all other cells.
- Value influence: relates final local `x` to the mathematical predicate.
- Dependents: `SPEC.is-simple-power`.
- Control/value validation: fixed semantics executes the condition, body,
  back-edge, and exit.  The claim itself and the complete claim set both
  print `#Top`; changing the source's first return changes the concrete result
  and is rejected.

There are no operational bridges, trusted opaque primitives, priority
shortcuts, call interceptions, or proof-local abrupt-control rules.

## Reproducible commands and actual results

The complete executable record is `prove.sh`; the final end-to-end run exited
0.  Its positive proof commands are:

```bash
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC \
  --claims SPEC.loop-invariant
# Actual stdout: #Top
# Actual exit: 0

kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
# Actual stdout: #Top
# Actual exit: 0
```

The concrete definition used the required command:

```bash
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
```

Actual `krun` result: exit 0, `<k> .K </k>`, `<exc> NoExc </exc>`, and
`<exit-code> 0 </exit-code>`.  Compiler warnings concern unrelated supplied
semantic functions and unused `As`/`Bs` variables in `str.k`; both compiler
commands exit 0.

Translation is reproducible:

```bash
python3 py2mpy.py solution.py > solution.mpy
```

Regeneration compared byte-for-byte equal (`cmp` exit 0).

The result mutation command is:

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`; its residual contains
`<k> true ~> .K </k>` while the deliberately false destination is `false`.

The body-sensitivity command is:

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`; changing the `x == 1`
branch to return false leaves `<k> false ~> .K </k>` against destination
`true`.

## Gate results

- Gate A — PASS.  The exact program body executes through fixed semantics;
  lookup, argument order, frame push/pop, branches, integer operators, loop,
  assignment, and return are not bypassed.  The equations are exhaustive and
  consistent.  The precondition is realizable, and both result and body
  mutations are rejected.
- Gate B — PASS.  The formal domain is every integer pair, matching the
  integer-power task and all examples.  K `Int` is unbounded like CPython
  `int`; supplied `pyMod` and floor division cover negative divisors.  The
  summary-to-property bridge is the standard exact-factor characterization,
  and the implementation handles the degenerate bases consistently.
- Gate C — PASS.  All commands and artifacts exist, the trust boundary and
  exclusions are explicit, the differential oracle is independent, and all
  claimed outputs and exit statuses were observed.

## Trust boundary

The proof trusts the supplied read-only `reference-semantics/`, K's compiler,
Haskell backend, SMT solver, and their implementation of mathematical integer
hooks.  No supplied opaque float, sorting, digest, or other trusted primitive
is reached by this program.  The human-facing interpretation of the recursive
predicate uses the elementary factor/exponent argument above and is supported,
but not replaced, by finite differential evidence.

The theorem is partial correctness.  The separate decreasing-absolute-value
argument supplies termination reasoning but is not a K liveness theorem.

## Empirical evidence

`python3 differential_test.py` uses multiplication to enumerate `N**e`
independently of the solution's division algorithm.  It covers every
`x` in `[-100,100]` and every `n` in `[-12,12]`.

Actual output:

```text
cases=5025 mismatches=0
```

`smoke.py` contains the six prompt examples plus zero, negative-one, and
negative-base boundaries.  `differential_test.py` checks that the function AST
in that smoke artifact is identical to `solution.py`; all assertions complete
under the LLVM MPY semantics.

## Excluded behavior

The formal input sort is K `Int`.  Non-integer Python numerics, strings,
user-defined numeric protocols, subclasses such as `bool`, resource bounds,
and behavior outside the supplied MPY subset are not claimed.  No exceptions
or external state are part of the intended function behavior.
