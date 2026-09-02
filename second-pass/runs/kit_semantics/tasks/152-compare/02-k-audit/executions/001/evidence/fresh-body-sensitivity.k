requires "verification.k"

module AUDIT-FRESH-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed program term is changed to append abs(score-predicted)+1.
  // For [5],[2] that body returns [4], so the original body's result [3]
  // must no longer be provable.
  claim [mutated-body-original-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "compare",
            Params("game", "guess"),
            Assign(Name("result"), ListExpr(.Exprs))
            For(
              TupleExpr(Name("score"), Name("predicted")),
              Call(Name("zip"), Name("game"), Name("guess")),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  BinOp(
                    "+",
                    Call(
                      Name("abs"),
                      BinOp("-", Name("score"), Name("predicted"))),
                    Int(1))))
              .Stmts)
            Return(Name("result"))
            .Stmts)
          .Stmts))
      ~> Call(
           Name("compare"),
           list(vCons(5, .ValSeq)),
           list(vCons(2, .ValSeq)))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(3, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
