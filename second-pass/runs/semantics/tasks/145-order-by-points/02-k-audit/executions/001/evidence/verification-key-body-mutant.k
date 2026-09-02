requires "reference-semantics/semantics.k"

module ORDER-BY-POINTS-VERIFICATION
  imports MPY

  syntax Stmts ::= "digitSumBody" [function, total]
  rule digitSumBody =>
    Return(Int(0))
    .Stmts

  syntax Stmts ::= "orderByPointsBody" [function, total]
  rule orderByPointsBody =>
    Return(
      Call(
        Name("sorted"),
        (Name("nums"),
         KwArg("key", Name("digit_sum")),
         .Exprs)))
    .Stmts

  syntax Val ::= "digitSumClosure" [function, total]
               | "orderByPointsClosure" [function, total]
  rule digitSumClosure =>
    closureVal(("n", .ParamNames), digitSumBody, 0)
  rule orderByPointsClosure =>
    closureVal(("nums", .ParamNames), orderByPointsBody, 0)

  syntax Module ::= "solutionModule" [function, total]
  rule solutionModule =>
    Module(
      FuncDef("digit_sum", Params(("n", .ParamNames)), digitSumBody)
      FuncDef(
        "order_by_points",
        Params(("nums", .ParamNames)),
        orderByPointsBody)
      .Stmts)

  syntax Map ::= "initialScopes" [function, total]
               | "loadedScopes" [function, total]
  rule initialScopes =>
    (0 |-> scope(.Map, parent(-1)))
    (-1 |-> builtinsScope)
  rule loadedScopes =>
    (0 |-> scope(
      .Map
        [ "digit_sum" <- digitSumClosure ]
        [ "order_by_points" <- orderByPointsClosure ],
      parent(-1)))
    (-1 |-> builtinsScope)

  syntax KItem ::= "#runDigitSum" "(" Int ")"
                 | "#runOrderByPoints" "(" Val ")"
  rule <k> #runDigitSum(N:Int)
        => #loadAll(solutionModule)
        ~> Call(Name("digit_sum"), (N, .Exprs))
        ... </k>
  rule <k> #runOrderByPoints(V:Val)
        => #loadAll(solutionModule)
        ~> Call(Name("order_by_points"), (V, .Exprs))
        ... </k>
endmodule
