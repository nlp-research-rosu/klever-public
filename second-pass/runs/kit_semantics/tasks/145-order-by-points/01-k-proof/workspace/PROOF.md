VALIDATED

## What is proven

All three claims in `spec.k` were proved by `kprove`; the combined command
printed `#Top` and exited 0.

Under the supplied MPY semantics, for every finite `ValSeq` whose elements are
K `Int` values:

1. `digit_sum(n)` executes its real translated body and returns
   `signedDigitSum(n)`.
2. `order_by_points(nums)` resolves the module-level `digit_sum` binding,
   resolves the builtin `sorted` binding, and returns a freshly allocated list
   containing
   `sortKeyVS(nums, closureVal("number", digitSumBody, 0))`.
3. `signedDigitSum` gives ordinary decimal digit sum for nonnegative integers.
   For a negative integer it negates the leading decimal digit and adds the
   remaining digits. Thus `-12` has key `-1 + 2 = 1`, as required by the prompt
   example.

The source-level conclusion that the returned list is a stable ascending sort
by those keys is conditional on the supplied semantics' named contract for the
external primitive `sortKeyVS`. The K proof does not pretend to derive the
ordering behavior of that opaque primitive. The fixed LLVM concrete leg calls
the real key closure and stable-inserts its results; the recorded tests provide
finite evidence for that trust boundary.

This is a partial-correctness proof. It establishes the result whenever the
modeled computations terminate; it is not a machine-checked termination proof.

## Formal claims

`SPEC.digit-sum-loop`

- Starts at the exact `#while` loop head in environment 1 with local bindings
  `number = N`, `sign = SIGN`, and `total = S`, where `N >= 0`.
- Ends with `number = leadingDigit(N)` and
  `total = lowerDigitSumAcc(N, S)`.
- Accepts an arbitrary continuation and arbitrary framed cells; the theorem
  itself is proved at exactly that generality. The loop body neither inspects
  nor abruptly discards the suffix.

`SPEC.digit-sum-function`

- Loads the exact two definitions from `solution.mpy`, calls the actual
  `digit_sum` binding on an arbitrary K integer `N`, and returns
  `signedDigitSum(N)`.
- Starts and ends with empty heap, empty stack, `NoExc`, exit code 0, and restored
  module environment. The exact module bindings on the RHS are constrained.

`SPEC.order-by-points`

- Loads the exact program and calls `order_by_points(list(VS))`.
- Requires `allInts(VS)`.
- Returns `ref(0)`, advances `heapLoc` from 0 to 1, and stores
  `list(expectedOrder(VS))` at heap location 0 while preserving the other
  observable cells.
- `expectedOrder(VS)` is definitionally
  `sortKeyVS(VS, closureVal("number", digitSumBody, 0))`.

## Rebuilt proof-extension inventory

The inventory was rebuilt from `verification.k`, `spec.k`, and the imported
sorting modules. There are no proof-local priority rules, simplification rules,
`[concrete]` rules, execution-interception rules, or operational bridges.

### Syntactic abbreviations

`digitSumLoopBody`, `digitSumBody`, `orderByPointsBody`, and `solutionModule`
are K macros. They are eliminated syntactically and do not replace execution.
Their expanded KORE was compared with the KORE parsed directly from
`solution.mpy`; `diff` was empty. Their state footprint and value influence are
therefore none independently of the exact program terms they abbreviate.

### Definitional summaries

| Extension | Domain and equations | Semantic role and value influence | Justification and dependents |
|---|---|---|---|
| `magnitude` | Disjoint guards `N >= 0` and `N < 0`, covering all integers | Pure value definition; does not replace a `<k>` computation | Integer absolute magnitude; used by `signedDigitSum` |
| `leadingDigit` | Base `0 <= N < 10`; recursive `N >= 10`; negative normalization `N < 0` | Pure decimal summary; affects the helper result and sort key | For nonnegative `N >= 10`, division by 10 strictly descends; used by the loop and `signedDigitSum` |
| `lowerDigitSumAcc` | Base `0 <= N < 10`; recursive `N >= 10`; negative normalization `N < 0` | Pure accumulator summary matching the program's update order | Recursive step removes the low digit and adds it to `S`; used by the loop |
| `lowerDigitSum` | Disjoint sign cases; initializes `lowerDigitSumAcc` with 0 | Pure abbreviation | Used by `signedDigitSum` |
| `signedDigitSum` | Disjoint `N >= 0` and `N < 0` cases | Determines the proven key result | Directly encodes the prompt example's signed-leading-digit convention; connected to execution by `SPEC.digit-sum-function` |
| `allInts` | Empty, integer-head, and guarded non-integer-head cases | Decides only the target precondition | Cases cover every `ValSeq` without overlap; used by `SPEC.order-by-points` |
| `expectedOrder` | One unconditional equation for every `ValSeq` | Names the entire observable output sequence | Definitional alias for the imported `sortKeyVS` call with the exact key closure; used by the target claim |

