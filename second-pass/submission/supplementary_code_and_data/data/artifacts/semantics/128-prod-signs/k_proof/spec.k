requires "verification.k"

module PROD-SIGNS-SPEC
  imports PROD-SIGNS-VERIFICATION

  claim [prod-signs-empty]:
    <k>
      Call(prodSignsFunction, list(.ValSeq))
      =>
      noneV
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

  claim [prod-signs-nonempty]:
    <k>
      Call(prodSignsFunction, list(vCons(I:Int, VS:ValSeq)))
      =>
      magnitudeSum(vCons(I, VS)) *Int signProduct(vCons(I, VS))
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
