requires "verification.k"

module STAGE6-FALSE-RESULT
  imports VERIFICATION

  claim [example-one-wrong-thirteen]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "solution",
            Params("lst"),
            Assign(Name("result"), Int(0))
            Assign(Name("position"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"),
              Name("lst"),
              If(
                Compare(
                  BinOp("%", Name("position"), Int(2)),
                  CmpOp("==", Int(0))
                ),
                If(
                  Compare(
                    BinOp("%", Name("value"), Int(2)),
                    CmpOp("!=", Int(0))
                  ),
                  AugAssign(Name("result"), "+", Name("value")) .Stmts,
                  .Stmts
                ) .Stmts,
                .Stmts
              )
              AugAssign(Name("position"), "+", Int(1)) .Stmts
            )
            Return(Name("result")) .Stmts
          ) .Stmts
        )
      )
      ~> Call(
        Name("solution"),
        list(vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq)))))
      )
      => 13
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1))
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "solution" |-> closureVal(
            "lst" , .ParamNames,
            Assign(Name("result"), Int(0))
            Assign(Name("position"), Int(0))
            Assign(Name("value"), Int(0))
            For(
              Name("value"),
              Name("lst"),
              If(
                Compare(
                  BinOp("%", Name("position"), Int(2)),
                  CmpOp("==", Int(0))
                ),
                If(
                  Compare(
                    BinOp("%", Name("value"), Int(2)),
                    CmpOp("!=", Int(0))
                  ),
                  AugAssign(Name("result"), "+", Name("value")) .Stmts,
                  .Stmts
                ) .Stmts,
                .Stmts
              )
              AugAssign(Name("position"), "+", Int(1)) .Stmts
            )
            Return(Name("result")) .Stmts,
            0
          ),
          parent(-1)
        )
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
