# Local K rule and declaration inventory

This inventory covers every local declaration and rule in the submitted
`semantic.k` and `verification.k`. Imported K built-ins used by those local
rules are listed separately; the whole K prelude is not candidate-authored.

## `semantic.k`: syntax and state

- `Pgm`: `Module(Stmts)`.
- `Stmts`: separator-free `List{Stmt,""}`.
- `Stmt`: `FuncDef(String,Params,Stmts)`, `If(Expr,Stmts,Stmts)`,
  `Return(Expr)`.
- `Params`: one `String`.
- `Expr`: `Name`, `Str`, `Int`, `BinOp`, `Call`, `Subscript`, `Slice`,
  `Compare`.
- `CmpOp`: one operator string and one right expression.
- `Bound`: the `Expr` subsort or `NoBound`.
- `Result`: `noResult` or the `String` subsort.
- `Val`: the `Int`, `String`, and `Bool` subsorts or `PyBool(Bool)`.
- Control `KItem`s: `start`, `eval`, `exec`, `binLeft`, `binRight`,
  `cmpLeft`, `cmpRight`, `subBase`, `applyFun`, `choose`, `endCall`,
  `finish`.
- `appendStmts(Stmts,Stmts)` is the only local `[function,total]` symbol.
- Configuration: `<k>` plus fixed single-function metadata
  (`<funName>`, `<parameter>`, `<body>`), `<env>` map, `<stack>` list, and
  `<result>`.

There are no local priorities, `owise` rules, `[functional]` declarations,
opaque declarations, or simplification rules in `semantic.k`.

## `semantic.k`: all 28 rules

1. `appendStmts(.Stmts,SS) => SS`: truthful empty-list equation.
2. `appendStmts(S REST,SS) => S appendStmts(REST,SS)`: truthful structural
   recursion; disjoint from rule 1 and descending.
3. Module/start: captures the only function's name, parameter, and body and
   calls it on the configured input before `finish`.
4. `eval(Str(S)) => S`.
5. `eval(Int(I)) => I`.
6. `eval(Name(X)) => V` when `X |-> V` is in `<env>`.
7. `eval(BinOp(OP,A,B))`: starts the left operand.
8. `V ~> binLeft(OP,B)`: starts the right operand after the left is a value.
9. Integer `+` dispatch.
10. String `+` dispatch.
11. Integer `-` dispatch.
12. Integer `%` dispatch to `modInt`.
13. `eval(Compare(A,CmpOp(OP,B)))`: starts the left operand.
14. `V ~> cmpLeft(OP,B)`: starts the right operand.
15. String `==` dispatch to `PyBool(S1 ==String S2)`.
16. `eval(Subscript(A,INDEX))`: evaluates the base first.
17. String integer subscript maps to `substrString(S,I,I+1)`.
18. String `[I:]` maps to
    `substrString(S,I,lengthString(S))`.
19. `eval(Call(Name(F),ARG))`: evaluates the sole argument first.
20. Integer argument to `chr` maps to `chrChar`.
21. String argument to `ord` maps to `ordChar`.
22. The stored one-argument user function call overwrites its parameter
    binding, saves the complete old environment on `<stack>`, and executes the
    stored body.
23. `exec(If(...) REST)`: evaluates the condition and saves both branches and
    the suffix.
24. `PyBool(true)`: executes then-branch followed by suffix.
25. `PyBool(false)`: executes else-branch followed by suffix.
26. `exec(Return(E) _REST)`: discards the remaining statements, evaluates
    `E`, then begins call return.
27. `V ~> endCall`: restores the saved environment and pops one stack entry.
28. `S ~> finish`: clears `<k>` and writes the final result.

Rules 4-16 and 19-28 faithfully cover the submitted source's used shapes and
left-to-right control order. Rules 17-18 are not a sound Python-string bridge
over the claim's whole `String` domain. The concrete satisfying witness
`S = "🙂"` executes normally in Python but returns `"t"`; both rebuilt K
backends return `"roil"`. Thus the `substrString`/`lengthString` bridge advances
through the UTF-8 representation in this execution rather than Python's one
Unicode-code-point slice. See `concrete-semantics.log` and
`unicode-backend-witness.log`.

Rules 17, 18, 20, and 21 also omit Python's index/range/arity exception
conditions. Those broader bad contexts are unreachable in this exact source
for nonempty inputs because the guard precedes index 0, the slice begins at 1,
and the computed `chr` value is 97 through 122. They are an over-broad semantics
gap, but no separate false conclusion from those omitted guards is alleged on
the submitted program's reachable input domain.

Rule 22 can overlap rule 21 if the configured user function itself is named
`ord`; the submitted module fixes it to `encrypt`, so that overlap is
unreachable here. The single-function metadata need not be stacked because
every reachable user call is recursion into that same stored function.

## `verification.k`: every extension

1. `solutionBody : Stmts` is `[function,total]`; its sole equation expands to
   the exact `If` followed by `Return` tree regenerated in `solution.mpy`.
   It is a transparent definitional abbreviation, not an execution shortcut.
2. `rotate4(String) : String` is `[function]` (not `[total]`).
3. `rotate4("") => "" [simplification]` is the base equation.
4. The guarded nonempty `rotate4` equation emits the transformed first
   K-string unit and recurses on `substrString(S,1,lengthString(S))`;
   it is `[simplification]`.

The rotate equations' guards are disjoint and cover every concrete K string.
They are transparent and structurally descending under the K string hooks.
They do not replace any operational term: `rotate4` appears only in claims.
However, they reuse the same hooked `lengthString`, `substrString`, `ordChar`,
and `chrChar` primitives as the operational semantics. Consequently they
characterize the submitted K model, but provide no independent theorem that
the model equals CPython string behavior. The `"🙂"` witness falsifies that
bridge.

There are no proof-local priority rules, ordinary operational bridges, fresh
opaque symbols, `[functional]` declarations, or unguarded task-answer axioms.

## Claims and imported trust boundary

- `encrypt-call-correct` is the recursive contextual execution summary.
- `program-correct` is the end-to-end entry claim and depends on that summary.
- Imported integer hooks used: `+Int`, `-Int`, `modInt`.
- Imported string hooks used: `+String`, `==String`, `lengthString`,
  `substrString`, `ordChar`, `chrChar`.
- Imported structural primitives: map lookup/update, `ListItem`, list
  constructors, and K sequencing/equality.

These imports are acceptable primitives for a K theorem about the defined
machine. Their interpretation as CPython behavior is a separate bridge and is
materially false over the formal all-`String` domain.