All guarded equation groups are pairwise disjoint. Their guards cover their
declared total domains. Recursive integer definitions descend after at most one
negative-to-nonnegative normalization. The sequence predicate structurally
descends. No equation is justified by alleged unreachability.

### Reachability extensions and matched contexts

| Extension | Class | Matched context and state footprint | Justification scope, containment, and dependents |
|---|---|---|---|
| `SPEC.digit-sum-loop` | Derived lemma / loop circularity | Exact `#while` term, condition, body, env 1, and exact local scope keys. Reads `number`, `sign`, and `total`; writes `number` and `total`; preserves `sign`, continuation, heap, stack, return state, exception, exit code, and framed scopes. | Proved using only fixed MPY execution and truthful summaries. Its arbitrary continuation and omitted cells are framed by the claim itself, so the match and justification domains coincide. Used by the whole-helper claim. |
| `SPEC.digit-sum-function` | Derived auxiliary execution theorem | Exact module load, exact binding, arbitrary integer argument, full helper body, call frame lifecycle, and listed initial/final cells. It returns an integer and restores control to the caller. | Machine-checked from fixed semantics plus the proved loop circularity. The altered-body witness fails, demonstrating body sensitivity. It justifies the program-defined key used at the external sorting boundary. |
| `SPEC.order-by-points` | Target reachability theorem | Exact module load and target call. Reads scopes and input; allocates heap location 0; advances `heapLoc`; returns `ref(0)`; preserves environment, stack, return state, exception, and exit code. | Executes the real target body under fixed MPY rules. Its result is conditional on the imported `sortKeyVS` contract. |

None of these claims is installed as a proof-local operational rewrite.
The loop circularity summarizes repeated fixed-semantics execution
coinductively; it has no return, exception, frame-pop, break, or continuation
discard in its body.

### Trusted result-bearing primitive

`sortKeyVS(ValSeq, Val)` is declared in the supplied read-only
`reference-semantics/semantics/sort.k` as an opaque total function. It is not
program-defined code and was not added by this proof.

- Class: trusted primitive.
- Complete symbolic match: the fixed rule for
  `#applyK(toCall(builtinV("sorted")), (list(VS), kwV("key", KV), .Vals))`.
- State footprint: consumes the evaluated builtin call, allocates one new list,
  returns its reference, and preserves the other modeled cells. Its value fixes
  the entire returned list and therefore affects the target postcondition.
- Named contract: stable ascending Python sorting of `VS` by calls to `KV`.
- Binding/control fidelity: the target proof establishes the exact builtin
  `sorted` binding and exact module `digit_sum` closure. The independent helper
  claim establishes the key closure's result for every integer.
- Dependents: `expectedOrder` and `SPEC.order-by-points`.
- Evidence: the supplied `MPY-CONCRETE` leg invokes the real key through the
  normal call machinery and uses stable insertion; four LLVM assertions,
  the prompt witness, tie cases, and the differential tests all passed.

No universal K theorem in these artifacts proves `sortKeyVS`'s ordering or
permutation contract. Every value-level HumanEval conclusion in this report is
explicitly conditional on that contract.

## Reproducible commands and actual results

The executable record is `prove.sh`. Its complete run exited 0.

```sh
python3 py2mpy.py solution.py > solution.mpy
python3 py2mpy.py concrete_tests.py > concrete_tests.mpy
python3 validate.py
```

Actual output:

```text
validated exact concrete-test body identity, 20001 digit keys, and 1781 stable sorts
```

The independent digit oracle in `validate.py` uses decimal strings rather than
the arithmetic proof equations. It checks every integer from -10000 through
10000. Stable-sort tests comprise all length-0-through-4 tuples over
`[-101, -20, -12, -11, -1]` (781 lists) plus 1000 deterministic random lists
of length 0 through 29 with values in `[-10^12, 10^12]`.

```sh
kompile reference-semantics/semantics.k \
  --backend llvm \
  --main-module MPY-KRUN \
  --syntax-module MPY-SYNTAX \
  --output-definition runtime-kompiled
krun concrete_tests.mpy --definition runtime-kompiled
```

Actual result: both commands exited 0. `krun` ended with `.K`, `NoExc`, and
modeled exit code 0. The four assertions include the prompt example, the empty
list, negative/positive ties, zero, and multi-digit stability. The compiler
printed only warnings from the supplied semantics; the exact output is in
`proof-logs/llvm-kompile.out` and `proof-logs/concrete-krun.out`.

```sh
kompile verification.k \
  --backend haskell \
  --main-module VERIFICATION \
  --syntax-module MPY-SYNTAX \
  --output-definition verification-kompiled
```

Actual result: exit 0, with only supplied-semantics unused-variable warnings.

