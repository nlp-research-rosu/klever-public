requires "/tmp/audit-work/rebuild/reference-semantics/semantics.k"

module AUDIT-MODULE-LOAD-CONNECTION
  imports MPY

  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "eat",
            Params("number", "need", "remaining"),
            If(
              Compare(Name("need"), CmpOp("<=", Name("remaining"))),
              Return(
                ListExpr(
                  BinOp("+", Name("number"), Name("need")),
                  BinOp("-", Name("remaining"), Name("need"))))
              .Stmts,
              .Stmts)
            Return(
              ListExpr(
                BinOp("+", Name("number"), Name("remaining")),
                Int(0)))
            .Stmts)
          .Stmts))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "eat" |->
          closureVal(
            ("number", "need", "remaining"),
            If(
              Compare(Name("need"), CmpOp("<=", Name("remaining"))),
              Return(
                ListExpr(
                  BinOp("+", Name("number"), Name("need")),
                  BinOp("-", Name("remaining"), Name("need"))))
              .Stmts,
              .Stmts)
            Return(
              ListExpr(
                BinOp("+", Name("number"), Name("remaining")),
                Int(0)))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
