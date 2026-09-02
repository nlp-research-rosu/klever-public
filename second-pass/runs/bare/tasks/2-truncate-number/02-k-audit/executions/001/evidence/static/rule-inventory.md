# Reviewer rule inventory

Scope: `/candidate/semantic.k`, `/candidate/verification.k`, and
`/candidate/spec.k`. There are no candidate-generated helper K source files.
Imported `domains.md` modules are K-toolchain primitives, not local rules.

## Syntax and configuration

Local productions in `SEMANTIC-SYNTAX`:

1. `Program ::= Module(Stmt)` with `[symbol(Module)]`.
2. `Stmt ::= FuncDef(String, Params, Stmt)` with `[symbol(FuncDef)]`.
3. `Stmt ::= Return(Expr)` with `[symbol(Return)]`.
4. `Params ::= Params(String)` with `[symbol(Params)]`.
5. `Expr ::= Name(String)` with `[symbol(Name)]`.
6. `Expr ::= BinOp(String, Expr, Expr)` with `[symbol(BinOp)]`.
7. `Expr ::= Call(Expr, Expr)` with `[symbol(Call)]`.
8. `Value ::= num(Int, Int, Int)` with `[symbol(num)]`.
9. `Value ::= intValue(Int)` with `[symbol(intValue)]`.
10. `Result ::= noResult`.
11. `Result ::= Value` (subsort/injection).
12. `KItem ::= invoke(String, Value)` with `[symbol(invoke)]`.
13. `KItem ::= eval(Expr)` with `[symbol(eval)]`.
14. `KItem ::= subtractLeft(Expr)` with `[symbol(subtractLeft)]`.
15. `KItem ::= subtractRight(Value)` with `[symbol(subtractRight)]`.
16. `KItem ::= applyInt` with `[symbol(applyInt)]`.
17. `KItem ::= finishReturn` with `[symbol(finishReturn)]`.

Local productions in `VERIFICATION`:

18. `Bool ::= validPositive(Value)` with `[function, total]`.
19. `Bool ::= validFraction(Value)` with `[function, total]`.

There are no local `[functional]`, `[opaque]`, `[simplification]`,
`[concrete]`, priority, or `owise` declarations/rules.

The configuration is:

- `<k>`: the parsed `Program`, followed by a harness invocation of
  `"truncate_number"` with `num($IPART,$FRAC,$SCALE)`.
- `<env>`: initially `.Map`.
- `<result>`: initially `noResult`.
- `<python>`: the top-level wrapper.

Every cell is used. No heap, allocation, I/O, exception, or call-stack cell is
needed by this one-expression, single-call program on the claimed domain.

## Construct-to-rule coverage for `solution.mpy`

The submitted tree is
`Module(FuncDef("truncate_number", Params("number"),
Return(BinOp("-", Name("number"), Call(Name("int"), Name("number"))))))`.

| Used construct | Declaration | Executing rule(s) |
|---|---|---|
| `Module`, `FuncDef`, `Params` | syntax items 1, 2, 4 | S1 |
| `Return` | item 3 | S2 and S9 |
| outer `BinOp("-")` | item 6 | S4, S5, S6 |
| both `Name("number")` nodes | item 5 | S3 |
| `Call(Name("int"), ...)` | items 5 and 7 | S7 and S8 |
| input/result `num` | item 8 | S6 and S8; also carried as data |
| intermediate `intValue` | item 9 | S6 and S8 |

No translated construct is unmodeled.

## Operational rules in `SEMANTIC`

S1. Function entry, lines 44–45:
`Module(FuncDef(F,Params(P),BODY)) ~> invoke(F,V) => BODY`, with empty
environment becoming `P |-> V`.

- Equality of the two occurrences of `F` pins the requested function name to
  the defined function name.
- The exact `.Map` match prevents accidental reuse of an existing local
  environment.
- On the submitted one-function, one-parameter program this is the intended
  call entry and has no overlap with another local rule.

S2. Return setup, line 47:
`Return(E) => eval(E) ~> finishReturn`.

- Evaluates the expression before committing the result.
- It frames a suffix, so it is not a reusable semantics for Python's abrupt
  `return` in arbitrary statement continuations. The supported `Stmt` grammar
  has no sequencing construct, and the real function body is the sole
  `Return`, so no such continuation is reachable from an entry claim.

