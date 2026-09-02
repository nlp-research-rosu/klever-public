# Candidate-local rule and declaration inventory

Scope: `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`, reviewed from the scratch copies. The candidate contains
no other K source/helper file. Imported K `INT`, `BOOL`, and collection
definitions are distribution primitives, not candidate-local rules.

## Local syntax and configuration

`MPY-SYNTAX` declares every constructor below:

1. `Pgm`: `Module(Stmts)`.
2. `Stmts`: unseparated list of `Stmt`.
3. `Strings`: comma-separated list of `String`.
4. `Params`: `Params(Strings)`.
5. `Stmt`: `ImportFrom(String,Strings)`, `FuncDef(String,Params,Stmts)`,
   `If(Expr,Stmts,Stmts)`, and `Return(Expr)`.
6. `Exprs`: comma-separated list of `Expr`.
7. `Expr`: `Name(String)`, `Int(Int)`, `Call(Expr,Exprs)`,
   `Compare(Expr,CmpOp)`, `BinOp(String,Expr,Expr)`, `ListExpr(Exprs)`, and
   `Subscript(Expr,Index)`.
8. `CmpOp`: `CmpOp(String,Expr)`.
9. `Bound`: `Expr` or `NoBound`.
10. `Index`: injected `Expr` or `Slice(Bound,Bound,Bound)`.
11. `Ints`: comma-separated list of mathematical K `Int`.
12. `Val`: `VInt(Int)`, `VBool(Bool)`, or `VList([Ints])`.
13. `Vals`: comma-separated list of `Val`.
14. `Run`: `Invoke(Pgm,String,Vals)`.

`MPY` declares `Env = env(Ints,Int)` and eleven `KItem` control constructors:
`exec`, `eval`, `decide`, `listSecond`, `makePair`, `binopRight`,
`concatWith`, `concat`, `prepend`, `callSecond`, and `callWith`.

The sole configuration is `<k> $PGM:Run </k>`. There are no binding, heap,
stack, output, exception, or allocation cells. That is sufficient for the
submitted body at pure integer-list value level, but cannot express Python
object identity, aliasing, recursion limits, or exceptions.

`VERIFICATION` adds one syntax declaration:
`intersperseSpec(Ints,Int):Ints [function,total]`.

There are no candidate-local `functional`, `simplification`, `concrete`,
`priority`, `owise`, `anywhere`, `macro`, or `alias` declarations; no local
opaque symbols; and no priority blocks.

## Construct coverage map

| Submitted construct | Declaration | Executing rules |
|---|---|---|
| `Module` containing `ImportFrom` and `FuncDef` | Pgm/Stmt/Params/Strings | S1 entry pattern |
| `If(len(numbers) <= 1, ...)` | If, Compare, Call, Name, CmpOp, Int | S3, S4/S5, S9-S11 |
| `Return` | Return | S2 |
| `numbers`, `delimeter`, integer literals | Name, Int | S6-S8 |
| `numbers[0]` | Subscript/Index | S12 |
| `numbers[1:]` | Subscript/Slice/Bound | S13 |
| `[numbers[0], delimeter]` | ListExpr/Exprs | S14-S16 |
| list `+` | BinOp | S17-S22 |
| recursive `intersperse(...)` | Call/Exprs | S23-S25, then S1 |

Every submitted constructor is both declared and covered on every state
reachable from an intended `VList([IS]), VInt(D)` invocation. Unused variants
of the broad declarations are deliberately not covered.

## Operational rules in `semantic.k`

The status column judges behavior on all states reachable from the exact
submitted program and intended input sort (finite integer sequences and an
integer delimiter).

