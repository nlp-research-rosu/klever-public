# Exact construct-to-semantics map

The submitted `solution.mpy` uses only the constructs below. Line references
are to the trusted, byte-identical supplied semantics copied into
`/tmp/audit-work/reconstruction/reference-semantics`.

| Submitted construct | Submitted location | Syntax declaration | Operational path | Review |
|---|---:|---|---|---|
| `Module` | `solution.mpy:1` | `semantics/syntax.k:61` | Initial configuration and `#loadAll` at `semantics/core.k:49-60,124-127` | Sound fixed module-load path, but no target claim starts from this term. |
| `FuncDef`, `Params`, parameter/name lists | `solution.mpy:2` | `semantics/syntax.k:53,56-60` | Closure installation at `semantics/functions.k:14-16` | Sound fixed binding path, but bypassed by `roundedAvgCall`. |
| Statement sequencing and empty sequences | throughout | `semantics/syntax.k:56` | `semantics/core.k:126-127` | Left-to-right K sequencing. |
| `Int` | `solution.mpy:4,7-10` | `semantics/syntax.k:9` | Literal reduction at `semantics/core.k:194` | Exact mathematical K integers. |
| `Name` | `solution.mpy:3,6-10,13` | `semantics/syntax.k:12` | Scope lookup at `semantics/core.k:130-154`; builtins registry at `157-181` | Local parameters/assignments shadow parents; `bin` reaches the `-1` builtins scope. |
| `UnaryOp("-")` | `solution.mpy:4` | `semantics/syntax.k:14` (`strict(2)`) | Dispatch at `semantics/operators.k:10`; integer case at `semantics/int.k:7` | Computes `0 -Int 1`. |
| `BinOp("+","//","%")` | `solution.mpy:6-10` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | Dispatch at `semantics/operators.k:12`; integer cases and `pyMod` at `semantics/int.k:9-20` | Left-to-right evaluation; denominators are the positive constant `2`. |
| `Compare` and `CmpOp(">","==")` | `solution.mpy:3,8-9` | `semantics/syntax.k:30,32` | Evaluation contexts and dispatch at `semantics/operators.k:14-17`; integer cases at `semantics/int.k:22-27` | Truthful integer comparisons. |
| `Assign` | `solution.mpy:6-7,10` | `semantics/syntax.k:41` (`strict(2)`) | Plain/cell assignment at `semantics/controls.k:9-18` | The fresh plain call frame has no `$cells`, so the ordinary scope update applies. |
| `If` | `solution.mpy:3-5,8-12` | `semantics/syntax.k:49` (`strict(1)`) | Branching at `semantics/controls.k:50-54`; integer/boolean truth at `semantics/core.k:198-205` | Executes exactly one branch after condition evaluation. |
| `Return` | `solution.mpy:4,13` | `semantics/syntax.k:50` (`strict`) | Return/pop at `semantics/functions.k:77-90` | Produces the value, restores caller environment/scope, and discards the rest of the body. |
| `Call(Name("bin"), ...)` | `solution.mpy:13` | `semantics/syntax.k:28` | Callee/argument evaluation at `semantics/call.k:18-21` and `semantics/core.k:183-191`; builtin dispatch at `semantics/call.k:31`; binary encoding at `semantics/builtins.k:107-121` | Exact non-negative binary encoding on all satisfying valid-interval states. |
| Closure invocation used by the claims | absent from `solution.mpy`; introduced in `verification.k:29-32` | proof-local `roundedAvgCall` | Fixed call-frame rule at `semantics/call.k:69-75`; parameter binding at `semantics/functions.k:62-75` | Executes the copied body under fixed semantics, but is not linked to module loading or the submitted function binding. |

The candidate path uses no float, list, tuple, dictionary, subscript,
comprehension, range, loop, sort, method, assertion, MD5, or concrete-only
keyed-sort rule. None of the supplied opaque symbols in `float.k`, `sort.k`, or
`builtins.k:285` is reachable from these claims.
