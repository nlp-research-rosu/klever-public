requires "verification.k"

module SPEC-VACUITY
  imports FIX-SPACES-VERIFICATION

  // Fresh false mutation: demand an extra trailing "!" in every returned
  // value. The empty IntSeq is a satisfying input, and fix_spaces("") == "".
  claim [false-extra-bang]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("fix_spaces"), str(IS:IntSeq))
      =>
      str(
        seqConcat(
          appendPending(
            fixSpacesLoop(.IntSeq, IS, 0),
            trailingSpaces(IS, 0)),
          iCons(33, .IntSeq)))
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
