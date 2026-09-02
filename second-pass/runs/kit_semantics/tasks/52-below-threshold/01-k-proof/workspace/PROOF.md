VALIDATED

# Proof report

## What is proven

`solution.py` implements `below_threshold(l, t)` by returning `False` at the
first element for which `e < t` is false and returning `True` after exhausting
the list. `solution.mpy` is generated from that file by the supplied
`py2mpy.py`.

Under the supplied MPY semantics, loading that exact function and calling it
with any K `Int` threshold and any arbitrary finite list of modeled numbers
(`Int`, `Bool`, or `Float`, in any mixture) reaches a normal final state whose
result is true exactly when every element is below the threshold. The proof is
not bounded by list length.

## Formal claim

`spec.k` partitions the complete represented domain into four exhaustive
claims:

1. the empty `ValSeq`;
2. a nonempty sequence headed by an `Int`;
3. a nonempty sequence headed by a `Bool`;
4. a nonempty sequence headed by a `Float`.

Each nonempty claim leaves `REST:ValSeq` symbolic and assumes
`numericSeq(REST)`, so the tail may have arbitrary finite length and arbitrary
numeric mixtures. The postcondition is:

```k
allBelow(.ValSeq, T) = true
allBelow(vCons(V, REST), T)
  = numericLt(V, T) andBool allBelow(REST, T)
```

`numericLt` is the supplied comparison dispatch specialized to an integer
threshold:

```k
Int:   I <Int T
Bool:  boolAsInt(B) <Int T
Float: ltFI(F, T)
```

Thus the summary-to-property bridge is definitional, while the auxiliary loop
claims prove that the source program computes that summary.

## Proof-extension inventory

### Definitional summaries in `base-verification.k`

- `numericVal` recognizes exactly K `Int`, `Bool`, and `Float`.
- `numericSeq` recursively recognizes finite sequences containing only those
  values.
- `numericLt` has disjoint typed equations and an `[owise]` totalization. The
  totalization is never used by a positive target claim because every element
  is guarded by `numericVal`/`numericSeq`.
- `allBelow` descends structurally through one `ValSeq` constructor per step.
- `lastVisited` records the exact final local value of `e`, including
  short-circuit termination at the first failing element. It also descends
  structurally.

All equations are total over their declared K domains; typed cases are
disjoint, `[owise]` excludes their union, and every recursion decreases the
sequence tail.

### Derived comparison lemma

`verification-loops.k` adds:

```k
rule applyCmp("<", V:Val, T:Int) => numericLt(V, T)
  requires numericVal(V)
  [simplification]
```

`connection-spec.k` imports `VERIFICATION-BASE`, not this simplification, and
proves the `Int`, `Bool`, and `Float` cases against the fixed MPY dispatch.
Those claims normalize directly to the same fixed-semantic expressions. This
lemma affects the loop branch and therefore the result, but its complete
numeric domain is covered by the three connection claims.

### Operational bridges

`verification.k` contains four priority-40 operational bridges: empty and
nonempty cases for native `#loop`, and empty and nonempty cases for source
`For`.

Each bridge matches the exact:

- loop target and body;
- continuation
  `(Return(Bool(true)) .Stmts):Stmts ~> #endcall`;
- current environment and exact local bindings for `l`, `t`, and `e`;
- parent scope, scope allocation counter, call frame, return cell, exception
  cell, and exit code.

Arbitrary globals and heap contents are accepted but preserved. The bridges
perform the exact frame deletion, environment restoration, stack pop, and
`e` update stated by `lastVisited`; they do not admit a broader continuation
or exceptional/control context.

`loop-spec.k` proves the two `#loop` transitions without importing any
operational bridge. Its two `For` claims are then proved from one fixed
`For` rewrite plus those already-proved loop claims. In the second proof
invocation, `--trusted` is used only as proof composition for the two loop
claims that the immediately preceding invocation independently closed with
`#Top`. The four rules in `verification.k` reproduce the proved claim
configurations and guards exactly.

Dependence is:

```text
fixed MPY comparison rules
  -> connection-spec numeric cases
  -> derived applyCmp simplification
  -> bridge-free loop claims
  -> bridge-free For claims
  -> exact operational bridges
  -> four entry-point claims
```

## Commands and actual results

The complete reproducible command sequence is in executable `prove.sh`.
Running:

```bash
./prove.sh
```

completed with exit 0. Its material commands and actual results were:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
python3 py2mpy.py bridge-smoke.py > bridge-smoke.mpy
python3 differential.py
# checked=77777 mismatches=0

kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
# Exit 0; final <k> .K, <exc> NoExc, <exit-code> 0

kompile --backend haskell base-verification.k \
  --main-module VERIFICATION-BASE --syntax-module MPY-SYNTAX \
  --output-definition connection-kompiled
kprove connection-spec.k --definition connection-kompiled \
  --spec-module CONNECTION-SPEC
# #Top; exit 0

kompile --backend haskell verification-loops.k \
  --main-module VERIFICATION-LOOPS --syntax-module MPY-SYNTAX \
  --output-definition loop-verification-kompiled
kprove loop-spec.k --definition loop-verification-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons
# #Top; exit 0

kprove loop-spec.k --definition loop-verification-kompiled \
  --spec-module LOOP-SPEC \
  --claims LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons,LOOP-SPEC.for-empty,LOOP-SPEC.for-cons \
  --trusted LOOP-SPEC.loop-empty,LOOP-SPEC.loop-cons
# #Top; exit 0

