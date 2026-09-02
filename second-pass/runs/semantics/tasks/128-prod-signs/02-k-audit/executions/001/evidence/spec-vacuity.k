requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports PROD-SIGNS-VERIFICATION

  // Deliberately false: for every nonempty integer input, demand one more
  // than the exact result constrained by the original entry claim.
  claim [prod-signs-nonempty-off-by-one]:
    <k>
      Call(prodSignsFunction, list(vCons(I:Int, VS:ValSeq)))
      =>
      (magnitudeSum(vCons(I, VS)) *Int signProduct(vCons(I, VS))) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
