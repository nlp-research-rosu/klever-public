requires "verification.k"

module COUNT-NUMS-VACUITY-AUDIT
  imports COUNT-NUMS-VERIFICATION

  // Deliberately false: for the satisfying witness VS = .ValSeq, the actual
  // and specified result is 0, while this mutation demands 1.
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
