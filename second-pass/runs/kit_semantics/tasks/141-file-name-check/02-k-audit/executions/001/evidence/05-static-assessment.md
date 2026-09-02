# Static rule assessment

This assessment covers every entry in `05-rule-inventory.tsv`: 937 declarations
from the 24 supplied K source files plus `verification.k` (700 rules, 231 syntax
declarations, five contexts, and one configuration). The supplied tree was
already established byte-identical to `/reference/reference-semantics`.

## Per-module decision

| Module/file | Role in this theorem | Static decision |
|---|---|---|
| `semantics.k` | Imports the fixed `MPY` modules; `MPY-KRUN` additionally imports the concrete legs | Import graph is consistent. The proof build imports `MPY`, not `MPY-CONCRETE`. |
| `syntax.k` | Declares every constructor in `solution.mpy` | Accepted. Strictness/context declarations give left-to-right expression evaluation where material. |
| `core.k` | Values, configuration, statement sequencing, lookup, literals, truthiness, argument evaluation | Accepted on the execution slice. The entry configuration supplies the exact function binding and builtin parent scope; argument evaluation is left-to-right; no allocation is performed by this program. |
| `iter.k`, `range.k`, `set.k`, `list.k`, `tuple.k`, `comprehension.k` | Fixed semantics outside this program's execution slice | No rule can match the submitted body. No candidate theorem depends on their iterator, collection, allocation, or comprehension behavior. |
| `operators.k` | Dispatches unary, binary, and comparison nodes | Accepted. The program reaches ordinary dispatch on non-reference string/int/bool values; heap-reference priority rules are inapplicable. |
| `int.k` | Unary minus, integer addition, `>` and `!=` | Accepted. Rules are direct K integer operations and sort-disjoint from float/string rules. |
| `bool.k` | `not` and three-way `or` short-circuit | Accepted. Only the next operand is heated; truthy branches are complementary and preserve Python's value-returning short circuit. Here every operand is Boolean. |
| `float.k` | Fixed float/trusted primitives | Outside the execution slice. All `no-evaluators` float symbols, concrete twins, and math-call priority rules are unused and cannot affect a claim result. |
| `str.k` | ASCII literals, equality, membership, substring helpers | Accepted on the execution slice. All program literals are ASCII. `strContains(singleton, alphabet)` exactly implements first-code membership; equality is sequence equality. |
| `subscript.k` | Index zero and `[-4:]` slicing | Accepted. The index is reached only after the dot-count test proves a nonempty input. The `[-4:]` route uses step 1, the standard negative-index adjustment and clamps, then builds an in-bounds suffix. Opaque/out-of-bounds `valSeqAt` behavior is not reached. |
| `methods.k` | `str.count` | Accepted. Every searched pattern is a nonempty singleton (`"."` or one ASCII digit); `cntSub` has base/consume/advance cases with complementary guards and strict recursive descent. |
| `controls.k` | `If` | Accepted. Strict condition evaluation feeds `truthy` to complementary `#branch` rules. Assignment/loop/import rules are unreachable. |
| `functions.k` | Parameter binding, return, and frame pop | Accepted. The single parameter is bound in a fresh scope; `Return` records the exact value and pops/restores every cell present in the claims. |
| `builtins.k` | Fixed builtin operations | No builtin call is made by this body. Its declarations are imported through the call layer but no `applyBuiltin` rule is reachable. The opaque MD5 symbol is unused. |
| `call.k` | Callee lookup, arguments, bound method dispatch, user-call frame | Accepted. The entry name selects the explicitly pinned closure; each `count` attribute becomes a bound method; arguments are evaluated before dispatch. No higher-priority math/MD5/sort interception matches. |
| `sort.k` | Opaque sort primitives and concrete sort equations | Outside the execution slice. `sortVS` and `sortKeyVS` do not occur in the body, claims, or constraints. |
| `assert.k` | Concrete smoke-test assertions | Outside the proof execution slice; used only by the independent LLVM test program. Its true/false guards are complementary. |
| `dict.k` | Fixed dictionary subset | Outside the execution slice. |
| `concrete.k` | LLVM-only deep equality/keyed sort | Not imported into the Haskell proof definition and outside the program. |
| `verification.k` | Exact body macro, three precondition summaries, one simplification | Each item is assessed individually below. |

For every fixed-semantics entry marked outside the execution slice, the entry's
left-hand constructor/symbol is absent from both the submitted body and all
reachable values/continuations. It therefore cannot contribute to closure.
Opaque fixed primitives are a declared semantics-level trust boundary, not
program-derived abstractions in this theorem.

## Material constructor-to-rule map

| Submitted construct | Declaration and material rules |
|---|---|
| `Module`, statement sequence | `syntax.k:61`; `core.k:124-127` |
| Function closure, name, and call | `functions.k:14-16`; `core.k:130-155`; `call.k:20-21,69-75`; `functions.k:63-85` |
| `Attribute(..., "count")` and method call | `call.k:16,20-23,26`; `methods.k:34-45` |
| `Str`, `Int` | `str.k:12-17`; `core.k:188`; all literals are ASCII |
| `If`, `Return` | `controls.k:51-54`; `functions.k:78-90` |
| `Compare` | `operators.k:14-17`; `str.k:25-31`; `int.k:24,27` |
| `UnaryOp("not", ...)`, unary `-4` | `operators.k:10`; `bool.k:8`; `int.k:7` |
| `BoolOp("or", ...)` | `bool.k:16-25` |
| Integer `BinOp("+", ...)` | `operators.k:12`; `int.k:9` |
| `Subscript(s, 0)` | `subscript.k:25-41`; nonempty before reachability |
| `Subscript(s, Slice(-4, NoBound, NoBound))` | `subscript.k:44-69,72-121` |

## Proof-local extensions

| Extension | Classification and complete decision |
|---|---|
| `fileNameCheckBody` syntax/rule | Parse-time macro, not an operational bridge. Fresh expanded KORE is byte-identical to `solution.mpy` (`04-program-identity.log`). Changing its actual final return makes `SPEC.valid-name-txt` fail with the fixed result `"No"` (`04-kprove-body-mutation-isolated.log`). |
| `decimalDigitCount(CS)` | Definitional summary used only in preconditions. Its one unguarded equation is total, nonoverlapping, and exactly the left-associated sum of the ten source singleton `count` calls. |
| `fileExtensionIs(CS, EXT)` | Definitional summary used only in preconditions. Its one unguarded equation is exactly fixed `doSlice(str(CS), someB(-4), noB, noB)` followed by fixed string equality. |
| `allowedFileExtension(CS)` | Definitional summary used only in the invalid-extension precondition. One unguarded equation enumerates `.txt`, `.exe`, `.dll`; there is no overlap. |
| `N >Int 3 => false requires N <=Int 3 [simplification]` | Derived mathematical lemma. Its complete domain is the guard `N <= 3`, on which the conclusion is true. The same reachability implication closes under an independently rebuilt MPY-only definition (`03-kprove-lemma.log`). It affects only the valid-name branches. |

There are no proof-local opaque symbols, operational bridges, priority rules,
loop circularities, or rules that synthesize the task result. No false
conclusion witness exists for a proof-local rule. The fixed semantics'
opaque float/sort/MD5 primitives and totalized out-of-bounds list accessor are
explicitly inventoried but absent from this theorem's dependency slice.
