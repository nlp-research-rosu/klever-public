requires "/audit-output/evidence/fixed-wrapper.k"

module HOW-MANY-TIMES-FIXED-WRONG-BINDING-SPEC
  imports HOW-MANY-TIMES-FIXED-AUDIT

  claim
    <k>
      #applyK(
        toCall(
          closureVal(
            ("string", "substring"),
            howManyTimesBodyFixed,
            0)),
        (str(iCons(97, .IntSeq)),
         str(iCons(97, .IntSeq)),
         .Vals))
    =>
      1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("how_many_times" |-> 0, parent(-1))
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
