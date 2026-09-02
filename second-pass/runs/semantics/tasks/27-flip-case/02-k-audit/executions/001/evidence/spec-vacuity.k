requires "/tmp/audit-work/27-flip-case/candidate/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: prepend U+0021 ("!") to every required result.
  // S = .IntSeq is a satisfying entry state whose real result is empty.
  claim
    <k> #runFlipCase(S:IntSeq) => str(iCons(33, mapSwap(S))) </k>
    <env> 0 </env>
    <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
        0  |-> scope(
                 "flip_case" |->
                   closureVal(
                     ("string", .ParamNames),
                     flipCaseBody,
                     0),
                 parent(-1))
        -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
