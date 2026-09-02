# Material construct map

The executed program term is the byte-identical expanded term recorded in
`stage4-program-pinning.log`. The following source declarations and rule
families cover every constructor on that term's reachable path.

| Program constructor / effect | Declaration | Operational rules |
|---|---|---|
| `Module`, statement lists | `semantics/syntax.k:56-61` | `core.k:124-127` loads and sequences the module |
| `FuncDef`, `Params`, binding | `semantics/syntax.k:53-60` | `functions.k:14-16`, `call.k:69-75`, `functions.k:63-66` |
| `Call`, left-to-right callee/argument evaluation | `semantics/syntax.k:28`, `core.k:185-191` | `call.k:19-21`, `call.k:69-75` |
| `Name` lookup | `semantics/syntax.k:12` | `core.k:130-154` |
| `Str` literals and strings-as-code-sequences | `semantics/syntax.k:13`, `core.k:13-15,25-40` | `str.k:13-17`; all submitted literals are ASCII |
| `Assign` | `semantics/syntax.k:41` (strict RHS) | `controls.k:9-18`; ordinary non-cell branch is reachable |
| `For` and string iteration | `semantics/syntax.k:45` (strict iterable) | `controls.k:65-74`, `str.k:8-10` |
| Loop target binding to `char` | `tuple.k:31` | `tuple.k:32-41`; ordinary non-cell branch is reachable |
| `If` and Boolean truth | `semantics/syntax.k:49` (strict guard) | `controls.k:51-54`, `core.k:199-205`; only the Boolean case is used |
| `Compare(..., "not in", ...)` | `semantics/syntax.k:30-32`, contexts `operators.k:15-16` | `operators.k:17`, `str.k:29-41`, and exact specialization `verification.k:21-23` |
| String membership specialization | `verification.k:6-23` | The priority-40 rule is pure and exact; the bridge-free 21-case exhaustive connection proof is in `connection-*.k` and `stage5-bridgefree-kprove.log` |
| `AugAssign(result, "+", char)` | `semantics/syntax.k:44` (strict RHS) | `controls.k:20-31`, `str.k:20-24`; ordinary non-reference branch is reachable |
| `Return` and frame pop | `semantics/syntax.k:50` (strict result) | `functions.k:78-90` |
| Filter result summary | `verification.k:25-38` | Structural recursion over `IntSeq`; base/vowel/non-vowel guards are complete and disjoint |
| Source/claim syntax macros | `verification.k:40-57` | Macro expansion is byte-identical at KORE level to freshly translated `solution.mpy` |
| State/configuration | `core.k:49-60` | Entry claim pins every cell; loop claims modify only `result` and `char` and frame all other state |

The remaining supplied declarations are unreachable from this program term.
They remain part of the immutable supplied-semantics trust boundary. In
particular, all 22 `no-evaluators` opaque declarations are confined to float,
MD5, and sorting operations that do not appear here. There are no local
`simplification` or `functional` declarations anywhere in the inventoried
sources, and the candidate adds no opaque symbol.
