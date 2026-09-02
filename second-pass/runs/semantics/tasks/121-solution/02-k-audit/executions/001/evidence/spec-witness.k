requires "verification.k"

module SPEC-WITNESS
  imports VERIFICATION

  claim [summary-ground]:
    <k>
      oddAtEvenPositions(
        vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq)))),
        true)
      =>
      12
    </k>

  claim [entry-ground]:
    <k>
      Call(
        solutionClosure,
        (list(vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq))))), .Exprs))
      =>
      12
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
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
