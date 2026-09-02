# Exhaustive local K inventory and static soundness review

This inventory covers every source-level declaration in the candidate's
`semantic.k`, `verification.k`, and `spec.k`. There are no additional helper K
files. Imported `INT`, `STRING`, and `MAP` definitions are upstream K
primitives, not candidate-local rules.

## `MPY-SYNTAX` declarations

| Location | Declaration | Use and review |
|---|---|---|
| `semantic.k:7-11` | Empty sort declarations `Pgm`, `Params`, `Stmt`, `Expr`, `Value` | Sort scaffolding only. |
| `semantic.k:13` | `Pgm ::= Module(Stmt)` | Represents the translated module. The submitted term has exactly one function definition. |
| `semantic.k:14` | `Params ::= Params(String)` | Represents the submitted one-parameter signature. |
| `semantic.k:15` | `Stmt ::= FuncDef(String, Params, Stmt)` | Represents the sole top-level function binding. |
| `semantic.k:16` | `Stmt ::= Return(Expr) [strict]` | Represents the sole body statement. `[strict]` generates heating/cooling so its expression evaluates before the return rule; this is Python's required order here. |
| `semantic.k:17` | `Value ::= Int(Int)` | Wraps mathematical integers as modeled Python values. |
| `semantic.k:18` | `Expr ::= Value` | Value injection; no behavior is fabricated. |
| `semantic.k:19` | `Expr ::= Name(String)` | Represents every occurrence of `n`. |
| `semantic.k:20` | `Expr ::= BinOp(String, Expr, Expr) [seqstrict(2,3)]` | Represents all submitted `+`, `-`, `*`, and `//` expressions. The generated heating/cooling evaluates operand 2 before operand 3, agreeing with Python. |

Construct coverage is exact: the trusted regenerated `solution.mpy` uses
`Module`, `FuncDef`, `Params`, `Return`, `BinOp` with the four operator strings,
`Name`, and `Int`, and no other constructor. The concrete comparison executes
all of them.

## `MPY` declarations, configuration, and rules

| Location | Kind | Complete matched domain / state footprint | Static judgment |
|---|---|---|---|
| `semantic.k:29` | `KResult ::= Value` | Declares the only local value form, `Int`, to be evaluated. | Sound for the modeled subset. |
| `semantic.k:31` | Result syntax `noResult`, `result(Int)` | Observable return cell. | Pure syntax. |
| `semantic.k:33-39` | Configuration | `<k>` program, immutable `<input>` integer, `<env>` map, `<result>` return state. | Every cell is read or observed; no material submitted behavior needs a heap, I/O, exception, or call stack. |
| `semantic.k:43-45` | Operational entry rule | Matches an exact sole `Module(FuncDef(_FN, Params(X), BODY))`, reads `<input> N`, requires empty `<env>`, replaces `<k>` by `BODY`, and writes `X |-> N`; `<input>` and `<result>` are preserved. | This is an explicitly documented single-entry-function invocation convention. For the exact submitted one-argument, capture-free function it has the same binding and control effect as invoking that function with `N`. It does not skip the body. The ignored name broadens this tiny language's entry convention but cannot alter the fixed claim, whose name is exactly `get_max_triples`. |
| `semantic.k:47-48` | Name lookup | Matches `Name(X)` in any `<k>` continuation and an existing integer binding `X |-> I`; rewrites only the expression to `Int(I)`. | Sound map lookup. The submitted environment has exactly `"n" |-> N`. |
| `semantic.k:50` | `+` operational rule | Two evaluated `Int` operands; rewrites to mathematical `I +Int J`. | Exact Python integer addition. |
| `semantic.k:51` | `-` operational rule | Two evaluated `Int` operands; rewrites to mathematical `I -Int J`. | Exact Python integer subtraction. |
| `semantic.k:52` | `*` operational rule | Two evaluated `Int` operands; rewrites to mathematical `I *Int J`. | Exact Python integer multiplication. |
| `semantic.k:53-54` | `//` operational rule | Two evaluated `Int` operands with `J =/=Int 0`; rewrites to `I divInt J`. | Every submitted divisor is the positive constant 3 or 6. Every submitted dividend is nonnegative for `N >= 1`, so K integer division agrees with Python floor division on the full claim domain. The zero-divisor stuck behavior is unused. |
| `semantic.k:56-57` | Return rule | Matches only a fully evaluated `Return(Int(I))` with no continuation and `noResult`; consumes `<k>` and writes exact `result(I)`. | Exact for the submitted sole return. It neither discards a continuation nor invents a value. |

