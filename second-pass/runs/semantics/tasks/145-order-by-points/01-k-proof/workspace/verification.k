requires "reference-semantics/semantics.k"

module ORDER-BY-POINTS-VERIFICATION
  imports MPY

  syntax Stmts ::= "digitSumBody" [function, total]
  rule digitSumBody =>
    Assign(Name("negative"), Compare(Name("n"), CmpOp("<", Int(0))))
    Assign(Name("n"), Call(Name("abs"), (Name("n"), .Exprs)))
    Assign(Name("total"), Int(0))
    Assign(Name("most_significant"), Int(0))
    While(Name("n"),
      Assign(Name("most_significant"), BinOp("%", Name("n"), Int(10)))
      AugAssign(Name("total"), "+", Name("most_significant"))
      AugAssign(Name("n"), "//", Int(10))
      .Stmts)
    If(Name("negative"),
      AugAssign(
        Name("total"),
        "-",
        BinOp("*", Int(2), Name("most_significant")))
      .Stmts,
      .Stmts)
    Return(Name("total"))
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
