requires "verification.k"

module AUDIT-GROUND-SPEC
  imports VERIFICATION

  claim
    <k>
      Call(
        closureVal(("xs", .ParamNames), findZeroBody, 0),
        list(vCons(1, vCons(2, .ValSeq))))
      =>
      bisectLow(
        vCons(1, vCons(2, .ValSeq)),
        bracketLow(vCons(1, vCons(2, .ValSeq))),
        bracketHigh(vCons(1, vCons(2, .ValSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validPolynomial(vCons(1, vCons(2, .ValSeq)))

  claim
    <k>
      Call(
        closureVal(("xs", .ParamNames), findZeroBody, 0),
        list(vCons(1, vCons(2, .ValSeq))))
      ~> #checkApprox(vCons(1, vCons(2, .ValSeq)))
      =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validPolynomial(vCons(1, vCons(2, .ValSeq)))
endmodule
