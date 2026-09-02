VALIDATED

# What is proven

Under the supplied `MPY` reference semantics, the exact translated
`string_sequence` function is partially correct for every mathematical integer
input `N`.

- If `N < 0`, the return value is the empty string.
- If `N >= 0`, the return value is the ASCII string
  `0 1 ... N`, with one space between adjacent decimal integers.
- The entry claim also checks normal call/return cleanup: the environment,
  scope allocator, heap, heap allocator, stack, return cell, exception cell,
  and exit code have their expected final values.

This is a partial-correctness theorem: the reachability proof establishes the
result whenever the computation terminates. It does not separately prove
termination.

# Formal claims

`spec.k` contains two claims, both proved together.

1. `SPEC.loop-invariant` starts at the semantics' actual recurring `#while`
   term. With local values `n = N`, `i = I`, and `result = str(ACC)`, where
   `I >= 1` and `N >= 0`, it consumes the loop and changes `result` to
   `str(sequenceAcc(ACC, I, N))`. The final `i` is intentionally existential
   because the function frame is immediately discarded and `i` is not
   observable.
2. `SPEC.string-sequence` starts from the initial MPY configuration, loads the
   exact function body represented in `solution.mpy`, resolves and invokes its
   binding with symbolic integer `N`, and returns
   `str(stringSequenceCodes(N))`.

The entry claim has no `requires` clause, so its formal input domain is all K
`Int` values.

# Proof-extension inventory

## `sequenceAcc`

- Extension: `sequenceAcc(IntSeq, Int, Int)` and its two concrete defining
  equations.
- Class: definitional summary.
- Semantic role: names the result of the loop; it does not rewrite a program
  AST, call, continuation, or configuration.
- Domain: every `ACC:IntSeq`, `I:Int`, and `N:Int`. The guards `I >Int N` and
  `I <=Int N` are disjoint and exhaustive.
- Matched context: only a `sequenceAcc` function term. No continuation, stack,
  binding, or cell is matched or omitted.
- Justification scope and containment: the base equation returns `ACC` when
  the loop guard is false. The step equation applies exactly the source body's
  two string concatenations and fixed-semantics decimal conversion
  `strToCodes(Int2String(I))`, then increments `I`. Its concrete recursion
  terminates because `I` increases by one until `I > N`.
- State footprint: none; this is a mathematical character-sequence function.
- Value influence: the loop result and final postcondition.
- Value justification: exhaustive guarded equations plus the machine-checked
  `SPEC.loop-invariant`, which connects the exact fixed-semantics loop
  execution to this value.
- Dependents: both claims.
- Control/value validation: no operational control is replaced. Concrete MPY
  execution, the comma-body mutation, the false-result mutation, and the
  differential test provide the recorded witnesses below.

## Symbolic base rule for `sequenceAcc`

- Extension: `sequenceAcc(ACC, I, N) => ACC` when `I >Int N`.
- Class: derived lemma.
- Semantic role: symbolic form of the concrete base equation; it reasons about
  a summary term only.
- Domain and matched context: exactly the guarded function term; no cells or
  continuation.
- Justification: identical to the base defining equation.
- Overlap: it overlaps the concrete base equation only with the same right-hand
  side.
- Dependents: `SPEC.loop-invariant`.

## Inductive fold rule for `sequenceAcc`

- Extension: folding
  `sequenceAcc(updated(ACC,I), I +Int 1, N)` to
  `sequenceAcc(ACC, I, N)` when `I <=Int N`, where `updated` is the exact pair
  of source string concatenations.
- Class: derived lemma.
- Semantic role: folds a mathematical summary; it does not skip source
  execution.
- Domain and matched context: every summary term of the displayed exact shape
  under `I <=Int N`; no K continuation, binding, or state cell is accepted.
- Justification: symmetry of the concrete step defining equation over the same
  guard.
- State footprint: none.
- Value influence: allows the invariant's inductive branch to match its
  destination.
- Dependents: `SPEC.loop-invariant`, and transitively the entry claim.

## `stringSequenceCodes`

- Extension: `stringSequenceCodes(Int)` and its two equations.
- Class: definitional summary.
- Semantic role: names the final result; it does not replace execution.
- Domain: every `N:Int`; `N <Int 0` and `N >=Int 0` are disjoint and exhaustive.
- Meaning: negative inputs map to `.IntSeq`; nonnegative inputs start with the
  code for `"0"` and use `sequenceAcc` from `1` through `N`.
- State footprint: none.
- Value influence: the entry claim's returned string.
- Value justification: the exhaustive definition and the entry reachability
  claim's connection to fixed execution.
- Dependents: `SPEC.string-sequence`.

## Reachability circularity

- Extension: `SPEC.loop-invariant`.
- Class: derived reachability lemma/circularity.
- Matched context: the exact `#while` condition and body, exact function
  binding/body, current environment `1`, and exact local scope. The active
  continuation and unrelated configuration cells are framed.
- Context containment: the fixed loop has no `break`, `continue`, `return`,
  exception-producing modeled operation, heap mutation, or stack operation.
  It reads `n` and `i`, writes only `result` and `i`, and performs normal
  builtin `str` lookup through the pinned scope chain. Therefore the theorem is
  equally general in every framed continuation/cell it accepts.
- State footprint: reads local `n`, `i`, and `result`; writes local `i` and
  `result`; preserves the pinned scope structure and every framed cell.
