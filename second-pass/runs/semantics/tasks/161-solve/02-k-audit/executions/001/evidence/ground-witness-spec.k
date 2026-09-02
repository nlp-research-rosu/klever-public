requires "verification.k"

module GROUND-WITNESS-SPEC
  imports VERIFICATION

  claim [ascii-letter]:
    <k> #runSolve(iCons(97, .IntSeq)) => str(iCons(65, .IntSeq)) </k>
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

  claim [ascii-no-letter]:
    <k> #runSolve(iCons(49, iCons(50, .IntSeq)))
      => str(iCons(50, iCons(49, .IntSeq)))
    </k>
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

  // The supplied ASCII model leaves Greek code points unchanged under mapSwap.
  claim [greek-model-boundary]:
    <k> #runSolve(iCons(945, iCons(946, .IntSeq)))
      => str(iCons(946, iCons(945, .IntSeq)))
    </k>
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
endmodule
