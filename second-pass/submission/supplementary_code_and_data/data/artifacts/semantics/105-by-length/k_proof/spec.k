requires "verification.k"

module BY-LENGTH-SPEC
  imports BY-LENGTH-VERIFICATION

  // For every finite list of integers, the implementation returns the
  // English names of exactly the 1..9 values, sorted in descending order.
  // MPY-SORT defines reverse=True as revVS(sortVS(...)).
  claim
    <k>
      #applyK(
        toCall(byLengthClosure),
        (list(intVals(IS:IntSeq)), .Vals))
      ~> #observeList
    =>
      list(
        tableNames(
          revVS(
            sortVS(
              filterDigits(
                intVals(IS))))))
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
