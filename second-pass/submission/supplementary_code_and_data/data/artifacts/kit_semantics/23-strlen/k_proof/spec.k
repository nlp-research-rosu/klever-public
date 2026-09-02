requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [strlen]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "strlen",
            Params("string"),
            Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts
          ) .Stmts
        )
      )
      ~> Call(Name("strlen"), (str(CS:IntSeq), .Exprs))
      => isLen(CS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "strlen" |-> closureVal(
             "string" , .ParamNames,
             Return(Call(Name("len"), (Name("string"), .Exprs))) .Stmts,
             0
           ),
        parent(-1)
      )
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
