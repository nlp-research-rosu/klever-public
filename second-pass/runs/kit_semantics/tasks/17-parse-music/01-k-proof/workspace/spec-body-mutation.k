requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberate program mutation: an "o" character sets current to 5, not 4.
  // The original postcondition for the ground input "o" must therefore fail.
  claim [changed-whole-note]:
    <k> Call(
      Name("parse_music"),
      str(iCons(111, .IntSeq)) , .Exprs)
      => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "parse_music" |-> closureVal(
          "music_string" , .ParamNames,
          mutatedParseMusicBody,
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(4, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
