# Static K review notes

## Inventory scope

`stage5-k-rule-inventory.log` mechanically reads every K source file used by
the clean proof: the supplied `reference-semantics/semantics.k`, all 23 helper
files below `reference-semantics/semantics/`, `verification.k`, and `spec.k`.
It records 28 modules, one configuration, 233 syntax records, 710 rule
records, five context records, and three claims. The full statement of every
record, including guards and attributes, is preserved there.

All 24 supplied-semantics files are byte-identical to the trusted
`/reference/reference-semantics` tree. They are therefore classified as the
fixed, launcher-selected semantics trust boundary. No candidate rule has been
inserted into that tree. The proof-specific extension surface is exactly
`verification.k`; it is reviewed rule by rule below.

## Constructs executed by `solution.mpy`

| Submitted constructor | Declaration/evaluation route | Static assessment |
|---|---|---|
| `Module`, `Stmts` | `syntax.k:56,61`; `core.k:124-127` | Loads and sequences the submitted module statements in order. |
| `ImportFrom("typing","List")` | `syntax.k:43`; `controls.k:35-44` | The non-`math` import is an `owise` no-op. This import is typing-only and has no runtime binding used by the body. |
| `FuncDef`, `Params` | `syntax.k:53,57`; `functions.k:14-16` | Binds the exact body as a closure in module scope 0. |
| `Call`, arguments, user closure | `syntax.k:28`; `call.k:20-21,69-74`; `core.k:183-191`; `functions.k:63-66,78-90` | Evaluates callee then arguments left-to-right, allocates a callee scope, binds `numbers`, executes the body, returns, pops the frame, and restores all caller control cells. |
| `Name` | `syntax.k:12`; `core.k:129-181` | Resolves locals, then module scope, then the pinned builtins scope. This pins `len` and `abs` to supplied builtins, not arbitrary bindings. |
| `Assign` | `syntax.k:41 [strict(2)]`; `controls.k:9-18` | Evaluates the RHS first and updates the active callee scope. The cell-variable priority case is inapplicable to this plain closure. |
| `len(numbers)` | `builtins.k:17,20-26`; `core.k:223-225`; call routing above | A bare read-only `list(VS)` yields `vsLen(VS)`. |
| `If`, `Compare(count == 0)`, `Int(0)` | `syntax.k:30,32,49`; `operators.k:15-17`; `int.k:26`; `controls.k:50-54`; `core.k:194,199-205` | Evaluates left then right, obtains exact integer equality, and selects exactly one branch. |
| `Float(0.0)` | `syntax.k:10`; `float.k:20-21` | Evaluates to K `Float` 0.0. |
| `For` over `list(VS)` | `syntax.k:45`; `controls.k:62-74`; `list.k:8-10`; target binding in `tuple.k` | Evaluates the iterable once, yields the list head in order, binds `number`, executes the body, and recurs on the tail. Empty and cons cases are disjoint. |
| `BinOp("+",...)` | `syntax.k:15 [seqstrict(2,3)]`; `operators.k:12`; `float.k:111-113`; guarded local dispatch twin | Preserves left-to-right evaluation and computes the supplied opaque `addF` value. |
| `BinOp("-",...)` | same route; `float.k:103-105`; guarded local dispatch twin | Computes supplied opaque `subF` on two floats. |
| `abs(...)` | call/name routes; `float.k:54-56` | Selects the pinned builtin and yields supplied opaque `absF`. |
| `BinOp("/", Float, Int)` | operator route; `float.k:189-192` | Yields supplied opaque `divFloatIntV`. Nonempty list length is positive; empty execution returns before division. |
| `Return` | `syntax.k:50 [strict]`; `functions.k:78-90` | Evaluates the result, discards the remaining body, records it, restores the caller frame, and exposes the value in `<k>`. |

The active program has no mutation of the input list, output, exception,
closure escape, method call, comprehension, subscript, dictionary, set,
string, sort, or concurrency behavior. Rules for those unused constructs are
part of the fixed trusted semantics but do not contribute to this proof.

## Proof-local declaration and rule decisions

