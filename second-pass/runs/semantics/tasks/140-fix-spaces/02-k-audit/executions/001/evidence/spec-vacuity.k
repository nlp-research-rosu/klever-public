requires "verification.k"

module FIX-SPACES-MAIN-VACUITY
  imports FIX-SPACES-VERIFICATION

  // False mutation: append an extra underscore to the claimed result.
  // The unchanged precondition is satisfiable with IS = .IntSeq, for which
  // the real program returns the empty string, not "_".
  claim [false-extra-underscore]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("fix_spaces"), str(IS:IntSeq))
      =>
      str(
        seqConcat(
          appendPending(
            fixSpacesLoop(.IntSeq, IS, 0),
            trailingSpaces(IS, 0)),
          iCons(95, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |->
        scope(
          "fix_spaces" |->
            closureVal("text", fixSpacesFunctionBody, 0),
          parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
