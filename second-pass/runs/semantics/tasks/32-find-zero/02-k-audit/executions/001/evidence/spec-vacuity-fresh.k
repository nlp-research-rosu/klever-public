requires "verification.k"

module AUDIT-SPEC-VACUITY-FRESH
  imports VERIFICATION

  // Deliberately false: execution produces bisectLow(...), while this target
  // demands the distinct bisectHigh(...) constructor.
  claim
    <k>
      Call(
        closureVal(("xs", .ParamNames), findZeroBody, 0),
        list(VS:ValSeq))
      =>
      bisectHigh(VS, bracketLow(VS), bracketHigh(VS))
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
    requires validPolynomial(VS)
endmodule