```sh
kast solution.mpy \
  --definition verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module --expand-macros --output kore > solution.kore
kast --expression solutionModule \
  --definition verification-kompiled \
  --module VERIFICATION-SYNTAX \
  --sort Module --expand-macros --output kore > verification-solution.kore
diff -u solution.kore verification-solution.kore
```

Actual result: all exited 0; `diff` produced no output. Recorded marker:

```text
KORE program identity: identical
```

```sh
kprove spec.k \
  --definition verification-kompiled \
  --spec-module SPEC
```

Actual output and status:

```text
#Top
exit 0
```

This single positive command proves all three claims in `SPEC`.

Body-sensitivity probe:

```sh
kprove mutation-spec.k \
  --definition verification-kompiled \
  --spec-module MUTATION-SPEC \
  --claims MUTATION-SPEC.digit-sum-body-mutation
```

Actual result: exit 1 with `WarnStuckClaimState`. At witness 12, the mutated
body `return 0` leaves `0` rather than `signedDigitSum(12) = 3`.

False-postcondition probe:

```sh
kprove mutation-spec.k \
  --definition verification-kompiled \
  --spec-module MUTATION-SPEC \
  --claims MUTATION-SPEC.target-postcondition-mutation
```

Actual result: exit 1 with `WarnStuckClaimState`. At the realizable prompt input,
the residual requires the deliberately unchanged/wrong list
`[1, 11, -1, -11, -12]` to equal the opaque sorted result, and the implication
does not hold.

## Gate results

### Gate A — PASS

- A1: `solution.mpy` and expanded `solutionModule` have byte-identical KORE.
  The target body executes under fixed semantics. The helper has a universal
  exact execution claim, and replacing its body by `return 0` invalidates that
  connection at 12.
- A2: there are no proof-local operational bridges. The target claim constrains
  the returned reference, allocated list, heap location, environment, stack,
  return state, exception, and exit code.
- A3: module loading fixes the two program bindings; lookup reaches the supplied
  builtin namespace for `sorted`; the exact helper closure is passed as key.
  The loop claim's continuation frame is no broader than its own universal
  theorem.
- A4: the summary equations have complete, disjoint guards and descending
  recursion. No result-bearing program-derived oracle is present.
- A5: the prompt input is a satisfiable concrete witness. LLVM execution passes,
  while both the body mutation and false postcondition exit nonzero with stuck
  residuals.

### Gate B — PASS

- The source contract says a list of integers; the formal domain is every finite
  K list of K integers, including empty lists. Non-integer values and K `Bool`
  values are explicitly excluded.
- K integers are unbounded, matching Python's mathematical integer behavior for
  the modeled operations. The supplied list model preserves sequence order.
- The prompt example fixes the otherwise ambiguous negative convention, and the
  implementation/formal key agree with it.
- The summary-to-property bridge is clearly classified: helper meaning is
  formally proved; stable keyed sorting is conditional on the named supplied
  primitive contract and empirically supported.
- The implementation matches both prompt examples and the stated stable
  tie-breaking requirement under that contract.

### Gate C — PASS

- The trust ledger names the supplied `sortKeyVS` primitive, its full value and
  state influence, dependents, and evidence.
- Every claimed test and mutation has an existing artifact, exact command,
  saved output, input scope, oracle, and actual status.
- Formal facts, conditional conclusions, finite evidence, and excluded behavior
  are separated throughout this report.

## Trust boundary

The proof trusts the supplied reference semantics, the K toolchain/backend, and
the opaque `sortKeyVS` contract. The last item is the only task-relevant
unproved result-bearing primitive. It controls ordering and permutation of the
returned list; the target claim depends on it. The program-defined key is not
trusted: its exact execution is proved separately for every integer.

The concrete LLVM sort implementation and differential tests support, but do
not universally prove, the opaque sort contract.

## Empirically supported facts

- The prompt example and empty-list example pass under CPython and LLVM MPY.
- Four K assertions finish with `NoExc` and modeled exit code 0.
- An independent string-based oracle agrees with `digit_sum` on 20,001
  consecutive integer inputs.
- It agrees with `order_by_points` on 1,781 list inputs, including stable ties,
  boundaries, and deterministic large random integers.
- The proof representation is identical to `solution.mpy` after macro
  expansion.
- Both negative mutations are rejected.

These finite checks are evidence only and are not presented as universal
equivalence proofs.

## Excluded behavior

- Inputs that are not finite lists of K `Int` values, including strings,
  floats, nested lists, and K `Bool` values.
- Python subclass behavior, user-overridden comparison/key behavior, mutation
  during sorting, resource exhaustion, and implementation-specific CPython
  details outside the supplied MPY model.
- Exceptional behavior outside the stated input domain.
- A formal termination theorem.
- An internal K derivation of the ordering/permutation/stability properties of
  `sortKeyVS`; those properties remain conditional on its named supplied
  contract.
