# Executed-constructor and rule map

This map is for the exact submitted `solution.mpy`. Line references point to
the candidate's byte-identical copy of the supplied semantics.

| Submitted constructor | Declaration | Rules exercised or connection |
|---|---|---|
| `Module` | `semantics/syntax.k:61` | Concrete execution uses `#loadAll` and statement sequencing at `semantics/core.k:124-127`. The entry claims start after module loading, with the `eat` binding installed; the translator-derived constructor comparison and pinning claim connect that binding to the sole submitted `FuncDef`. |
| `FuncDef("eat", ...)` | `semantics/syntax.k:53-54` | Ordinary loading uses `semantics/functions.k:14-16`, producing `closureVal(PNS,BODY,L)`. `verification.k:11-27` defines exactly that value at defining environment `0`. |
| `Params`, `Stmts` | `semantics/syntax.k:56-60` | Call dispatch and parameter binding use `semantics/call.k:69-75` and `semantics/functions.k:63-75`; statement sequencing uses `semantics/core.k:125-127`. |
| `Call` | `semantics/syntax.k:28` | Callee evaluation and left-to-right argument evaluation use `semantics/call.k:20-21`, `semantics/core.k:185-191`, and closure dispatch at `semantics/call.k:69-75`. No higher-priority math, md5, method, or builtin interception matches `Name("eat")`. |
| `Name` | `semantics/syntax.k:12` | Lookup starts at `semantics/core.k:130-154`. The claims bind `eat` in frame 0; the callee frame binds `number`, `need`, and `remaining`, so the direct in-frame rule at lines 132-134 applies. Cell-specific priority rules cannot match the plain frames. |
| `Int` | `semantics/syntax.k:9` | Literal evaluation is `semantics/core.k:194`. The symbolic arguments become K `Int` values before closure entry. |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | Truth conversion and branch selection use `semantics/controls.k:51-54`. The ref-specific priority rule at lines 95-97 cannot match the Boolean comparison result. |
| `Compare` / `CmpOp("<=")` | `semantics/syntax.k:30,32` | Left/right evaluation contexts are `semantics/operators.k:15-17`; integer `<=` is `semantics/int.k:23`. Ref-dereference priority rules do not match integer operands. |
| `BinOp("+",...)`, `BinOp("-",...)` | `semantics/syntax.k:15` (`seqstrict(2,3)`) | Dispatch is `semantics/operators.k:12`; integer addition/subtraction are `semantics/int.k:9,13`. List and ref-specific rules do not overlap the integer operands. |
| `ListExpr` | `semantics/syntax.k:17` | Elements evaluate left-to-right through `#evalArgs`; `semantics/list.k:13-15` converts them with the structural `vals2valSeq` equations at `semantics/core.k:217-219` and allocates with `semantics/core.k:117-121`. |
| `Return` | `semantics/syntax.k:50` (`strict`) | `semantics/functions.k:78-90` records the value, unwinds the function frame, restores the caller environment, and leaves the allocated list in the heap. This also makes the trailing second `Return` unreachable after the true branch, exactly like the source. |
| `eatClosure` | `verification.k:9-27` | One zero-arity functional name and one non-overlapping equation. It is a definitional summary, not an operational bridge: it expands to the exact closure constructor derived from the submitted function body. |

## Cell and control footprint

The closure call reads `<env>`, `<scopes>`, and `<scopeLoc>`; pushes a
`frame` into `<stack>`; binds three parameters in a fresh scope; executes the
condition and exactly one return expression; allocates the result list in
`<heap>` while advancing `<heapLoc>`; records and clears `<ret>` during frame
pop; restores `<env>`, `<scopes>`, `<scopeLoc>`, and `<stack>`; and preserves
`<exc> NoExc` and `<exit-code> 0`. Both claims constrain all these cells.

## Overlap and opacity result

The reachable path contains no `no-evaluators` symbol, proof oracle,
simplification rule, circularity, auxiliary loop claim, or problem-specific
operational interception. All priority rules in the fixed semantics either
implement cell/ref cases whose guards are false in these plain integer frames,
or concern constructors absent from the program. The sole proof-local equation
has no competing equation.
