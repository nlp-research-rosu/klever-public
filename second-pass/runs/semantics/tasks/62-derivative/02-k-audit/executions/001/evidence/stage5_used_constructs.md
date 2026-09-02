# Used-program construct map

This map covers every constructor in the submitted `solution.mpy`. Line
references are to the fresh scratch copy of the byte-verified supplied
semantics.

| Submitted construct | Syntax declaration | Execution rules on this program path | Audit result |
|---|---|---|---|
| `Module(Stmts)` | `semantics/syntax.k:56-61` | `core.k:123-127` loads and sequences statements. | Matches module sequencing. Entry claims start after module load but bind the exact closure macro; fresh `krun` covered module loading. |
| `FuncDef`, `Params` | `syntax.k:53-60` | `functions.k:14-16` installs `closureVal`; `call.k:69-74` allocates a call frame and binds parameters via `functions.k:62-75`. | Exact one-parameter closure and lexical parent 0. |
| `Expr(Str(...))` docstring | `syntax.k:13,52` | `str.k:13-17` evaluates the ASCII string; `controls.k:46-48` discards the resulting value. | No result or state influence beyond normal expression evaluation. |
| `Assign(Name("result"), ListExpr())` | `syntax.k:17,41` | `list.k:13-15` and `core.k:183-191` evaluate the empty literal; `core.k:117-121` allocates it; `controls.k:9-18` binds the resulting reference. | Creates one fresh mutable result object, as required. |
| `For(TupleExpr(...), Call(Name("enumerate"), Name("xs")), ...)` | `syntax.k:21,28,30,45` | Names use `core.k:129-154`; calls use `call.k:18-32`; `builtins.k:123-129` eagerly materializes enumerate pairs; `controls.k:62-74,104-108` dereferences the fresh enumerate list and drives `#iterNext`; tuple target binding uses `tuple.k:30-57`. | Fixed path is faithful. Candidate `verification.k:39-51` replaces the symbolic enumerate sequence and is rejected separately. |
| `If(Compare(Name("i"), CmpOp(">", Int(0))), ..., .Stmts)` | `syntax.k:9,30,32,49` | strictness/contexts evaluate operands left-to-right (`syntax.k:14-15`, `operators.k:14-17`); `core.k:131-154,193-205` handles lookup/literal/truth; `int.k:22-27` supplies integer comparison; `controls.k:50-54` selects the branch. | Index 0 skips; every index greater than 0 takes the append branch. |
| `Call(Attribute(Name("result"), "append"), BinOp("*", Name("i"), Name("x")))` | `syntax.k:15,28-29` | `call.k:15-32` cools the receiver and evaluates arguments; `operators.k:10-17` dispatches the binop; `int.k:14` computes unbounded integer multiplication; `list.k:52-55` appends in place; `controls.k:46-48` discards `noneV`. | Correct evaluation order, multiplication, aliasing, and in-place heap update. |
| `Return(Name("result"))` | `syntax.k:50` | lookup is `core.k:129-154`; `functions.k:77-90` records the returned reference, pops the frame, restores the caller environment, and preserves heap allocation. | Returned reference is the same object constrained by the entry postcondition. |
| Empty `Exprs`/`Stmts` and sequence constructors | `syntax.k:36-37,56` | `core.k:125-127,183-191` supplies empty and nonempty sequencing/evaluation cases. | Coverage is complete for all emitted list forms. |

## Configuration and state footprint

The authoritative configuration is `core.k:49-60`: `<k>`, current `<env>`,
scope map/allocation counter, heap/allocation counter, frame stack, return
state, exception state, and exit code. The actual used path reads or updates
all of these except the exit code: calls allocate/remove a scope frame,
list/enumerate constructors allocate heap objects monotonically, append updates
only the result heap object, return restores the caller frame, and no exception
is raised for finite integer lists.

The candidate loop claim omits some cells, which K frames. Its explicit
footprint is the current environment, the local scope bindings, the result heap
entry, and the computation/continuation. The proof-local `#iterNext` rules also
frame every non-`<k>` cell and preserve the arbitrary continuation
syntactically.

## Fixed semantics versus proof-local rules

- `asValSeq` and `derivativeAcc` are structural, descending definitions with
  disjoint reachable cases.
- `derivativeAcc` deliberately has no `N < 0` equation and is not declared
  total. Every entry use starts at 0; recursive calls advance to 1 and upward;
  the loop invariant requires `N > 0`.
- `derivativeTarget`, `derivativeLoopStep`, and `derivativeClosure` expand to
  the exact submitted constructor subtrees.
- `enumIntSeq` is a new inhabitant of the existing `ValSeq` sort. The extended
  LLVM build warns that inherited total helpers such as `vsLen`,
  `valSeqConcat`, `enumVS`, and `valSeqAt` are non-exhaustive on it. More
  importantly, the global simplification is inconsistent with the fixed
  semantics, as demonstrated by the preserved symbolic/ground witness logs.
