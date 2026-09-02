requires "verification.k"

module AUDIT-GROUND-WITNESSES
  imports VERIFICATION

  claim [singleton]:
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
    <heap> .Map => 0 |-> list(vCons(3, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [prompt-second]:
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
           list(vCons(0, vCons(5, vCons(0, vCons(0, vCons(0, vCons(4, .ValSeq))))))),
           list(vCons(4, vCons(1, vCons(1, vCons(0, vCons(0, vCons(-2, .ValSeq))))))))
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
    <heap>
      .Map
      =>
      0 |-> list(vCons(4, vCons(4, vCons(1, vCons(0, vCons(0, vCons(6, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
