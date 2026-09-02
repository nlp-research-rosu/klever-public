requires "verification.k"

module PROD-SIGNS-VACUITY-AUDIT
  imports PROD-SIGNS-VERIFICATION

  // False for the satisfying witness [1]: the program/formal summary is 1,
  // while this destination requires 2.
  claim [false-off-by-one]:
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
