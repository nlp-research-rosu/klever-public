requires "verification.k"

module AUDIT-SPEC-RESULT
  imports VERIFICATION

  // Functional correctness of the exact find_zero body, for every symbolic
  // coefficient sequence satisfying the HumanEval input contract.
  claim
    <k>
      Call(
        closureVal(("xs", .ParamNames), findZeroBody, 0),
        list(VS:ValSeq))
      =>
      bisectLow(VS, bracketLow(VS), bracketHigh(VS))
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
