requires "verification-body-mutated.k"

module FIX-SPACES-BODY-MUTATED-SPEC
  imports FIX-SPACES-VERIFICATION

  // The actual function body now emits one underscore for exactly two trailing
  // spaces, while the unchanged result summary still demands two.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("fix_spaces"), str(IS:IntSeq))
      =>
      str(
        appendPending(
          fixSpacesLoop(.IntSeq, IS, 0),
          trailingSpaces(IS, 0)))
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
