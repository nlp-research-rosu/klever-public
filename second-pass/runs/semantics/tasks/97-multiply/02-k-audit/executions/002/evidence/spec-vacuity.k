requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-off-by-one]:
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
