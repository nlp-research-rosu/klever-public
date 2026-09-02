requires "/tmp/audit-work/candidate-src/verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the executed program returns unitDigitProduct(A,B),
  // not that value plus one. A=14, B=-15 is a satisfying witness (20 != 21).
  claim [multiply-false-plus-one]:
    <k> #runMultiply(A:Int, B:Int)
      => unitDigitProduct(A, B) +Int 1 </k>
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
