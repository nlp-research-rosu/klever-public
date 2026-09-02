# Used-construct and rule map

This map covers every constructor in the submitted `solution.mpy`; the
sentence-level source inventory and disposition for every selected-semantics
and proof-local K sentence are in `rule-inventory.tsv` and
`rule-assessment.tsv`.

| Submitted construct | Declaration | Fixed-semantics execution path |
|---|---|---|
| `Module`, statement sequence | `semantics/syntax.k:56,61` | `core.k:124-127` loads and sequences the exact module |
| `ImportFrom("typing","List")` | `syntax.k:43` | `controls.k:35-44`; non-`math` import is a no-op |
| `FuncDef`, `Params` | `syntax.k:53,57,60` | `functions.k:14-16` installs the closure in module scope |
| `Call`, `Name` | `syntax.k:12,28` | `core.k:129-191` lookup/evaluation; `call.k:20-21,69-75` callee, arguments, and frame |
| Boolean/integer/float literals | `syntax.k:9-12` | `core.k:193-196`; `float.k:19-21` |
| `Assign(Name, expr)` | `syntax.k:41` | `controls.k:9-18`; updates the active local scope |
| `For` | `syntax.k:45` | `controls.k:62-74`; iterator protocol and loop continuation |
| List iteration | `core.k:13-29`; `iter.k:8` | `list.k:8-10` handles only canonical `.ValSeq`/`vCons` lists |
| Loop target binding | `tuple.k:31` | `tuple.k:32-41` binds each yielded element to the loop name |
| `If` | `syntax.k:49` | `controls.k:50-54`; evaluates condition then chooses one branch |
| `BinOp("+", int, int)` | `syntax.k:15`; `core.k:209` | `operators.k:12`; `int.k:9` |
| `Compare(i,"!=",j)` | `syntax.k:30-32`; `core.k:210` | `operators.k:15-17`; `int.k:27` |
| `BinOp("-", float, float)` | same operator path | `float.k:103-105` produces opaque `subF`, with a concrete LLVM equation |
| builtin `abs(float)` | builtin registry `core.k:157-181` | `call.k:20-31`; `float.k:54-56` produces opaque `absF`, with concrete equation |
| `Compare(float,"<",float)` | comparison path above | `float.k:50-52` produces opaque `floatLt`, with concrete equation |
| `Return` | `syntax.k:50` | `functions.k:77-90`; stores result, pops frame, restores caller |
| Complete runtime state | `core.k:49-60` | Entry post-state pins scope allocation, heap, stack, return/exception/exit state |

The candidate adds `floatVals(FloatSeq)` as a third proof-only `ValSeq`
constructor and then adds priority-40 iterator rules for it. Those two rules do
not execute the `list.k:9-10` runtime representation; they supply behavior for
a state on which the fixed list iterator is stuck.
