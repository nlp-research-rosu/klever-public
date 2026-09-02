# Stage 5 local declaration and rule inventory

Source under review: fresh copies of `/candidate/semantic.k`,
`/candidate/verification.k`, and `/candidate/spec.k`. Line numbers below refer
to the candidate files.

## Declarations and attributes

`semantic.k` declares:

- `Pgm`: `Module(Stmts)`, `run(Pgm,Val,Val)`, and `programLoaded`.
- `Stmts`: one statement or a juxtaposed nonempty sequence.
- `Stmt`: `FuncDef(String,Params,Stmts)` and `Return(Expr)`.
- `Params`: exactly two string parameters.
- `Expr`: `Name`, `Int`, `UnaryOp`, `BoolOp`, `Compare`, `Call`, and
  `Subscript`.
- `CmpOp`, `Slice`, `NoBound`, integer-list constructors `nil`/`cons`, and
  value constructors `pyInt`/`pyBool`/`pyList`.
- `Env`: `env(Val,Val)`.
- Fifteen semantic/helper function symbols across the two source modules:
  `eval`, `negate`, `reverseVal`, `sumVal`, `compare`, `boolAnd`, `getInt`,
  `sumInts`, `reverseInts`, `reverseAcc`, `equalVals`, `equalIntLists`,
  `balanced`, `withinWeight`, and `canFly`.
- One macro symbol, `solutionProgram`.

All syntax productions have `symbol` attributes. The fifteen symbols named
above have `function`; none has `total`. There are no `functional`,
`simplification`, `priority`, `owise`, or `anywhere` attributes, no local
opaque result symbols, and no side-conditioned rules. `solutionProgram` alone
has `macro`.

The configuration is only `<k> $PGM:Pgm </k>` (`semantic.k:45`). This is
adequate for the submitted pure expression: it has no assignment, heap,
allocation, I/O, exceptions on the formal domain, user-call stack, or mutable
state. K adds the standard generated counter cell used by the claims.

## Operational and functional rules

| ID | Source | Rule | Judgment on the submitted program and formal domain |
|---|---|---|---|
| S1 | `semantic.k:49-50` | A loaded one-function `Module` becomes `programLoaded`. | Faithful load result; it is not used as a value oracle. |
| S2 | `semantic.k:52-55` | `run` of the exact `will_it_fly(q,w)` body becomes `eval(E,env(Q,W))`. | Faithful invocation of the actual retained body and binding. |
| S3 | `semantic.k:66` | `eval(Name("q"),env(Q,W)) = Q`. | Correct exact parameter lookup. |
| S4 | `semantic.k:67` | `eval(Name("w"),env(Q,W)) = W`. | Correct exact parameter lookup. |
| S5 | `semantic.k:68` | Integer AST literal becomes `pyInt`. | Correct for Python unbounded integers. |
| S6 | `semantic.k:69` | Unary `-` delegates to `negate`. | Correct; the exact slice is also recognized structurally by S7. |
| S7 | `semantic.k:70-74` | Exact `E[::-1]` slice delegates to list reversal. | Correct for the submitted integer-list slice. |
| S8 | `semantic.k:75` | Exact `sum(E)` call delegates to `sumVal`. | Correct with the unshadowed builtin binding in `solution.py`. |
| S9 | `semantic.k:76` | Comparison evaluates its left value and dispatches to `compare`. | Correct; both actual operands are pure. |
| S10 | `semantic.k:77-78` | `and` evaluates both operands and delegates to `boolAnd`. | Result-correct for the exact two pure, total Boolean comparisons. It is eager rather than Python-short-circuiting for arbitrary other ASTs; that is outside this submitted program. |
| S11 | `semantic.k:80` | `negate(pyInt(I)) = pyInt(-I)`. | Ordinary integer arithmetic. |
| S12 | `semantic.k:81` | Reverse an integer list with `reverseInts`. | Correct constructor bridge. |
| S13 | `semantic.k:82` | Sum an integer list with `sumInts`. | Correct constructor bridge. |
| S14 | `semantic.k:83-84` | `==` compares evaluated values with `equalVals`. | Correct for the actual list/list comparison. |
| S15 | `semantic.k:85-86` | `pyInt(I) <= E` compares `I` with evaluated integer `E`. | Correct for `sum(q) <= w`. |
| S16 | `semantic.k:87` | Boolean conjunction uses `andBool`. | Ordinary Boolean conjunction. |
| S17 | `semantic.k:91` | `getInt(pyInt(I)) = I`. | Correct and reached only on `pyInt(W)`. |
| S18 | `semantic.k:92` | `sumInts(nil) = 0`. | Correct base case. |
| S19 | `semantic.k:93` | `sumInts(cons(I,IS)) = I + sumInts(IS)`. | Correct structurally decreasing recursion. |
| S20 | `semantic.k:98` | `reverseInts(IS) = reverseAcc(IS,nil)`. | Correct accumulator initialization. |
| S21 | `semantic.k:99` | `reverseAcc(nil,ACC) = ACC`. | Correct base case. |
| S22 | `semantic.k:100` | Move the head of the input to the accumulator. | Correct structurally decreasing reversal. |
| S23 | `semantic.k:105` | Integer value equality uses `==Int`. | Ordinary equality. |
| S24 | `semantic.k:106` | Boolean value equality uses `==Bool`. | Ordinary equality. |
| S25 | `semantic.k:107` | List value equality delegates to `equalIntLists`. | Correct constructor bridge. |
| S26 | `semantic.k:108` | `nil == nil` is true. | Correct base case. |
| S27 | `semantic.k:109` | `nil == cons(...)` is false. | Correct disjoint-shape case. |
| S28 | `semantic.k:110` | `cons(...) == nil` is false. | Correct disjoint-shape case. |
| S29 | `semantic.k:111-112` | Two cons lists are equal iff heads and tails are equal. | Correct structurally decreasing recursion. |

