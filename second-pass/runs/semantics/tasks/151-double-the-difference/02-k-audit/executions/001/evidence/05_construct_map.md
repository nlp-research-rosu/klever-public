# Material constructor-to-semantics map

The source body was parsed with the fresh Haskell definition. The exact KAST
body is recorded in `solution.kast.json`; `04_program_pinning.log` establishes
constructor equality with the sole entry-claim `closureVal`.

| Executed construct | Declaration/evaluation mechanism | Material rules |
|---|---|---|
| `Call(Name("double_the_difference"), ...)` | `syntax.k:28`; callee then arguments | `call.k:20-21`, `core.k:189-191`, `call.k:69-74` |
| Function binding/body | Entry scope contains `closureVal("lst", BODY, 0)` | `functions.k:14-16` is the normal module-binding rule; constructor comparison proves this is its exact binding/body |
| Name lookup | `Name(String)` | `core.k:131-154`; local hit or parent walk to builtins |
| Parameter binding | `closureVal` frame | `functions.k:63-66` |
| `Assign` | strict RHS (`syntax.k:41`) | `controls.k:9-11`; cell-write priority rule is guard-false in the exact plain frame |
| `For` | strict iterable (`syntax.k:45`) | `controls.k:69-74` |
| Standard list iteration comparator | ordinary `.ValSeq`/`vCons` | `list.k:9-10` |
| Proof-domain list iteration | `numVals(.NumSeq/iNum/fNum)` | `verification.k:16-21`; exact homomorphic shapes corresponding to `list.k:9-10` |
| Loop-target write | `#bindTgt(Name(...), V)` | `tuple.k:32-34`; cell-write priority rule is guard-false |
| `If` | strict condition (`syntax.k:49`) | `controls.k:52-54` |
| `BoolOp("and", ...)` | one-hole head context | `bool.k:16-25`; enforces left-to-right short circuit |
| `isinstance(number, int)` | ordinary name/type lookup and call | `call.k:20-21,31`; `builtins.k:291,294-295`; Int true and every other `Val` false |
| Comparisons `>`, `==` | explicit left/right contexts | `operators.k:15-17`; `int.k:24,26` |
| `%` | strict binary operands | `operators.k:12`; `int.k:15,19-20`; divisor is fixed nonzero 2 |
| `**` | strict binary operands | `operators.k:12`; `int.k:17`; exponent is fixed nonnegative 2 |
| `AugAssign("+")` | strict RHS (`syntax.k:44`) | `controls.k:20-23`; `int.k:9` |
| `Return` | strict value (`syntax.k:50`) | `functions.k:78-90`; records value and pops/restores the exact call frame |
| Integer literals | `Int(Int)` | `core.k:194` |
| Float input elements | `Float` is a `Val`; no float arithmetic is reached | `float.k:20`; `isIntV`'s disjoint fallback skips every Float |

Configuration audit:

- The entry state fixes environment 0, a module scope containing exactly the
  mechanically matched closure, the supplied builtins scope, next scope 1,
  empty heap/stack, `noRet`, `NoExc`, and exit code 0. The call rule allocates
  frame 1 and `#pop` restores those cells.
- The loop circularity fixes environment 1 and the exact local/module/builtin
  scopes. Its nested rewrites change only `total` and `number`; omitted
  configuration cells are framed. This loop performs no allocation, heap
  mutation, output, or exceptional operation.
- Candidate iterator rules have no priority attribute and cannot overlap the
  supplied `.ValSeq` or `vCons` rules because all three constructors are
  disjoint. They preserve the arbitrary continuation via `...` and introduce
  no abrupt control.
- Proof-local functions are exhaustive over the three `NumSeq` constructors;
  guards/equations do not overlap, and every recursive call structurally
  descends.
