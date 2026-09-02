requires "/tmp/audit-work/audit-108/source/verification.k"

module COUNT-NUMS-SPEC-VACUITY
  imports COUNT-NUMS-VERIFICATION

  // Deliberately false: for every satisfying input, the real result is
  // countPositive(VS), not one greater. The empty list is a concrete witness
  // (allInts(.ValSeq) is true, actual result 0, mutated target 1).
  claim
    <k> #applyK(toCall(countNumsClosure),
                (list(VS:ValSeq), .Vals))
      => countPositive(VS) +Int 1 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(digitFunctionBindings, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
