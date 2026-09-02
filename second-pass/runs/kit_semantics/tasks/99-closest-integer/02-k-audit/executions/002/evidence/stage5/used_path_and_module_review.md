# Static review notes

The machine-derived inventory in `rule-inventory.log` enumerates 244 local
`syntax` declarations, one configuration, five contexts, 764 rules, and four
claims from every supplied `.k` file plus `verification.k` and `spec.k`.
There are no `[simplification]` rules. `verification.k` adds no declaration.

## Exact submitted-program path

| Submitted construct or internal step | Fixed declaration/rule path | Finding |
|---|---|---|
| `Module`, `Import`, `FuncDef`, `Params` | `syntax.k:53,57,61`; `core.k:125`; `float.k:61`; `functions.k:14-16` | Module loading creates the exact closure. The supplied model deliberately makes imports a no-op. |
| Entry `Call(Name("closest_integer"), str(CS))` | `call.k:20-21,69-74`; `core.k:131-154,157-181,189-191`; `functions.k:63-66` | Callee then argument evaluation, exact closure selection, fresh frame, positional bind, and caller continuation preservation are correct for this one-argument call. |
| Statement sequence and assignments | `core.k:126-127`; `syntax.k:41`; `controls.k:9-18` | Left-to-right body sequencing and RHS-before-write assignment are preserved. Candidate frames contain no closure cells, so the ordinary write leg is selected. |
| `float(value)` | `call.k:20-32`; `float.k:196-223` | Produces the supplied opaque `decStrToF(CS)` proof value; its concrete parser is a supplied-model boundary. |
| `math.floor(number)`, `math.ceil(number)` | `float.k:61,65-75,90-95` | Fixed priority bridges evaluate the sole argument and return `floorFI`/`ceilF`. They skip ordinary `math` lookup, but the submitted module imports `math`, never rebinds it, and uses exactly these calls. |
| `number > 0` | `syntax.k:15,30,32`; `operators.k:15-17`; `core.k:194`; `float.k:158-181` | Cools to `ltIF(0, decStrToF(CS))`, exactly the claims' first guard. |
| `number - lower < 0.5` | `operators.k:12,15-17`; `float.k:103-105,125-139,231-239`; `float.k:21,50-52` | Cools to `floatLt(subF(F,intToF(floorFI(F))),0.5)`, exactly the positive guards. Duplicate mixed-arithmetic rules have identical right-hand sides. |
| `upper - number < 0.5` | Same operator rules | Cools to `floatLt(subF(intToF(ceilF(F)),F),0.5)`, exactly the nonpositive guards. |
| Nested `If` and `Return` | `syntax.k:49-50`; `controls.k:51-54`; `functions.k:77-90` | Boolean branch selection, abrupt return, frame pop, environment restoration, callee-scope deallocation, and result resumption match the real control flow. |
| Final cells | `core.k:49-60`; call/pop rules above | The claim constrains scopes, allocators, heap, stack, return state, exception, and exit code, not only the value. |

No helper claim, circularity, proof-local function, rule, priority, equation,
oracle, or operational bridge is present. The four claims merely select the
four concrete paths induced by two fixed opaque Boolean primitives.

## Module-by-module disposition

| Module | Inventory disposition |
|---|---|
| `MPY-SYNTAX` | Grammar and strictness declarations are coherent. Every constructor used by `solution.mpy` is declared; `BinOp` is left-to-right, assignments evaluate RHS, and `If`/`Return` evaluate their expressions. |
| `MPY-CORE` | Configuration, lookup, sequencing, literal, list-helper, allocation, and closure-cell rules are internally coherent. Candidate execution uses the plain (non-cell) lookup/write paths. |
| `MPY-CALL`, `MPY-FUNCTIONS` | Frame and call rules preserve binding, continuation, return, and all modeled cells for the candidate's top-level one-argument call. Unsupported arity/nested-closure cases become stuck rather than fabricating this result. |
| `MPY-CONTROLS` | Assignment and branch rules used here are faithful. Imports are intentionally collapsed; this is a fixed-model state/representation gap, not a candidate rule. |
| `MPY-OPERATORS`, `MPY-INT`, `MPY-BOOL` | Dispatch and the integer/Boolean equations are ordinary arithmetic/control equations. Priority dereferences are unused by this heap-free program. |
| `MPY-FLOAT` | The concrete equations use K's IEEE float hooks; the proof-side symbols are externally supplied opaque primitives. The duplicated mixed `+`, `-`, `*` equations agree on overlaps. The used parser, floor, ceil, integer conversion, subtraction, and comparison primitives are result-bearing trust boundaries, not derived theorems. |
| `MPY-STR` | Code-sequence operations are truthful for the supplied ASCII code model. The ASCII-only literal restriction is a supplied representation gap and does not narrow symbolic `str(CS)` input. |
| `MPY-LIST`, `MPY-TUPLE`, `MPY-SET`, `MPY-DICT` | Structural sequence/set/dict equations are coherent for their encoded domains and unreachable from this candidate. Proof-mode list/tuple/dict equality uses structural K equality, so Python's cross-numeric equality is not generally modeled (witness: `[True] == [1]` in CPython); no such term is reachable here. |
| `MPY-SUBSCRIPT` | Index/slice equations are unreachable. Its declared-total opaque/OOB stance is explicitly a model abstraction; it cannot influence these claims. |
| `MPY-METHODS` | ASCII string method folds are unreachable. The subset is not full CPython (for example, CPython `"abc".count("") == 4` while the supplied empty-pattern fold returns 0); no candidate term can expose it. |
| `MPY-RANGE`, `MPY-ITER` | Nonzero-step length and iterator equations are ordinary and unreachable here. |
| `MPY-COMPREHENSION` | Macro expansion is unreachable. `GenExp` is modeled eagerly like the supported comprehension subset, not as a general CPython generator. |
| `MPY-BUILTINS` | Registry/call equations used for `float` are routed into `MPY-FLOAT`. Other folds, the restricted arithmetic `eval`, and opaque `md5` are unreachable and cannot affect this proof. |
| `MPY-SORT` | Opaque proof-side sorting lacks an in-K universal connection theorem, but no sort term occurs in this program, precondition, or result. |
| `MPY-ASSERT`, `MPY-CONCRETE` | Assert and concrete-only deep-equality/sort/membership rules are absent from the Haskell proof module. They are used only for independent LLVM probes. |
| `VERIFICATION` | Imports `MPY` and adds nothing. |
| `SPEC` | Four reachability claims, no rules or simplifications. Their guards are complementary and their result terms are exact executed locals, with no RHS-only variable. |

The concrete CPython-inexact examples above are limitations of unused portions
of the supplied fixed subset. They do not overlap any term reachable from the
submitted function and therefore cannot enable a false conclusion about its
return value or state.

## Result-bearing supplied primitives

The proof depends on `decStrToF`, `floorFI`, `ceilF`, `intToF`, `subF`,
`ltIF`, and `floatLt`. In the Haskell definition they are opaque/abstract
fixed primitives; in the LLVM definition they reduce through concrete float
hooks. The proof is interpretation-parametric in these symbols and establishes
the exact program result structure under any interpretation. Its
human-facing nearest-integer conclusion is conditional on their normal finite
binary-float contracts.

The supplied parser cannot model every spelling CPython `float` accepts.
Fresh evidence records that the fixed model makes the submitted algorithm
return 632 for `"1e2"`, while the unchanged submitted Python returns 100 under
CPython. The candidate explicitly records exponent, plus-sign, whitespace,
and related spellings as a fixed-model boundary. The candidate program itself
is faithful on the concrete witness.
