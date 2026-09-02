requires "identity-verification.k"

module ORDER-BY-POINTS-PROGRAM-IDENTITY
  imports ORDER-BY-POINTS-IDENTITY-VERIFICATION

  // RHS is the trusted-translator output in solution.mpy, written with explicit
  // list units so the parser-normalized constructor identity is checked by K.
  claim
    <k>
      #identityModule(solutionModule)
      =>
      #identityModule(Module(
      FuncDef("digit_sum", Params(("n", .ParamNames)),
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
        .Stmts)
      FuncDef("order_by_points", Params(("nums", .ParamNames)),
        Return(
          Call(
            Name("sorted"),
            (Name("nums"),
             KwArg("key", Name("digit_sum")),
             .Exprs)))
        .Stmts)
      .Stmts))
    </k>
    <env> 0 </env>
    <scopes> initialScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
