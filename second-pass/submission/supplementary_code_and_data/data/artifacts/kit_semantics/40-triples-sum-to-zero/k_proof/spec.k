requires "verification.k"

module SPEC
  imports VERIFICATION

  // Innermost loop circularity: all third indices k >= K.
  claim [inner-loop]:
    <k>
      #while(innerCond(), innerBody())
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
        0  |-> scope(solutionBindings(), parent(-1))
        -1 |-> builtinsScope
        1  |-> scope(
          ( "l"     |-> ref(0)
            "found" |-> (FOUND:Bool =>
              FOUND orBool thirdFrom(IS, I, J, K))
            "i"     |-> I:Int
            "j"     |-> J:Int
            "k"     |-> (K:Int => isLen(IS))
          ),
          parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(IS:IntSeq)
       0 |-> list(intVals(IS))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack>
      ListItem(frame(CONT:K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I
     andBool I <Int J
     andBool J <Int K
     andBool K <=Int isLen(IS)

  // Middle loop circularity: all pairs j < k for one fixed first index i.
  claim [middle-loop]:
    <k>
      #while(middleCond(), middleBody())
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
        0  |-> scope(solutionBindings(), parent(-1))
        -1 |-> builtinsScope
        1  |-> scope(
          ( "l"     |-> ref(0)
            "found" |-> (FOUND:Bool =>
              FOUND orBool pairFrom(IS, I, J))
            "i"     |-> I:Int
            "j"     |-> (J:Int => isLen(IS))
            "k"     |-> 0
          ),
          parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(IS:IntSeq)
       0 |-> list(intVals(IS))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack>
      ListItem(frame(CONT:K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I
     andBool I <Int J
     andBool J <=Int isLen(IS)

  // Outer loop circularity: all increasing triples beginning at i >= I.
  claim [outer-loop]:
    <k>
      #while(outerCond(), outerBody())
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
        0  |-> scope(solutionBindings(), parent(-1))
        -1 |-> builtinsScope
        1  |-> scope(
          ( "l"     |-> ref(0)
            "found" |-> (FOUND:Bool =>
              FOUND orBool tripleFrom(IS, I))
            "i"     |-> (I:Int => isLen(IS))
            "j"     |-> 0
            "k"     |-> 0
          ),
          parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(IS:IntSeq)
       0 |-> list(intVals(IS))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack>
      ListItem(frame(CONT:K, 0, 1))
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I andBool I <=Int isLen(IS)

  // Required target theorem: the exact public entry call over an arbitrary
  // finite integer sequence returns the increasing-index triple predicate.
  claim [triples-sum-to-zero]:
    <k>
      Call(
        Name("triples_sum_to_zero"),
        (ref(0), .Exprs))
      => tripleFrom(IS:IntSeq, 0)
    </k>
    <env> 0 </env>
    <scopes>
        0  |-> scope(solutionBindings(), parent(-1))
        -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      -1 |-> intSeqGhost(IS)
       0 |-> list(intVals(IS))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
