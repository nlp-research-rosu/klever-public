requires "verification.k"

module PARSE-MUSIC-ENTRY-VACUITY
  imports PARSE-MUSIC-VERIFICATION

  // Fresh false mutation of the result-bearing heap obligation. For M = .Music
  // the satisfying input is the empty string: both Python implementations
  // return [], while this destination requires the returned list to begin 99.
  claim
    <k> #loadAll(parseMusicProgram)
         ~> Call(Name("parse_music"), str(musicCodes(M:Music)), .Exprs)
        => ref(0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("parse_music" |-> parseMusicClosure), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map => 0 |-> list(vCons(99, musicAcc(.ValSeq, M)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
