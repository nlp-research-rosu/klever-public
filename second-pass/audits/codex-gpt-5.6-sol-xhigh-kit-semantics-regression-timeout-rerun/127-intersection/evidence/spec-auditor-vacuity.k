requires "/tmp/audit-work/scratch/verification.k"

module AUDITOR-VACUITY
  imports VERIFICATION

  // False mutation of the prime-entry result for a satisfiable exact input.
  // The real program and canonical function both return "YES" for length 2.
  claim [prime-two-returns-no]:
    <k>
      Call(
        Name("intersection"),
        tuple(vCons(0, vCons(2, .ValSeq))),
        tuple(vCons(0, vCons(2, .ValSeq))))
      =>
      str(iCons(78, iCons(79, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "intersection" |-> intersectionClosure,
        parent(-1))
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
