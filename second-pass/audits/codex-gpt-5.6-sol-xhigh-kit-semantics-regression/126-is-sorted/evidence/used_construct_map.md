# Real-program construct and state map

The submitted `solution.mpy` uses only these AST constructors:

| Submitted construct | Declaration | Executing declarations/rules |
|---|---|---|
| `Module`, `Stmts` | `semantics/syntax.k:56-61` | `#loadAll` and statement sequencing, `semantics/core.k:123-127` |
| `FuncDef`, `Params` | `semantics/syntax.k:53-60` | closure installation, `semantics/functions.k:13-16` |
| `Call`, `Name` | `semantics/syntax.k:12,28` | lookup, `semantics/core.k:129-181`; callee/arguments/frame creation, `semantics/call.k:18-21,69-74` |
| `Assign` | `semantics/syntax.k:41` (`strict(2)`) | current-scope write, `semantics/controls.k:8-18` |
| `Int`, `Bool` | `semantics/syntax.k:9,11` | literal cooling, `semantics/core.k:193-196` |
| `UnaryOp("-")` | `semantics/syntax.k:14` (`strict(2)`) | dispatch, `semantics/operators.k:10`; integer negation, `semantics/int.k:7` |
| `For` over `list` | `semantics/syntax.k:45` (`strict(2)`) | loop protocol, `semantics/controls.k:62-74`; list iterator, `semantics/list.k:8-10`; target binding, `semantics/tuple.k:30-41` |
| `If` | `semantics/syntax.k:49` (`strict(1)`) | truth conversion and branch choice, `semantics/controls.k:50-54`; Boolean truth, `semantics/core.k:198-205` |
| `Compare("<"|"==")` | `semantics/syntax.k:30-32` | left-then-right contexts and dispatch, `semantics/operators.k:14-17`; integer comparisons, `semantics/int.k:22-27`; guarded proof simplifications, `verification.k:62-74` |
| `Return` | `semantics/syntax.k:50` (`strict`) | return state and frame cleanup, `semantics/functions.k:77-90` |

State transition:

1. `#loadAll` installs the exact `is_sorted` closure in module scope 0.
2. `Call` evaluates the closure and the unboxed read-only `list(VALUES)`
   argument, allocates scope 1, changes `env` 0→1 and `scopeLoc` 1→2, and pushes
   `frame(.K,0,1)`.
3. `#bindP` binds `lst`; the three initialization assignments bind
   `previous=-1`, `duplicates=0`, and `value=0`.
4. Each list iterator step binds `value`, evaluates the two comparisons in
   order, may return `false`, otherwise updates the duplicate flag and
   predecessor. The trailing `Return(true)` handles exhaustion.
5. `#pop` restores `env=0`, removes scope 1, restores `scopeLoc=1`, clears the
   frame and `ret`, and leaves the returned Boolean at `<k>`.

The input is an unboxed `list(ValSeq)` and the body allocates nothing, so
`heap=.Map` and `heapLoc=0` remain unchanged. No exception or exit-code rule is
reachable under `nonNegativeInts`.
