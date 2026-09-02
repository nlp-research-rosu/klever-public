requires "verification-body-mutant.k"

module PARSE-MUSIC-LOOP-SPEC
  imports PARSE-MUSIC-BASE

  // Inductive functional-correctness claim for the exact loop in solution.py:
  // for every finite valid note sequence and every existing result prefix,
  // execution appends precisely the durations prescribed by musicAcc.
  claim
    <k> #loop(musicIter(M:Music), Name("note"), parseMusicLoopBody)
        => .K
    </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
            ("music_string" |-> S:Val)
            ("beats" |-> ref(B))
            ("note" |-> (N:Val => musicLast(N, M))),
            P:Parent)
          ...
    </scopes>
    <heap>
      ... B:Int |-> list(A:ValSeq => musicAcc(A, M)) ...
    </heap>
endmodule

module PARSE-MUSIC-ENTRY-SPEC
  imports PARSE-MUSIC-VERIFICATION

  // End-to-end correctness of the translated entry point for every finite
  // valid music sequence represented by the symbolic split boundary.
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
    <heap> .Map => 0 |-> list(musicAcc(.ValSeq, M)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
