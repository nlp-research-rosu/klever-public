# `solution.mpy` construct-to-semantics map

The supplied semantics tree is byte-identical to `/reference/reference-semantics`.
The exhaustive declaration/rule list is in `rule-inventory.txt`; this map isolates
the rules reachable from the submitted program.

| Submitted construct | Declaration | Operational rules |
|---|---|---|
| `Module`, statement sequencing | `semantics/syntax.k:61`, `semantics/syntax.k:56` | initial `<k>` and cells at `semantics/core.k:49`; `#loadAll` and statement sequencing at `semantics/core.k:124-127` |
| `FuncDef`, `Params`, function closures | `semantics/syntax.k:53-54,57`; closure/frame syntax at `semantics/core.k:31` and `semantics/functions.k:8-11` | definition at `semantics/functions.k:14-16`; call/frame setup at `semantics/call.k:69-75`; parameter binding and return/pop at `semantics/functions.k:63-90` |
| `Name` | `semantics/syntax.k:12` | lookup and parent traversal at `semantics/core.k:130-154`; builtin root at `semantics/core.k:157-181` |
| `Int(0)`, `Int(1)` | `semantics/syntax.k:9` | literal cooling at `semantics/core.k:193-196` |
| `Assign(Name("i"), Int(0))` | `semantics/syntax.k:41` | current-frame write at `semantics/controls.k:9-18` |
| `Call` and argument lists | `semantics/syntax.k:28`, `semantics/syntax.k:37` | callee lookup/routing at `semantics/call.k:18-32`; left-to-right arguments at `semantics/core.k:183-191` |
| `len(string)` | builtin binding at `semantics/core.k:159` | dispatch and string length at `semantics/builtins.k:17-26`; `isLen` recursion at `semantics/core.k:227-229` |
| `range(len(string))` | builtin binding at `semantics/core.k:167`; `rangeObj` at `semantics/core.k:21` | constructor at `semantics/builtins.k:176-180`; iterator at `semantics/range.k:9-24` |
| `For` | `semantics/syntax.k:45` | `For` to `#loop`, iterator step, target binding, and continuation at `semantics/controls.k:62-74`; name target binding is declared/rule-driven in `semantics/tuple.k` |
| `If` | `semantics/syntax.k:49` | strict condition plus `truthy` branch at `semantics/controls.k:50-54`; boolean truth at `semantics/core.k:198-205` |
| `Subscript`, `Slice`, `NoBound` | `semantics/syntax.k:22,38-39` | evaluation order at `semantics/subscript.k:25-61`; slice index normalization and `buildIS` at `semantics/subscript.k:63-121` |
| `UnaryOp("-", Int(1))` | `semantics/syntax.k:14` | dispatch at `semantics/operators.k:10`; integer negation at `semantics/int.k:7` |
| `Compare(..., CmpOp("==", ...))` | `semantics/syntax.k:30,32` | left/right evaluation and dispatch at `semantics/operators.k:14-17`; string equality at `semantics/str.k:24-26` |
| `BinOp("+", string, reverse_prefix)` | `semantics/syntax.k:15` | dispatch at `semantics/operators.k:12`; string concatenation and `seqConcat` at `semantics/str.k:20-24` |
| `Return` | `semantics/syntax.k:50` | return value, frame pop, environment restoration, scope deletion, and continuation restoration at `semantics/functions.k:77-90` |

No submitted construct reaches the opaque float, sorting, or MD5 symbols listed
in `rule-inventory.txt`.
