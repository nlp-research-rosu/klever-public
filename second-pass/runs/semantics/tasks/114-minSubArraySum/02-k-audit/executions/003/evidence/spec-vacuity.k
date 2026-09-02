requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation.  The precondition is satisfiable at H=5,
  // T=.IntSeq, where the actual result is 5 and the target requires 6.
  claim
    <k>
      #applyK(
        toCall(minSubArraySumClosure),
        (list(intVals(iCons(H:Int, T:IntSeq))), .Vals))
      => minSubArraySumSpec(iCons(H, T)) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
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