- Value justification: the loop body executes under the unmodified MPY rules;
  the claim itself is proved as part of the successful all-claims run.
- Dependents: `SPEC.string-sequence`.

There are no operational bridges, priority rules, result-bearing oracles, or
proof-local trusted primitives in `verification.k`.

# Reproducible commands and actual results

The complete recorded workflow is:

```bash
./prove.sh
```

`prove.sh` runs these positive proof steps:

```bash
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py smoke.py > smoke.mpy
kompile --backend llvm reference-semantics/semantics.k \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun smoke.mpy --definition runtime-kompiled
kompile --backend haskell verification.k \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
kprove spec.k --definition verification-kompiled --spec-module SPEC
```

Actual results:

- `kompile` LLVM: exit 0.
- `krun`: exit 0; final `<k>` is `.K`, `<exc>` is `NoExc`, and
  `<exit-code>` is `0`.
- `kompile` Haskell: exit 0.
- all-claims `kprove`: output `#Top`; exit 0.

The supplied semantics emits compiler warnings about unrelated total functions
and unused variables. They do not occur on this function's execution path and
did not change any command's exit status.

# Gate A — PASS

## A1: program identity and body sensitivity

The entry claim loads and calls the exact `FuncDef` AST generated in
`solution.mpy`. `prove.sh` regenerates that file and also checks that
`smoke.py` begins with a byte-identical copy of `solution.py`.

`spec-body-mutation.k` changes the loop separator from space (ASCII 32) to comma
(ASCII 44), keeps the original postcondition, and uses the satisfiable witness
`N = 1`.

```bash
kprove spec-body-mutation.k \
  --definition verification-kompiled \
  --spec-module SPEC-BODY-MUTATION
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual return value is
the character sequence for `"0,1"`, including `iCons ( 44 , ...)`, so the
connection is materially body-sensitive.

## A2/A3: state, binding, evaluation, and control

No operational bridge exists. The entry claim pins the module binding to the
exact closure body and lets MPY execute lookup, argument evaluation, parameter
binding, local updates, builtin `str` lookup/conversion, return, frame popping,
and cleanup. All observable configuration cells are constrained in the entry
claim.

## A4: logical consistency

The two defining guards of each total function are pairwise disjoint and
exhaustive. The duplicate symbolic base equation agrees with the concrete base
equation on their overlap. The fold lemma is the reverse direction of the
guarded step equation and is therefore equal-valued everywhere it applies.
Concrete `sequenceAcc` recursion strictly reduces `N - I + 1` while positive.

## A5: realizability and non-vacuity

The entry precondition is satisfiable; for example, `N = 0`. The distinct
mutation in `spec-vacuity.k` falsely requires the result at `N = 0` to be `""`.

```bash
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY
```

Actual result: exit 1 with `WarnStuckClaimState`. The residual return value is
`str ( iCons ( 48 , .IntSeq ) )`, namely `"0"`. Thus the return value is
genuinely constrained.

# Gate B — PASS

- Input-domain alignment: the theorem accepts all integer inputs. For every
  nonnegative `n`, it states exactly the prompt's inclusive sequence. Negative
  inputs are not specified by the prompt; the implementation additionally
  defines them to return `""`, matching Python's empty `range(n + 1)`.
- Language-model adequacy: K `Int` and Python integers are unbounded. The
  supplied string model is ASCII-only, but every generated character is a
  decimal digit, space, or (only inside integer conversion) minus sign, all
  ASCII. The formal domain excludes non-integer calls, consistent with the
  annotated signature.
- Summary-to-property adequacy: `stringSequenceCodes` starts with `"0"` and
  its step appends exactly one space and the fixed-semantics decimal rendering
  of each successive integer through `N`.
- Implementation-to-intent alignment: the prompt examples for `0` and `5`
  are present in the concrete MPY smoke artifact and pass.

# Gate C — PASS

## Trust ledger

- The supplied, read-only `reference-semantics/` definition is the fixed
  execution model. In particular, `Int2String`, `strToCodes`, builtin lookup,
  function call/return, and string concatenation affect the proved value and
  control. Both claims depend on this task-provided semantics.
- The K 7.1.293 compiler, Haskell backend, LLVM backend, SMT reasoning, and
  host runtime form the machine-checking trusted base.
- `py2mpy.py` is the task-provided translation boundary. `prove.sh` regenerates
  `solution.mpy`; the theorem directly embeds the resulting AST shape.
- There are no additional proof-local trusted assumptions or operational
  abstractions.

## Concrete and differential evidence

`smoke.py`/`smoke.mpy` executes the exact function body under LLVM for
`-2`, `0`, `5`, and `12`. Its oracle consists of explicit expected strings,
including both prompt examples and a multi-digit boundary. All assertions pass,
and MPY exits with code 0.

`differential_test.py` independently constructs the oracle with Python
`range`, `str`, and `" ".join`, rather than the K summary equations:

```bash
python3 differential_test.py
```

Actual output:

```text
inputs=277 range=-25..250 plus 999
mismatches=0
```

This finite evidence supports the implementation-to-intent and execution-model
bridges on the tested inputs; it is not used as a universal proof.

# Excluded behavior

- Calls with non-integer arguments are outside the formal claim.
- Total termination, resource usage, and performance are not proved.
- Correctness is relative to the supplied MPY semantics, translator, K
  toolchain, and backend trusted base listed above.
