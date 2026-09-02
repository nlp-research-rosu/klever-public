requires "verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION-LEMMA

  // Deliberately false: the submitted function returns prefixBelow(0, IS),
  // not its negation. Empty input is a satisfying witness (false != true).
  claim
    <k> #loadAll(solutionProgram)
         ~> Call(Name("below_zero"), list(asValSeq(IS:IntVals)))
      => notBool prefixBelow(0, IS)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "below_zero" |-> closureVal(
          "operations", belowZeroFunctionBody, 0),
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
