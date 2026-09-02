requires "/tmp/audit-work/161-solve/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // False for CS = iCons(97, .IntSeq), which satisfies the precondition:
  // real execution returns "A", while this mutant requires "a".
  claim [false-unchanged-result-for-letter]:
    <k> #runSolve(CS:IntSeq) => str(CS) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "solve" |-> solutionClosure(), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (CS ==K mapSwap(CS))
endmodule
