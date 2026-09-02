requires "verification.k"

module AUDIT-BODY-MUTATION
  imports VERIFICATION

  // Reviewer-authored sensitivity probe: the executed body is changed from
  // `return len(string)` to `return 0`, while the one-character obligation
  // remains result 1.
  claim [changed-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "strlen",
            Params("string"),
            Return(Int(0)) .Stmts
          ) .Stmts
        )
      )
      ~> Call(Name("strlen"), (str(iCons(97, .IntSeq)), .Exprs))
      => 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "strlen" |-> closureVal(
             "string" , .ParamNames,
             Return(Int(0)) .Stmts,
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
