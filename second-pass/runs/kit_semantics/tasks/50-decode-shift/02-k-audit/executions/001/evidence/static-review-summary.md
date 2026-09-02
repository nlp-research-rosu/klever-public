# Static rule review summary

The exhaustive machine inventory is `rule-inventory.tsv`: 941 source
statements (231 syntax declarations, one configuration, five contexts, 701
rules, and three claims). Its row count exactly matches an independent
source-start scan. The assessments below cover every row by source module.

| Source | Review of all declarations/rules | Material to this theorem |
|---|---|---|
| `semantics.k` | Assembly imports only; `MPY` excludes concrete-only rules and `MPY-KRUN` adds them for LLVM. | The Haskell proof imports `MPY`; the concrete audit imports `MPY-KRUN`. |
| `syntax.k` | Constructor AST plus strict/seqstrict evaluation attributes. No semantic result equations. | `Module`, `FuncDef`, `Params`, `Expr`, `Str`, `Assign`, `Name`, `For`, `BinOp`, `Call`, `Int`, `Return`, and list units. `BinOp` is left-to-right; assignment/iteration/return evaluate their operands. |
| `core.k` | Algebraic values, nine-cell configuration, allocation/cells, sequencing, lexical lookup, builtins scope, left-to-right argument evaluation, literals, truthiness, dispatch declarations, and structural sequence helpers. Priorities only disambiguate heap/cell paths. | Plain (non-cell, non-heap) scope lookup, the exact builtins binding, statement sequencing, argument order, integer literals, and `appendVal`. No allocation or opaque value lies on the proof path. |
| `iter.k` | Declares the uniform iterator protocol. | Used by the string `for` loop. |
| `range.k` | Positive/negative range bounds, lengths, and iterator steps. Step zero is outside its defined subset. | Unused. |
| `operators.k` | Dispatch after strict evaluation; heap dereference priorities and identity cases. | Only ordinary `BinOp` dispatch on integer and string values is reachable. |
| `int.k` | Integer unary/arithmetic/comparison equations; `pyMod` implements floored modulo. | `+`, `-`, `%`, and `pyMod(_,26)` are used. The divisor is always positive and nonzero. |
| `bool.k` | Boolean comparison, value-returning short-circuit `and`/`or`, and heap receiver variants. | Unused by the submitted body. |
| `float.k` | Concrete IEEE hooks plus 19 proof-opaque `no-evaluators` symbols and guarded math-call interception. | Entirely unused. No Float term can arise from the submitted body. |
| `str.k` | Finite code-list iteration, ASCII literal conversion, concatenation, equality/membership, and lexicographic order. | String iteration, ASCII literals, and concatenation are used. Every source literal is ASCII and every input code is constrained to 97–122. |
| `set.k` | Finite code-set folds and equality. | Unused. |
| `list.k` | List construction/allocation, structural operations, iterator, membership, and mutation. | Unused by the submitted body and proof. |
| `tuple.k` | Tuple construction/iteration/equality, unpacking, and target binding. | Only `#bindTgt(Name,V)` is reached by `for`; it performs the plain local write. Cell/tuple cases are excluded by the exact state. |
| `subscript.k` | Indexing/slicing and normalization. `valSeqAt` is deliberately total/opaque outside constructor in-bounds cases. | Unused. |
| `comprehension.k` | Pure macros expanding comprehensions into closures and loops. | Unused; the candidate deliberately uses a direct `for`. |
| `methods.k` | String/list methods and structurally recursive helper equations. | Unused. |
| `controls.k` | Assignment, imports, expression statements, branches, direct loops, control transfer, and heap receiver priorities. | Plain assignment, docstring expression discard, and the direct `for`/`#loop` rules are used. There is no break, continue, mutation, or abrupt bridge. |
| `functions.k` | Function closure creation, annotated cells, parameter binding, return, and frame pop. | Plain closure, one parameter, return, frame deletion, and restoration are used. Annotated closures/cells are excluded by the pinned plain scopes. |
| `builtins.k` | Registry operations and finite folds; ordinary `ord`/ASCII `chr`; one opaque MD5 symbol. | Only `applyBuiltin`, one-character `ord`, and guarded `chr` are used. The decoder arithmetic proves `chr` receives 97–122. |
| `call.k` | Callee-before-arguments evaluation and dispatch to closures, builtins, types, and methods; heap priorities. | Exact closure lookup/call and `ord`/`chr` builtin calls are used. The pinned scope chain rules out shadow bindings. |
| `sort.k` | Opaque symbolic sorting with concrete LLVM insertion-sort equations. | Unused; both opaque sort symbols are outside the theorem. |
| `assert.k` | Truthy/falsy concrete smoke-test assertions. | Used only by the reviewer’s LLVM harness, not by the proof claims. |
| `dict.k` | Ordered finite dictionary constructors/helpers, access, update, and equality. | Unused. |
| `concrete.k` | LLVM-only deep list equality and keyed sorting. | Absent from the Haskell proof definition and unused by the reviewer’s concrete function. |
| `verification.k` | Four total proof-local functions: one unconditional equation each for `decodeCode` and `encodeCode`; disjoint empty/constructor equations for `decodeAcc` and `lowerCodes`. Both recursions strictly shorten the first sequence. | All are mathematical definitions. There are no priorities, simplifications, concrete rules, opaque symbols, operational bridges, or overlap gaps. |
| `spec.k` | One arithmetic inverse claim, one fixed-semantics loop circularity, and one entry reachability claim. | All three reconstruct with `#Top`; entry uses the loop claim as its circularity dependency. |

## Overlap, totality, and trust decision

All proof-local equations are exhaustive over their declared algebraic domains,
pairwise disjoint (or have one unconditional equation), and terminating.
`decodeCode`, `encodeCode`, `decodeAcc`, and `lowerCodes` do not rewrite any
operational configuration and cannot bypass program execution.

The material fixed-semantics rules have disjoint sorts/guards on the pinned
state. Priority rules for cells, heap references, special calls, collection
allocation, and control constructs do not match the plain string/integer
execution path. No material rule is `concrete`, `no-evaluators`, or
`simplification`.

The supplied definition intentionally has a wider trust surface for unused
features: 22 `no-evaluators` declarations (float arithmetic/comparison,
sorting, and MD5), concrete-only equations, partial valid-program functions,
and compiler warnings for total declarations not exhaustively reduced by
equations. These are not reachable from this program and no symbol derived
from them occurs in a claim or postcondition. They therefore cannot enable a
false result on the intended lowercase-input domain. No unsound-rule finding
is made without such a witness.
