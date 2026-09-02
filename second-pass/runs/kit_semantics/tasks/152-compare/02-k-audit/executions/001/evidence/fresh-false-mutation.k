requires "verification.k"

module AUDIT-FRESH-FALSE-MUTATION
  imports VERIFICATION

  // False for the satisfying input game=[5], guess=[2]:
  // the implementation and canonical function both return [3], not [4].
  claim [singleton-wrong-result]:
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
                  Call(
                    Name("abs"),
                    BinOp("-", Name("score"), Name("predicted")))))
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
    <heap> .Map => 0 |-> list(vCons(4, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
