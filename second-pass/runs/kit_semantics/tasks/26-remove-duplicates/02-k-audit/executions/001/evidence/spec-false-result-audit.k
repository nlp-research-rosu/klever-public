requires "verification.k"

module SPEC-FALSE-RESULT-AUDIT
  imports VERIFICATION

  // Fresh audit mutation: the real singleton result [1] is replaced by [99].
  claim [false-singleton-value]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "remove_duplicates",
            Params("numbers"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("number"), Int(0))
            For(
              Name("number"),
              Name("numbers"),
              If(
                Compare(
                  Call(
                    Attribute(Name("numbers"), "count"),
                    (Name("number"), .Exprs)),
                  CmpOp("==", Int(1))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    (Name("number"), .Exprs))),
                .Stmts))
            Return(Name("result")))))
      ~> Call(
           Name("remove_duplicates"),
           (list(vCons(1, .ValSeq)), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "remove_duplicates" |->
                    closureVal(
                      ("numbers", .ParamNames),
                      Assign(Name("result"), ListExpr(.Exprs))
                      Assign(Name("number"), Int(0))
                      For(
                        Name("number"),
                        Name("numbers"),
                        If(
                          Compare(
                            Call(
                              Attribute(Name("numbers"), "count"),
                              (Name("number"), .Exprs)),
                            CmpOp("==", Int(1))),
                          Expr(
                            Call(
                              Attribute(Name("result"), "append"),
                              (Name("number"), .Exprs))),
                          .Stmts))
                      Return(Name("result")),
                      0),
                  parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(99, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
