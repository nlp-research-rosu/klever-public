# Submitted-program constructor and rule map

The normalized `solution.mpy` uses `Module`, `FuncDef`, `Params`, `Name`,
`Int`, `Assign`, `While`, `Compare`, `CmpOp`, `AugAssign`, and `Return`, plus
the `Stmts`/`ParamNames` list productions.

| Constructor or effect | Declaration | Material fixed-semantics path |
|---|---|---|
| `Module` | `semantics/syntax.k:61` | `core.k:49-60` config, `core.k:124-127` module load/sequencing |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` installs the exact `closureVal` body |
| `Call`, `Name` | `syntax.k:12,28` | `call.k:20-21`; `core.k:131-154` lookup; `call.k:69-74` frame creation |
| argument `Int(N)` | `syntax.k:9` | `core.k:189-196` left-to-right argument evaluation/literal reduction |
| parameter binding | `core.k` value/list declarations | `functions.k:63-75` binds `n=N` in the fresh current scope |
| `Assign(total,0)` | `syntax.k:41` | strict RHS evaluation then `controls.k:9-18` current-scope update |
| `While` | `syntax.k:46` | `controls.k:65-82` expands to `#while`, evaluates the guard, executes body, and loops |
| `Compare(n, > 0)` | `syntax.k:30-32` | `operators.k:15-17`; `int.k:24` implements mathematical integer `>` |
| guard truth | `core.k` `truthy` | `core.k:199-205`, in particular nonzero integer truth |
| `AugAssign(total,+,n)` | `syntax.k:44` | `controls.k:20-31`; `int.k:9` mathematical integer addition |
| `AugAssign(n,-,1)` | `syntax.k:44` | `controls.k:20-31`; `int.k:13` mathematical integer subtraction |
| local `Name` reads/writes | `syntax.k:12` | `core.k:131-154`; `controls.k:9-31`; plain frames make cell-only priority rules inapplicable |
| `Return(total)` | `syntax.k:50` | strict evaluation; `functions.k:78-90` records return, restores caller frame, and preserves the continuation |

The entry claims start after module loading but bind `sum_to_n` to the exact
constructor body produced by the trusted translator. The loop claim starts at
the exact internal `#while` head reached by `controls.k:77`; it does not add an
ordinary operational rewrite.