The four operator rules have disjoint literal operator guards. No local
operational rule overlaps another on the same term. The evaluation attributes
make every arithmetic rule applicable only after both operands are values.

The entry rule is intentionally not a general Python module semantics. For
example, the alternate term
`Module(FuncDef("other", Params("x"), Return(Int(7))))` is also treated as the
selected entry function rather than merely installed by module import. That is
a visible scope limitation of the declared entry convention, not a false
conclusion about the fixed submitted program or any positive integer input.
Similarly, unsupported syntax and division by zero stop rather than silently
produce a value. Neither occurs in `solution.mpy`.

## `VERIFICATION` declarations and rules

| Location | Extension class | Domain, coverage, and overlap | Static judgment |
|---|---|---|---|
| `verification.k:8-9` | Definitional summary `choose3(Int) [function,total]` | One unconditional, nonrecursive equation covers every `Int`; divisor 6 is nonzero; there is no overlap. | The equation names exactly `X*(X-1)*(X-2) div 6`. For every nonnegative class size reached under `N >= 1`, this is the ordinary binomial coefficient `C(X,3)`. It occurs only in the postcondition and never replaces program execution. |
| `verification.k:15-18` | Definitional summary `validTripleCount(Int) [function,total]` | One unconditional, nonrecursive equation covers every `Int`; its only callees are total; there is no overlap. | It names `choose3((N+1) div 3) + choose3(N-(N+1) div 3)`. It occurs only on the destination side and is fully fixed by equations, so it is neither opaque nor an oracle. |

For `N >= 1`, let `q = floor((N+1)/3)`. For an index `i`, the value
`i*i-i+1` is congruent to 0 modulo 3 exactly when `i` is 2 modulo 3 and is
otherwise congruent to 1. There are `q` zero-residue indices and `N-q`
one-residue indices in `1..N`. A three-element residue sum is divisible by 3
exactly when it contains zero or three one-residue terms. Therefore the
contract count is `C(q,3)+C(N-q,3)`, exactly `validTripleCount(N)`.

The K proof formally establishes equality with this fully defined summary. The
residue/counting derivation connecting that summary to the English contract is
ordinary but informal mathematics; differential evidence independently checks
the bridge on a finite sample.

## `SPEC` claim

`spec.k:6-41` contains the only claim. Its source is the exact constructor tree
of the trusted-regenerated `solution.mpy`; its initial cells are `<input> N`,
empty environment, and `noResult`; its final cells require consumed
computation, the exact binding `"n" |-> N`, and the exact result
`validTripleCount(N)`. Its precondition `N >=Int 1` is exactly the prompt's
positive-integer domain and is satisfiable (for example `N=5`). There are no
helper or loop claims.

## Attribute and opaque-symbol census

- Local `[function]` declarations: `choose3`, `validTripleCount`.
- Local `[total]` declarations: the same two, each covered by one unconditional
  terminating equation.
- Local strictness declarations: `Return` `[strict]`; `BinOp`
  `[seqstrict(2,3)]`.
- Local `[functional]`, `[simplification]`, `[concrete]`, `[anywhere]`,
  `[owise]`, macro, priority, and explicit heating/cooling declarations: none.
- Local opaque, fresh, or unconstrained result-bearing symbols: none.
- Operational bridges that replace program-defined arithmetic or body
  execution: none. The entry convention performs argument binding and then
  executes the exact body.
- Candidate-local derived lemmas: none.

No candidate-local rule supports a false conclusion for the submitted program
on a positive integer input.