| `verification.k` lines | Extension | Decision |
|---|---|---|
| 8, 47-49 | `allFloatVS` total predicate | Sound definitional summary. Empty/cons equations are disjoint and exhaustive over `ValSeq`; recursion strictly descends. It restricts the theorem to K `Float` elements. |
| 9-10 | total opaque `projectFloat(Val)` declaration | Outside `isFloat` it is deliberately underspecified despite `[total]`; that opaque outside-domain value is not used by any target path. Inside the theorem guard it is fixed by the cast/collapse rules below. This is a real local trust/evidence boundary omitted by the candidate's claim that there are no local opaque symbols. |
| 54-56 | definedness of the `Val`-to-`Float` projection | Sound sort characterization: the outer cast is defined exactly when `isFloat(V)` and `V` itself is defined. It affects no configuration cell. |
| 57-63 | concrete/symbolic projection orientations and `projectFloat(F) => F` | Sound on their guards. Concrete and symbolic orientations are mode-separated; the ground collapse fixes every actual `Float` to itself. The positive 1.0 witness closes and the opposite 2.0 witness is rejected in `stage5-projection-witnesses.log`. No false ground interpretation was found. |
| 67-70 | guarded dynamic float addition dispatch | Sound derived equation on `isFloat(V)`: it overlaps supplied `applyBin("+", Float, Float)` only where `projectFloat(V)` collapses to the same `V`, so both RHS terms agree. No state/control cells are changed. |
| 71-74 | guarded dynamic float subtraction dispatch | Same assessment against supplied `applyBin("-", Float, Float)`. |
| 77-79 | `sumFloatVS` | Sound left-fold definition; constructor cases are exhaustive/disjoint and recursion descends on the tail. It does not rewrite an operational program term. |
| 81-86 | `deviationFloatVS` | Sound left-fold definition matching the exact subtraction, absolute-value, and addition order of the body. Exhaustive/disjoint and descending. |
| 88-99 | `madResult` | Sound result summary for the generated program. Zero/nonzero guards are disjoint; `vsLen` is a nonnegative integer and the guards cover it. The nonzero equation exactly composes the two folds and the two divisions. |
| 16, 26-44 | `madBody` syntax macro | Sound and semantically inert. Fresh `kast --expand-macros` parses of the submitted module and the claim module are byte-identical KORE in `stage4-constructor-pinning.log`. |

The two guarded `applyBin` rules are proof-time dispatch lemmas. A
bridge-free Haskell attempt using only fixed semantics reached the expected
sort-projection implication but did not close
(`stage5-bridge-free-connections-v2.log`); this is a machine-evidence gap, not
a false-rule witness. The rule equations nevertheless follow by exhaustive
subsort reasoning, their supplied-rule overlaps agree after the identity
collapse, and the opposite projection interpretation is rejected. They do not
skip binding, iteration, calls, returns, exceptions, or any configuration
state.

## Claim decisions

- `sum-loop` starts at the actual supplied-semantics `#loop` form for the first
  source loop. Its arbitrary suffix is retained; every configuration cell is
  fixed or framed. The accumulator becomes the exact left fold over the
  remaining suffix. `number` is existentially left at its actual final value,
  which is safe because it is overwritten before the next read in the entry
  execution.
- `deviation-loop` has the same control footprint for the second source loop,
  additionally preserving the exact `mean`. Its accumulator becomes the exact
  deviation fold. The final `number` value is unobserved before frame
  deallocation.
- `mean-absolute-deviation` begins with the entire submitted module constructor,
  performs the actual function lookup/call/body, and constrains the returned
  `<k>` value to `madResult(VS)`. Initial scope, heap, allocation counters,
  stack, return state, exception state, and exit code are realizable and
  pinned.

`[1.0, 2.0, 3.0, 4.0]` satisfies the entry precondition. Ground
interpretations of `madResult` agree exactly with both trusted canonical
Python and generated Python on four nonempty witnesses in
`stage4-postcondition-substitutions.log`.

## Static conclusion

No proof-local rule admits a concrete or symbolic false conclusion on the
formal all-float domain, so no rule is labelled unsound. The two limitations
to carry into the verdict are:

1. the guarded dynamic dispatch connection is justified by sort reasoning and
   witnesses, but the attempted bridge-free universal K claim did not close;
2. the formal precondition excludes K `Int` elements even though both Python
   implementations accept integer and mixed numeric lists at runtime, and the
   generated program gives `[]` a value where the trusted canonical raises.
