requires "verification.k"

module BY-LENGTH-SPEC-REVIEWER-VACUITY-GROUND
  imports BY-LENGTH-VERIFICATION

  // Deliberately false result for the satisfying input []:
  // the implementation returns [], not ["One"].
  claim
    <k>
      #applyK(
        toCall(byLengthClosure),
        (list(intVals(.IntSeq)), .Vals))
      ~> #observeList
    =>
      list(vCons(str(strToCodes("One")), .ValSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?FINALHEAP:Map </heap>
    <heapLoc> 0 => ?FINALHEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
