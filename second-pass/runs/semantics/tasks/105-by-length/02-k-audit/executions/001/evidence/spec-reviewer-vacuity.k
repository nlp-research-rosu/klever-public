requires "verification.k"

module BY-LENGTH-SPEC-REVIEWER-VACUITY
  imports BY-LENGTH-VERIFICATION

  // Deliberately false mutation: prepend "One" to every result.
  // IS = .IntSeq satisfies the entry precondition and the real result is [].
  claim
    <k>
      #applyK(
        toCall(byLengthClosure),
        (list(intVals(IS:IntSeq)), .Vals))
      ~> #observeList
    =>
      list(
        vCons(
          str(strToCodes("One")),
          tableNames(
            revVS(
              sortVS(
                filterDigits(
                  intVals(IS)))))))
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
