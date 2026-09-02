requires "verification.k"

module COMPARE-MUTATION-SPEC
  imports COMPARE-VERIFICATION

  // This is intentionally false: the addition mutant returns [3], not [1].
  claim
    <k>
      FuncDef(
        "compare",
        Params("game", "guess"),
        Expr(Str("Return the absolute error for each corresponding score and guess."))
        Assign(Name("result"), ListExpr(.Exprs))
        For(
          TupleExpr(Name("score"), Name("prediction")),
          Call(Name("zip"), Name("game"), Name("guess")),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              Call(
                Name("abs"),
                BinOp("+", Name("score"), Name("prediction"))))))
        Return(Name("result")))
      ~> Call(
           Name("compare"),
           list(vCons(1, .ValSeq)),
           list(vCons(2, .ValSeq)))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 Expr(Str("Return the absolute error for each corresponding score and guess."))
                 Assign(Name("result"), ListExpr(.Exprs))
                 For(
                   TupleExpr(Name("score"), Name("prediction")),
                   Call(Name("zip"), Name("game"), Name("guess")),
                   Expr(
                     Call(
                       Attribute(Name("result"), "append"),
                       Call(
                         Name("abs"),
                         BinOp("+", Name("score"), Name("prediction"))))))
                 Return(Name("result")),
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(1, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
