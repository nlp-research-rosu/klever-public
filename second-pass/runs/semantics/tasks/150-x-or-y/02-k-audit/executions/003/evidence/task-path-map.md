# Material constructor and rule map

This map is derived from the byte-identical trusted translation
`solution.mpy`. `rule-inventory.tsv` inventories every declaration and rule,
including imported constructs that are not reachable from this program.

| Submitted constructor / effect | Declaration and rules that execute it | Audit decision |
|---|---|---|
| `Module(FuncDef(...))` in concrete reconstruction | `semantics/syntax.k:61`; `semantics/core.k:42`; `semantics/functions.k:14` | Faithfully loads the sole function binding in module scope. The target claim uses an equivalent direct closure invocation, mechanically checked in `constructor_compare.py`. |
| Statement sequence | `semantics/syntax.k:56`; `semantics/core.k:43-44` | Left-to-right sequencing; `.Stmts` terminates. |
| `#xOrY(N,X,Y)` entry | `verification.k:26-29` | Macro-expands to `Call(closureVal(("n","x","y"), translated-body,0),(N,X,Y))`; exact body and parameter equality is machine-compared. |
| Closure call and frame allocation | `semantics/core.k:143-149`; `semantics/call.k:16-20,61-66`; `semantics/functions.k:63-65,78-89` | Callee and arguments evaluate left-to-right; parameters bind in order; a fresh local frame is pushed; return restores the caller and deletes the frame. |
| `if n < 2` | `semantics/syntax.k:21,46`; `semantics/operators.k:12-19`; `semantics/int.k:22`; `semantics/core.k:165-169`; `semantics/controls.k:49-52` | Integer comparison is exact; `If` selects the matching branch. |
| `return y` / `return x` | `semantics/syntax.k:48`; `semantics/functions.k:78-89` | Sets `retV` and discards the remaining callee continuation exactly as Python return requires. |
| `range(2,n)` lookup and call | `semantics/core.k:47-82,94-119,143-149`; `semantics/call.k:16-30`; `semantics/builtins.k:177-180` | Plain local scope does not contain `range`, so lookup reaches the fixed builtins scope; two arguments are evaluated left-to-right; the result is `rangeObj(2,n,1)`. |
| `for divisor in range(...)` | `semantics/syntax.k:44`; `semantics/controls.k:61-69`; `semantics/range.k:7-24`; `semantics/tuple.k:31-40` | Iteration yields `D`, advances to `D+1`, binds `divisor` in the active local scope, executes the body, then returns to the exact loop continuation. |
| `n % divisor` | `semantics/syntax.k:15`; `semantics/operators.k:10`; `semantics/int.k:15,19-20` | `divisor` is always at least 2 on the loop path. `pyMod(n,d)=((n %Int d)+d)%Int d` is Python’s floor-modulus result for positive `d`. |
| `... == 0` | `semantics/syntax.k:31`; `semantics/operators.k:14-19`; `semantics/int.k:26` | The right operand evaluates after the left; integer equality is exact. |
| Loop mathematical result | `verification.k:33-49` | `primeSelect` returns `y` for `n<2` or the first divisor and `x` exactly after exhausting all `2..n-1`; guards partition every use and recursion strictly increments `D` until `D>=N`. |
| Final loop-local `divisor` | `verification.k:52-64` | `scanLast` mirrors the last successful target binding; guards partition every use and recursion terminates. It affects only the exact scope footprint of the loop summary, not the returned choice. |
| Proven loop bridge | `spec.k:9-36` and `verification.k:73-100` | The base definition proves the exact claim first. The imported priority-40 rule has the same complete continuation, stack, bindings, heap, exception, exit, scope-location, result, guard, and state updates—no wildcard continuation or omitted cell. |

No used operation allocates heap data, performs I/O, raises an exception, uses
floating point, sorting, hashing, collections, comprehensions, imports,
subscripts, or an opaque supplied symbol. The heap therefore remains `.Map`;
the only material mutable state is the local scope and call stack.
