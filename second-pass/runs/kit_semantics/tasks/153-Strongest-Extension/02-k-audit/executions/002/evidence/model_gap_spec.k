requires "reviewer-pinning.k"

module MODEL-GAP-SPEC
  imports REVIEWER-PINNING

  // Fixed ASCII model: "" and "Ω" both score zero, so the first extension wins.
  claim [model-gap]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "Strongest_Extension",
            Params("class_name", "extensions"),
            REVIEWED-PROGRAM-BODY
          )
          .Stmts
        )
      )
      ~> Call(
           Name("Strongest_Extension"),
           str(iCons(71, iCons(97, iCons(112, .IntSeq)))),
           list(
             vCons(
               str(.IntSeq),
               vCons(str(iCons(937, .IntSeq)), .ValSeq)
             )
           ),
           .Exprs
         )
      => str(iCons(71, iCons(97, iCons(112, iCons(46, .IntSeq)))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "Strongest_Extension" |->
             closureVal(
               "class_name", "extensions", .ParamNames,
               REVIEWED-PROGRAM-BODY,
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
