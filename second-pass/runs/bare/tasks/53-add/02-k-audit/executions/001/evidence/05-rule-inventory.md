# Reviewer rule inventory

Scope: candidate-authored K source only. Candidate compiled output is excluded.
There are three K source files: `semantic.k`, `verification.k`, and `spec.k`;
there are no generated helper K files.

## `semantic.k`: local declarations

- Module `MPY-SYNTAX` imports trusted K builtin syntax modules `INT-SYNTAX`
  and `STRING-SYNTAX`.
- `Pgm` has one production: `Module(Stmt)`.
- `Stmt` has two productions: `FuncDef(String, Params, Stmt)` and
  `Return(Expr)`.
- `Params` has one production: `Params(String, String)`.
- `Expr` has three productions: `Int(Int)`, `Name(String)`, and
  `BinOp(String, Expr, Expr)`.
- Module `SEMANTIC` imports `MPY-SYNTAX` and trusted K builtin modules `INT`
  and `MAP`.
- `PyVal` has one constructor-like production: `pyInt(Int)`.
- `Function` has one constructor-like production:
  `function(String, String, Stmt)`.
- `KItem` has seven productions: `load(Pgm)`,
  `invoke(String, PyVal, PyVal)`, `bind(String, PyVal)`, `eval(Expr)`,
  `plusLeft(Expr)`, `plusRight(PyVal)`, and `finishReturn`.
- The configuration contains `<k>`, `<env>`, `<functions>`, and `<result>`
  below `<mpy>`. Its driver loads `$PGM` and then invokes `add` with the two
  integer configuration variables `$ARG1` and `$ARG2`. Both maps start empty
  and the integer result cell starts at zero.
- There are no local `[function]`, `[total]`, `[functional]`,
  `[simplification]`, `[priority]`, strictness, or opacity declarations.

## `semantic.k`: exhaustive ordinary-rule inventory

1. Line 41, module loading:
   `load(Module(S)) => S`. This exposes the sole translated statement before
   the pre-existing invocation continuation. It is faithful for the submitted
   one-function module.
2. Lines 43–44, function definition:
   consumes `FuncDef(F, Params(X,Y), BODY)` and stores exactly
   `F |-> function(X,Y,BODY)` into an initially empty function map. The actual
   module contains exactly one non-closure function, so no closure or
   multi-definition behavior is needed.
3. Lines 46–48, invocation:
   resolves `F` in the singleton function map, then schedules left-to-right
   parameter bindings followed by the stored body. This performs binding and
   body execution; it is not an opaque program summary.
4. Lines 50–51, binding:
   consumes `bind(X,V)` and updates the environment at key `X` using the
   trusted K `Map` update. With actual distinct formals `"x"` and `"y"`, the
   final map contains both bindings.
5. Line 53, return setup:
   rewrites `Return(E)` to `eval(E) ~> finishReturn`, so the expression must
   execute before the result is committed.
6. Line 55, integer literal evaluation:
   `eval(Int(I)) => pyInt(I)`. This is mathematically direct. It is not used by
   the submitted body but is independently smoke-tested with
   `literal-return.mpy`.
7. Lines 57–58, name evaluation:
   looks up the name's `PyVal` in `<env>`. Both actual names are bound before
   body evaluation.
8. Lines 60–61, binary-plus setup:
   only `BinOp("+", LEFT, RIGHT)` advances, scheduling evaluation of the left
   operand first. Other operator strings remain visibly unmodeled.
9. Lines 63–64, left-to-right sequencing:
   after the left operand becomes `pyInt(I)`, schedules right evaluation and
   carries `I` in `plusRight`.
10. Lines 66–67, integer addition:
    after the right operand becomes `pyInt(J)`, produces
    `pyInt(I +Int J)` using trusted K mathematical-integer addition.
11. Lines 69–70, return completion:
    consumes `pyInt(I) ~> finishReturn` and overwrites `<result>` with `I`.
    On the actual single-call, single-return path the continuation is empty.

## Other candidate-authored K source

- `verification.k` only requires `semantic.k` and imports `SEMANTIC`. It adds
  no syntax, function, totality declaration, opacity, priority, semantic rule,
  simplification, lemma, operational bridge, or oracle.
- `spec.k` contains one unlabeled entry reachability claim and no helper or loop
  claim. Its source term is the exact submitted translated program followed by
  invocation; its destination consumes `<k>`, records the two bindings and
  loaded function, and requires `<result>` to equal `X +Int Y`.

## Construct-to-rule coverage for `solution.mpy`

- `Module`: syntax plus rule 1.
- `FuncDef`: syntax plus rule 2.
- `Params("x","y")`: syntax; destructured by rules 2 and 3.
- `Return`: syntax plus rule 5 and completion rule 11.
- `BinOp("+", ...)`: syntax plus rules 8–10 and trusted `+Int`.
- Each `Name`: syntax plus rule 7 after rules 3–4 bind its value.
- String tokens: trusted `STRING-SYNTAX`; used structurally and as map keys.
- Entry invocation and argument integers: configuration driver plus rule 3;
  arguments are wrapped in `pyInt`.

## Static soundness conclusion

The used path is deterministic and fully covered. Rule fronts are disjoint on
that path, so there are no priority or overlap issues. There is no allocation,
heap, I/O, exception, recursion, loop, or helper summary. The only
result-bearing primitive is trusted K `+Int`; the program-defined addition is
not replaced by an oracle.

The model is deliberately a single-function, two-integer, one-call driver. Its
environment is not a general Python call stack, and `finishReturn` is not a
general abrupt-return/unwinding mechanism under arbitrary synthetic
continuations. Those contexts are outside the submitted program and the claim.
No false conclusion witness exists on the intended domain: for every input
pair, the reachable path has an empty post-call continuation and exactly the
two distinct local bindings. The limitation therefore narrows reuse of this
semantics but does not invalidate the theorem about this submitted program.
