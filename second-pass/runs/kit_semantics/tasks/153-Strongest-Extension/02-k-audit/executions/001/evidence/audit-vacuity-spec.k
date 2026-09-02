requires "/tmp/audit-work/rebuild/verification.k"

module AUDIT-VACUITY-SPEC
  imports TARGET-VERIFICATION

  // Fresh false-result mutation. The satisfying input is class_name="" and
  // extensions=[]; the submitted body returns ".", never "X".
  claim [false-entry-result]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "Strongest_Extension",
            Params("class_name", "extensions"),
            STRONGEST-BODY
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
      => str(iCons(88, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "Strongest_Extension" |->
             closureVal(
               "class_name", "extensions", .ParamNames,
               STRONGEST-BODY,
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
