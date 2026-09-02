requires "verification.k"

module REVIEWER-VACUITY
  imports TARGET-VERIFICATION

  // Satisfiable input: "B" has score +1 and beats "a" with score -1.
  // Deliberately false postcondition chooses the losing first extension.
  claim [wrong-winner]:
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
           str(iCons(67, .IntSeq)),
           list(
             vCons(
               str(iCons(97, .IntSeq)),
               vCons(str(iCons(66, .IntSeq)), .ValSeq)
             )
           ),
           .Exprs
         )
      => str(iCons(67, iCons(46, iCons(97, .IntSeq))))
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