| ID / lines | Rule | Review |
|---|---|---|
| S1 / 63-72 | `Invoke` exposes the matched function body and creates `env(IS,D)` | Correct for the pinned module, function name, parameter order, and two typed arguments. It preserves the parsed Pgm for recursion. Its pattern is broader than its justification because it ignores the actual parameter names and import names; this is a reuse/generalization gap, not a false transition reachable for the pinned program. |
| S2 / 74 | `exec(Return(E) REST)` evaluates `E` and discards following body statements | Correct Python return control for this body; the outer K continuation is preserved. |
| S3 / 75-77 | `exec(If...)` evaluates the condition then records branches/rest | Correct test-before-branch order. |
| S4 / 78-79 | true decision executes `THEN`, discarding `_REST` | On the exact body, `THEN` is a single `Return`, so discarding following source statements is correct. The rule is too broad for an arbitrary normally-completing then-suite; because no empty-suite completion rule exists, the wider case becomes stuck rather than enabling a wrong intended result. Narrow generated-semantics coverage concern only. |
| S5 / 80-81 | false decision with empty else executes `REST` | Correct and exact for the submitted empty else. Nonempty else is intentionally unmodeled and stuck. |
| S6 / 83 | lookup `numbers` from the first Env field | Correct for the pinned binding and body. |
| S7 / 84 | lookup `delimeter` from the second Env field | Correct for the pinned binding and body. |
| S8 / 85 | evaluate integer literal | Exact mathematical-integer value. |
| S9 / 90-93 | `len(numbers) <= 1` on empty list -> true | Correct. |
| S10 / 94-97 | same test on singleton -> true | Correct. |
| S11 / 98-101 | same test on at-least-two list -> false | Correct. S9-S11 are structurally disjoint and exhaustive for finite `Ints`. |
| S12 / 103-105 | `numbers[0]` on nonempty list -> head | Correct; reachable only after S11, so no empty-index exception is silently fabricated. |
| S13 / 106-109 | `numbers[1:]` on nonempty list -> tail | Correct at integer-list value level; allocation and identity are outside the configuration. |
| S14 / 111-112 | begin two-element `ListExpr`, evaluating E1 first | Correct for the exact two-element literal. Other arities are unmodeled. |
| S15 / 113-114 | after E1, evaluate E2 | Correct left-to-right order. |
| S16 / 115 | assemble two integer values as `[I,J]` | Correct; intended elements are integers. |
| S17 / 117-118 | begin `+`, evaluating left operand first | Correct Python operand order. |
| S18 / 119-120 | after left value, evaluate right | Correct. |
| S19 / 121 | dispatch evaluated values to `concat` | Correct for reachable list/list operands; other types get stuck rather than fabricated. |
| S20 / 122 | `[] + JS -> JS` | Correct value sequence. It does not model allocation/identity. |
| S21 / 123-124 | recursively concatenate a nonempty left list | Correct structural recursion; the left length strictly decreases. |
| S22 / 125 | prepend saved head to recursive result | Correct order. |
| S23 / 127-128 | begin recursive call, evaluating E1 first | Correct call-argument order for the exact direct call. Function expression/binding lookup is hardwired, acceptable only because the pinned source never rebinds the name. |
| S24 / 129-130 | after E1, evaluate E2 | Correct. |
| S25 / 131-132 | invoke the same Pgm with evaluated list and delimiter | Correct recursive control and value binding for the pinned program. |

The operational heads are disjoint on reachable configurations. There are no
guards or priorities. S9-S11 and S20-S21 are the only same-operation families;
their list-shape cases do not overlap.

## Proof-local function rules in `verification.k`

| ID / lines | Equation | Review |
|---|---|---|
| V1 / 9 | `intersperseSpec([],D) = []` | True base case. |
| V2 / 10 | `intersperseSpec([I],D) = [I]` | True singleton case. |
| V3 / 11-12 | `intersperseSpec(I,J,REST,D) = I,D,intersperseSpec(J,REST,D)` | True recurrence for length at least two; decreases length by one. |

V1-V3 are pairwise disjoint and exhaustive over finite `Ints`, so the local
`[function,total]` declaration is justified. The symbol appears only in the
postcondition and its own equations; it never replaces program execution and
is therefore a definitional summary, not a result-bearing oracle or
operational bridge.

## Claim inventory

`spec.k` contains exactly one unlabeled entry claim and no helper claims. Its
recursive call returns to the same `Invoke` configuration with the same parsed
program and delimiter and a one-element-shorter list, so the entry claim itself
is the circularity matching real recursive control flow.

There are no proof-local operational rules, lemmas, simplifications, opaque
symbols, or priority rules. The proof's only local extension is V1-V3.
