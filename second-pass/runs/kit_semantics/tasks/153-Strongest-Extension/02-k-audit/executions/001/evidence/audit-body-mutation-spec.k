requires "/tmp/audit-work/rebuild/verification.k"

module AUDIT-BODY-MUTATION-SPEC
  imports TARGET-VERIFICATION

  // Changes the FuncDef term executed by the claim itself. The postcondition
  // remains the original empty-input result ".".
  claim [changed-executed-body]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "Strongest_Extension",
            Params("class_name", "extensions"),
            Return(Str("wrong"))
            .Stmts
          )
          .Stmts
        )
      )
      ~> Call(
           Name("Strongest_Extension"),
           str(.IntSeq),
           list(.ValSeq),
           .Exprs
         )
      => str(iCons(46, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "Strongest_Extension" |->
             closureVal(
               "class_name", "extensions", .ParamNames,
               Return(Str("wrong"))
               .Stmts,
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
