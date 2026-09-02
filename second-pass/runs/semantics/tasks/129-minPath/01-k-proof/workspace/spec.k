requires "verification.k"

module MINPATH-SPEC
  imports MINPATH-VERIFICATION

  // Loop invariant: for arbitrary positive remaining length and arbitrary
  // chosen neighbor N, the exact Python for-loop appends the alternating path.
  claim
    <k>
      #loop(rangeObj(I, K, 1), Name("i"), minPathAppendBody)
      => .K
    </k>
    <env> L </env>
    <scopes>
      ...
      L |-> scope(
        ("i" |-> OLD)
        ("path" |-> ref(H))
        ("neighbor" |-> N)
        =>
        ("i" |-> K -Int 1)
        ("path" |-> ref(H))
        ("neighbor" |-> N),
        PARENT)
      ...
    </scopes>
    <heap>
      ...
      H |-> list(P => minPathBuild(P, I, K, N))
      ...
    </heap>
    requires
      0 <=Int I andBool I <Int K

  // Prompt example: top-left 1, path length 3.
  claim
    <k>
      #loadAll(minPathProgram)
      ~> Call(
           Name("minPath"),
           list(vCons(
             list(vCons(1, vCons(2, vCons(3, .ValSeq)))),
             vCons(
               list(vCons(4, vCons(5, vCons(6, .ValSeq)))),
               vCons(
                 list(vCons(7, vCons(8, vCons(9, .ValSeq)))),
                 .ValSeq)))),
           Int(3))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(("minPath" |-> minPathClosure), parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(1, vCons(2, vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Prompt example: interior 1 and the k=1 boundary case.
  claim
    <k>
      #loadAll(minPathProgram)
      ~> Call(
           Name("minPath"),
           list(vCons(
             list(vCons(5, vCons(9, vCons(3, .ValSeq)))),
             vCons(
               list(vCons(4, vCons(1, vCons(6, .ValSeq)))),
               vCons(
                 list(vCons(7, vCons(8, vCons(2, .ValSeq)))),
                 .ValSeq)))),
           Int(1))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(("minPath" |-> minPathClosure), parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(1, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Symbolic theorem: for every permutation of 1..4 in a 2x2 grid, the
  // implementation returns the unique length-four lexicographic minimum.
  claim
    <k>
      #loadAll(minPathProgram)
      ~> Call(
           Name("minPath"),
           list(vCons(
             list(vCons(A, vCons(B, .ValSeq))),
             vCons(list(vCons(C, vCons(D, .ValSeq))), .ValSeq))),
           Int(4))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0 |-> scope(("minPath" |-> minPathClosure), parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(minPathFour(minPathNeighbor2(A, B, C, D)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      1 <=Int A andBool A <=Int 4 andBool
      1 <=Int B andBool B <=Int 4 andBool
      1 <=Int C andBool C <=Int 4 andBool
      1 <=Int D andBool D <=Int 4 andBool
      A =/=Int B andBool A =/=Int C andBool A =/=Int D andBool
      B =/=Int C andBool B =/=Int D andBool C =/=Int D
endmodule
