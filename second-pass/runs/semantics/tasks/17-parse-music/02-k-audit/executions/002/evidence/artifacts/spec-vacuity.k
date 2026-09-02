requires "verification.k"

module PARSE-MUSIC-VACUITY-SPEC
  imports PARSE-MUSIC-VERIFICATION

  // AUDITOR FALSE MUTATION.
  // Satisfiable start: M = whole(.Music), the proof bridge feeds token "o".
  // The real and submitted program returns [4], so requiring [5] is false.
  claim
    <k> #loadAll(parseMusicProgram)
         ~> Call(
              Name("parse_music"),
              str(musicCodes(whole(.Music))),
              .Exprs)
        => ref(0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("parse_music" |-> parseMusicClosure), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(5, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