S3. Name lookup, lines 49–50:
`eval(Name(X)) => V` when `<env>` contains `X |-> V`.

- Reads but does not change the environment.
- Both real lookups select the `number` binding introduced by S1.

S4. Subtraction start, lines 52–53:
`eval(BinOp("-",LEFT,RIGHT)) => eval(LEFT) ~> subtractLeft(RIGHT)`.

- Matches only subtraction and starts Python's left-to-right operand order.

S5. After-left transition, lines 54–55:
`V ~> subtractLeft(RIGHT) => eval(RIGHT) ~> subtractRight(V)`.

- Saves the evaluated left value while the right expression evaluates.

S6. Numeric subtraction, lines 56–57:
`intValue(J) ~> subtractRight(num(I,F,S)) => num(I-J,F,S)`.

- The continuation stores the left operand, so this computes
  `(I + F/S) - J`, in the correct operand order.
- The actual right operand is `intValue(I)` from S8, yielding
  `num(0,F,S)`.

S7. Built-in `int` call setup, line 59:
`eval(Call(Name("int"),ARG)) => eval(ARG) ~> applyInt`.

- Matches exactly the syntactic built-in used by the submitted program. It
  models `int` as a trusted primitive, rather than as program-defined code.

S8. Positive canonical `int` primitive, line 61:
`num(I,_F,_S) ~> applyInt => intValue(I)`.

- This is mathematically correct on every entry state satisfying
  `S>0`, `0<=F<S`, and `I>=0`: the represented number is in `[I,I+1)`.
- The rule itself is unguarded and is therefore not a reusable definition for
  all syntactically constructible `num` terms. For example, if
  `num(0,3,2)` is informally read as 1.5, this rule returns 0. That term fails
  the entry precondition (`F<S`) and is not the canonical encoding of an
  intended input. This is an over-broad semantics limitation, not an
  unsoundness witness on the claimed intended domain.

S9. Return completion, lines 63–64:
`V ~> finishReturn => .K`, changing `noResult` to `V`.

- Consumes the return marker and writes exactly the computed value.
- It cannot silently overwrite an earlier result because it requires
  `noResult`.

The operational rules have disjoint leading constructors/continuations on the
real path. There are no priorities and no local overlapping alternatives.

## Verification functions and equations

V1. `validPositive(num(I,F,S))`, lines 10–15, expands to
`S>0 ∧ I>=0 ∧ F>=0 ∧ F<S ∧ (I>0 ∨ F>0)`.

V2. `validPositive(intValue(_))`, line 16, is `false`.

V3. `validFraction(num(I,F,S))`, lines 19–20, expands to
`I=0 ∧ S>0 ∧ F>=0 ∧ F<S`.

V4. `validFraction(intValue(_))`, line 21, is `false`.

For each `[function,total]` symbol, V1/V2 or V3/V4 cover the two and only two
constructors of `Value`. The constructor patterns are disjoint, the equations
terminate immediately, and there are no guard gaps or overlaps.

## Claims

C1, `spec.k` lines 9–20, is the universal entry claim. Its precondition is
exactly V1. It executes the exact submitted constructor tree plus the harness
invocation and requires termination with `num(0,F,S)`. Its `validFraction`
ensure is redundant but true under the precondition.

C2, lines 23–32, is the ground prompt example for `num(3,5,10)` and requires
the exact result `num(0,5,10)`.

Neither claim contains a free result oracle, an existential returned value, a
one-way implication, a loop circularity, an auxiliary helper claim, or a
proof-local operational rewrite.

## Static conclusion

The task-bearing computation is performed by S1–S9. No local rule directly
rewrites the whole program to the requested answer, and the body-sensitivity
experiment shows that replacing the body with `return number` changes the K
result from `num(0,1,2)` to `num(3,1,2)` on 3.5.

The proof's main limitation is the bridge from CPython binary64 execution to
the exact-rational `num(I,F,S)` model. That representation and the behavior of
the `int` and subtraction primitives on canonical positive decompositions are
not proved against CPython inside K. They are mathematically justified and
empirically supported by the preserved differential and concrete tests, but
finite tests are not a universal connection theorem.
