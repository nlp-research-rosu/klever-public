requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop invariant.  Starting with previous=current=P and drops=D, scanning
  // VS leaves both value locals at lastAfter(P, VS) and transforms D by the
  // exact strict-descent accumulator fold scanDrops.
  claim [scan-loop]:
    <k> #loop(list(VS:ValSeq), Name("current"), scanBody)
        => .K ... </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "arr"      |-> ARR:Val
        "first"    |-> F:Val
        "previous" |-> (P:Val => lastAfter(P, VS))
        "current"  |-> (P => lastAfter(P, VS))
        "drops"    |-> (D:Int => scanDrops(D, P, VS)),
        parent(0))
    </scopes>
    requires isInt(P) andBool allInts(VS)

  // Whole-program partial correctness from the exact function binding and
  // body.  The theorem covers every finite list of mathematical integers.
  claim [move-one-ball]:
    <k> Call(Name("move_one_ball"), (list(VS:ValSeq), .Exprs))
        => moveSpec(VS) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
         "move_one_ball" |-> closureVal("arr", moveOneBallBody, 0),
         parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