The function equations are shape-disjoint wherever they share a head symbol:
the two names differ by fixed string; comparisons differ by fixed operator;
sums and reversals split on `nil`/`cons`; `equalVals` splits on value
constructor; and list equality's four shape combinations are disjoint. The
equations cover every reachable value shape for `IntList` inputs and integer
`W`. There are no priorities or overlapping right-hand sides to reconcile.

## Proof-local rules

| ID | Source | Rule | Class and judgment |
|---|---|---|---|
| V1 | `verification.k:12` | `balanced(IS) = equalIntLists(IS,reverseInts(IS))`. | Truthful definitional summary of palindrome. |
| V2 | `verification.k:13` | `withinWeight(IS,W) = sumInts(IS) <= W`. | Truthful definitional summary. |
| V3 | `verification.k:14` | `canFly = balanced and withinWeight`. | Truthful contract conjunction. |
| V4 | `verification.k:18-33` | `solutionProgram` macro expands to the constructor tree. | Syntax abbreviation, not an operational bridge; the normalized RHS is identical to `solution.mpy`. |

V1-V3 do not replace program execution. They define the postcondition using the
same audited mathematical operations that the semantics assigns to list
reversal, equality, and sum. V4 is expanded before execution.

## Claim inventory and construct coverage

`spec.k` has five entry claims and no helper/loop claims: one universal
`IntList`/`Int` claim and four ground example claims. There are no loops in the
submitted program.

| Submitted construct | Declaration and behavior |
|---|---|
| `Module`, one `FuncDef`, `Params`, `Return` | `Pgm`/`Stmt`/`Params` declarations; S2 invokes the retained return expression. |
| `BoolOp("and",...)` | `Expr` declaration; S10 and S16. |
| `Name("q")`, `Name("w")` | `Expr`; S3 and S4. |
| List equality `==` | `Compare`/`CmpOp`; S9, S14, S25-S29. |
| `q[::-1]` | `Subscript`/`Slice`/`NoBound`/`UnaryOp`/`Int`; S7 and S20-S22. |
| `sum(q)` | `Call`; S8, S13, S18-S19. |
| Integer `<=` | `Compare`/`CmpOp`; S9, S15, S17. |
| Input/output values | `pyList`, `pyInt`, `pyBool`; all reachable helper rules preserve these shapes. |

The only fidelity limitation is S10's eager evaluation for arbitrary other
programs. A term such as a false left operand followed by an unbound name would
short-circuit in Python but can get stuck here. That term is neither the
submitted body nor reachable from any intended integer-list/integer input.
Accordingly this is an out-of-scope language-model limitation, not an
unsoundness witness on the intended domain. No local rule permits a false
conclusion for the submitted program on that domain.
