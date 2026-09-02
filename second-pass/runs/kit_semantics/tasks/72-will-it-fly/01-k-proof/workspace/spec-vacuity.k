requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for q = [3], w = 5.
  claim [false-result]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(vCons(3, .ValSeq)), 5, .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "will_it_fly" |-> willItFlyClosure(),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(reverseSlice(vCons(3, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      allIntegral(vCons(3, .ValSeq))
      andBool
      notBool hasFloat(vCons(3, .ValSeq))
      andBool
      (reverseSlice(vCons(3, .ValSeq)) ==K vCons(3, .ValSeq))
      andBool
      (sumInts(0, vCons(3, .ValSeq)) ==Int 3)
endmodule