kompile --backend haskell verification.k \
  --main-module VERIFICATION --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
# #Top; exit 0
```

The compiler emitted only warnings from the supplied semantics and unused
symbolic state variables; no positive command exited nonzero.

The boundary comparison in `prove.sh` ran `bridge-smoke.mpy` once with the
fixed LLVM definition and once with the bridge-enabled Haskell definition,
then diffed the complete final configurations. `diff -u` produced no output
and exited 0.

The two negative commands were:

```bash
kprove spec-vacuity.k --definition verification-kompiled \
  --spec-module SPEC-VACUITY
# exit 1; WarnStuckClaimState; residual <k> false ~> .K while RHS demanded true

kprove spec-mutation.k --definition verification-kompiled \
  --spec-module SPEC-MUTATION
# exit 1; WarnStuckClaimState; residual <k> true ~> .K while RHS demanded false
```

## Gate results

### Gate A — PASS

- Program identity: `spec.k` loads the same parameters, docstring, assignment,
  loop body, comparison, returns, and statement-list structure generated in
  `solution.mpy`.
- Every result-bearing summary has exhaustive truthful equations or a
  bridge-free machine-checked connection.
- The loop and `For` operational bridges have universal bridge-free connection
  claims over their exact match domains, including control and state.
- Fixed and bridge-enabled ground executions with both true and false outcomes
  produced byte-identical complete final configurations.
- `spec-mutation.k` changes `<` to `<=`; the exact bridge no longer matches,
  fixed execution produces `true` for `[5], 5`, and the original required
  result `false` is rejected. This establishes body and operational
  sensitivity.
- `spec-vacuity.k` asks the unmodified program to return `true` for `[5], 5`;
  the prover exposes the actual `false` residual and exits 1. This establishes
  result constraint and non-vacuity.

### Gate B — PASS

The HumanEval contract asks whether all numbers in an arbitrary list are below
an integer threshold. The theorem covers empty and arbitrary finite,
heterogeneous lists of every numeric class represented by the supplied
semantics for which ordering against an integer is defined: `Int`, `Bool`, and
`Float`. It imposes no size bound and matches Python's strict `<`, including
equality returning false.

Nonnumeric represented values are not silently excluded from a defined
behavior: their comparison with an integer has no MPY `applyCmp("<", _, Int)`
case, corresponding to the source computation being undefined rather than
returning a Boolean. Numeric classes not represented by MPY are a supplied
model boundary, not a proof-introduced list restriction.

### Gate C — PASS

All claimed proof, concrete, differential, bridge-comparison, and mutation
artifacts exist and are run by `prove.sh`. Universal facts are attributed to K
claims; finite evidence is reported only as empirical support. The trust
boundary below names every unproved component and its dependents.

## Trust boundary

- **Supplied reference semantics.** The MPY rules, including loading, calls,
  scopes, iteration, control transfer, comparison dispatch, and primitive K
  hooks, are assumed to model the requested Python subset. Every proof claim
  depends on this semantics.
- **K toolchain.** `kompile`, `krun`, `kprove`, the LLVM backend, and the
  Haskell backend are trusted to implement their stated K behavior.
- **Translator.** The supplied, fixed `py2mpy.py` is trusted to translate the
  inspected Python AST to the displayed constructors. Regeneration is the
  first step of `prove.sh`; neither input file is modified.
- **`ltFI(Float, Int)`.** The supplied semantics intentionally marks this
  exact mixed comparison total and opaque to symbolic proof, with concrete
  rules for LLVM execution. It controls the float loop branch and therefore
  the float-headed claim and any numeric tail containing floats. The theorem
  is parametric in that named fixed primitive: it proves that the program
  returns the recursive conjunction of the supplied `ltFI` results. It does
  not independently claim CPython equivalence for NaN, infinities, signed
  zero, or representation extremes.
- **Proof composition.** The second `loop-spec.k` command marks only
  `loop-empty` and `loop-cons` trusted while proving `for-empty` and
  `for-cons`; those exact claims are machine-proved with `#Top` by the previous
  command. No unproved program property is introduced by that composition.

## Empirical support

- `differential.py` uses Python's independent
  `all(value < threshold for value in values)` as its oracle. It exhaustively
  checks all lengths 0 through 4 over ten representative integer, Boolean, and
  finite-float values, with thresholds -3 through 3: 77,777 cases, zero
  mismatches.
- `smoke.py` runs the two prompt examples plus empty-list, equality-boundary,
  Boolean, and finite-float cases through the supplied LLVM semantics. It
  terminates normally with every assertion satisfied.
- `bridge-smoke.py` covers empty, both prompt outcomes, equality, and Boolean
  coercion. Fixed and bridge-enabled runs agree on every printed final cell.
- The float universal connection is machine-checked symbolically through the
  fixed `applyCmp`/`ltFI` dispatch. A bridge-enabled concrete float comparison
  is not claimed: this Haskell backend lacks the concrete `FLOAT.isNaN` hook;
  finite-float concrete evidence therefore comes from the required LLVM
  execution.

## Excluded behavior

- Calls whose threshold is not a K `Int` are outside the annotated entry-point
  contract.
- Lists containing strings, `None`, containers, or other nonnumeric MPY values
  are outside the natural-language “numbers” domain and make `< int` undefined
  in the supplied semantics.
- Python numeric/value classes absent from the supplied MPY model are outside
  this semantics' representation boundary.
- No claim of independently checked CPython fidelity is made for exceptional
  float edge values; the universal float result is conditional on the supplied
  `ltFI` contract.
