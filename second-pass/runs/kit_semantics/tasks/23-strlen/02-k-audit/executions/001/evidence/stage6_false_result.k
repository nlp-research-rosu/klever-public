requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Fresh reviewer-authored false obligation. The exact submitted body is
  // executed on "abc", but its required result is changed from 3 to 4.
  claim [abc-off-by-one]:
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
      ~> Call(
           Name("strlen"),
           (str(iCons(97, iCons(98, iCons(99, .IntSeq)))), .Exprs)
         )
      => 4
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
