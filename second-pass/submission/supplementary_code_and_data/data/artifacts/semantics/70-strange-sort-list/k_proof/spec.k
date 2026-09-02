requires "verification.k"

module LOOP-SPEC
  imports VERIFICATION-BASE

  // Inductive loop invariant.  S is the already sorted sequence, N its
  // length, and result contains exactly the first I alternating selections.
  claim [loop-invariant]:
    <k> #while(strangeCondition(), strangeLoopBody()) => .K </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst"     |-> LIST:Val
        "ordered" |-> ref(HO:Int)
        "result"  |-> ref(HR:Int)
        "i"       |-> I:Int,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      1 |-> scope(
        "lst"     |-> LIST
        "ordered" |-> ref(HO)
        "result"  |-> ref(HR)
        "i"       |-> N:Int,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <heap>
      HO |-> list(S:ValSeq)
      HR |-> list(strangePrefix(S, I, N))
      =>
      HO |-> list(S)
      HR |-> list(strangePrefix(S, N, N))
    </heap>
    <scopeLoc> 2 </scopeLoc>
    <heapLoc> 2 </heapLoc>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int I andBool I <=Int N
      andBool N ==Int vsLen(S)

endmodule

module SPEC
  imports VERIFICATION

  // End-to-end claim for the actual translated function body.  The result is
  // a fresh list containing the alternating low/high traversal of sortVS(VS).
  claim [function-correct]:
    <k>
      Call(
        closureVal(("lst", .ParamNames), strangeBody(), 0),
        list(INPUT:ValSeq))
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(INPUT))
      1 |-> list(strangeResult(sortVS(INPUT)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
