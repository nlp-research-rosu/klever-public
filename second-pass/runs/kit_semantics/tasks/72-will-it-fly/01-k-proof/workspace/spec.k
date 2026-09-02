requires "verification.k"

module SPEC
  imports VERIFICATION

  // Balanced integral/float branches plus the unrestricted short-circuit
  // branch cover every terminating behavior modeled by the reference.
  claim [will-it-fly-balanced]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(VS:ValSeq), W:Int, .Exprs))
      => sumInts(0, VS) <=Int W
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
      0 |-> list(reverseSlice(VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      allIntegral(VS)
      andBool
      notBool hasFloat(VS)
      andBool
      (VS ==K reverseSlice(VS))

  claim [will-it-fly-unbalanced]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(VS:ValSeq), W:Int, .Exprs))
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
      0 |-> list(reverseSlice(VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      allIntegral(VS)
      andBool
      notBool hasFloat(VS)
      andBool
      notBool
        (VS ==K reverseSlice(VS))

  claim [will-it-fly-float-balanced]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(VS:ValSeq), W:Float, .Exprs))
      => notBool gtF(sumToFloat(0, VS), W)
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
      0 |-> list(reverseSlice(VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      allNumeric(VS)
      andBool
      hasFloat(VS)
      andBool
      notBool allIntegral(VS)
      andBool
      (VS ==K reverseSlice(VS))

  claim [will-it-fly-any-unbalanced]:
    <k>
      Call(
        Name("will_it_fly"),
        (list(VS:ValSeq), W:Val, .Exprs))
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
      0 |-> list(reverseSlice(VS))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      notBool (VS ==K reverseSlice(VS))
endmodule
