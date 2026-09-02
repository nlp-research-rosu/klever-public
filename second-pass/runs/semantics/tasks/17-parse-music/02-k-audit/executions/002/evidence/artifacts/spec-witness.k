requires "verification.k"

module PARSE-MUSIC-ABSTRACT-WITNESS-SPEC
  imports PARSE-MUSIC-VERIFICATION

  // Ground instance of the submitted entry claim:
  // M = whole(half(quarter(.Music))) and its claimed result is [4, 2, 1].
  claim
    <k> #loadAll(parseMusicProgram)
         ~> Call(
              Name("parse_music"),
              str(musicCodes(whole(half(quarter(.Music))))),
              .Exprs)
        => ref(0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("parse_music" |-> parseMusicClosure), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(4, vCons(2, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module PARSE-MUSIC-CONCRETE-WITNESS-SPEC
  imports PARSE-MUSIC-VERIFICATION

  // Independent concrete source-string witness under the supplied semantics.
  claim
    <k> #loadAll(parseMusicProgram)
         ~> Call(Name("parse_music"), Str("o o| .|"), .Exprs)
        => ref(0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("parse_music" |-> parseMusicClosure), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(4, vCons(2, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module PARSE-MUSIC-CONCRETE-ACTUAL-STATE-SPEC
  imports PARSE-MUSIC-VERIFICATION

  // The same concrete source string, with the actual supplied-semantics
  // allocation footprint of str.split included in the destination.
  claim
    <k> #loadAll(parseMusicProgram)
         ~> Call(Name("parse_music"), Str("o o| .|"), .Exprs)
        => ref(0) ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => ("parse_music" |-> parseMusicClosure), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(4, vCons(2, vCons(1, .ValSeq))))
         1 |-> list(
           vCons(
             str(iCons(111, .IntSeq)),
             vCons(
               str(iCons(111, iCons(124, .IntSeq))),
               vCons(str(iCons(46, iCons(124, .IntSeq))), .ValSeq))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
