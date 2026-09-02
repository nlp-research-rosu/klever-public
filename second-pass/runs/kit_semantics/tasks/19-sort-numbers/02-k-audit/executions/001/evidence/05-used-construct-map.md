# Used-construct and proof-extension audit

The exhaustive machine-readable inventory is `05-rule-inventory.json` (950
entries: 232 syntax declarations, one configuration, five contexts, 701 rules,
and 11 claims). This note records the program-relevant mapping and the
individual decisions for every candidate-local extension.

## Submitted constructor mapping

| Submitted construct | Fixed declaration/behavior | Evaluation, control, and state audit |
|---|---|---|
| `Module` / two `FuncDef` nodes | `syntax.k`; `core.k` `#loadAll`; `functions.k` function-definition rule | The entry claim starts after load with exactly the two resulting module bindings. Mechanical constructor comparison is in `04-pinning-results.json`. |
| `Call` / `Name` | `syntax.k`; `core.k` `#look` and left-to-right `#evalArgs`; `call.k` generic call route and closure dispatch | Lookup is pinned to module scope 0, whose parent is the fixed builtins scope. Calls allocate a temporary scope, push a continuation frame, bind the sole parameter, and later restore/deallocate it. |
| `Return` | `syntax.k`; `functions.k` `Return(V) ~> _ => #pop` and `#pop` | Correct abrupt return: the function suffix is discarded, the saved continuation/environment/scope location are restored, and the return value is propagated. |
| `Str` | `syntax.k`; `str.k` `Str` and `strToCodes` | All program literals are ASCII and reduce exactly to `IntSeq` code strings. |
| `TupleExpr` | `syntax.k`; `tuple.k` `toTuple` through `#evalArgs` | Ten literals evaluate left-to-right into an unboxed tuple value; no heap allocation is omitted. |
| `Attribute` | `syntax.k`; `call.k` bound-method rule | Receiver evaluation precedes arguments. No candidate priority bridge changes binding. |
| tuple `.index` | `tuple.k` `applyMethod(...,"index",...)` and `idxOfVS` | For each allowed ground string, recursion stops at the first structural-equality match. Ten independently proved helper claims cover the complete valid callback domain. |
| string `.split()` | `methods.k` priority-40 no-argument dispatch, `splitWS`, `flushTok`, `isWSC`; `core.k` `#alloc` | Exactly one fresh list is allocated at heap location 0. Runs of ASCII space/tab/LF/CR are discarded. Prompt-required ASCII-space inputs are fully covered. |
| `KwArg("key", Name("_number_key"))` | `core.k` `#kwTag` and `isKwV` | The callback name is looked up after the split argument and is preserved as a tagged argument. |
| builtin `sorted(..., key=...)` | `core.k` `builtinsScope`; `sort.k` keyed dispatch and opaque `sortKeyVS` | Proof execution allocates heap location 1 containing `sortKeyVS(VS, callback)`. The proof backend does not invoke the callback or define the returned permutation. This is the sole material trust boundary. `concrete.k` has a separate priority-40 callback-executing stable insertion algorithm for LLVM only. |
| string `.join(...)` | `call.k` receiver/argument dereference; `methods.k` `joinCodes` | The sorted-list heap object is read, separators are inserted between string values, and the result stays an unboxed string. In the proof backend, `joinCodes` remains wrapped around opaque `sortKeyVS`. |

No submitted construct uses a loop, comprehension, mutation, exception handler,
float, dictionary, set, slice, import, or other semantics subsystem.

## Candidate-local extension decisions

| Extension | Attributes/class | Complete decision |
|---|---|---|
| `numberKeyClosure` syntax and macro rule | `macro`; compile-time definitional alias | Acceptable. It has no cells, guards, priority, continuation, or runtime rewrite footprint. `04-pinning-results.json` mechanically matches its parameters/body/environment to the regenerated `_number_key` constructor. The fresh body mutation executes a swapped tuple and leaves residual result `1` where `0` is required. |
| `sortNumbersClosure` syntax and macro rule | `macro`; compile-time definitional alias | Acceptable. It is constructor-identical to regenerated `sort_numbers`, including the single-space separator, no-argument split, keyword callback binding, and environment 0. The fresh main-body mutation that returns its input is rejected with the concrete unsorted string in the residual. |
| `isNumberWord` declaration and equation | `[function,total]`; definitional predicate | Acceptable. One unconditional equation covers every `Val`; its ten structural string equalities are exactly the prompt vocabulary. It affects only the entry precondition. |
| `allNumberWords` declaration and two equations | `[function,total]`; structural predicate | Acceptable. Empty and `vCons` guards are constructor-disjoint and exhaustive; recursion strictly descends. It affects only the entry precondition. |
| `expectedSortNumbers` declaration and equation | `[function,total]`; execution summary | Formally truthful but trust-dependent. One unconditional nonrecursive equation names the exact proof-backend result. It has no operational match or state footprint. Its value depends on supplied opaque `sortKeyVS`, so it does not independently prove numeric ordering. |

There are no candidate-local opaque symbols, ordinary operational bridges,
priority rules, simplification rules, `concrete` rules, auxiliary semantic
rules, or loop circularities. The only candidate-local ordinary equations are
the predicates and result-summary equation above; their guards do not overlap
inconsistently, and their declared domains are covered.

## Fixed-semantics rule decision

All 928 fixed-semantics inventory entries are byte-identical to the trusted
supplied tree. Each syntax-only row is a declaration and has no truth
conclusion. Each rule row was reviewed by module in the inventory:

- the 499 ordinary relevant entries plus five `sortKeyVS` declaration/dispatch
  entries implement the flow mapped above; no false rule conclusion or
  state/control mismatch was found on the intended input domain;
- the 20 `MPY-CONCRETE` entries are absent from the Haskell proof module and
  support only finite LLVM validation;
- the 404 assembly or unused-general entries do not match any submitted
  construct. They add no candidate-specific proof shortcut, and this audit
  makes no unsupported claim that the intentionally partial MPY language is a
  complete Python semantics.

The relevant compiler warning that `joinCodes` is not exhaustive for arbitrary
`ValSeq` values does not fabricate a concrete result: applied to the opaque
`sortKeyVS` output it remains an abstract term. The other non-exhaustiveness
warnings concern unused float/map/index cases. No rule was labeled unsound, so
there is no unsupported unsoundness allegation requiring a false-conclusion
witness.
