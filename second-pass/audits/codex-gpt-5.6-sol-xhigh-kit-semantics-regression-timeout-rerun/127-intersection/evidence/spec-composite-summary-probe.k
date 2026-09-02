requires "/tmp/audit-work/scratch/spec.k"

module COMPOSITE-SUMMARY-PROBE
  imports SPEC

  claim [composite-nine-as-prime]:
    <k>
      Call(
        Name("intersection"),
        tuple(vCons(0, vCons(9, .ValSeq))),
        tuple(vCons(0, vCons(9, .ValSeq))))
      =>
      str(iCons(89, iCons(69, iCons(83, .IntSeq))))
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
    requires scanPrime(9, 2, true)
endmodule
