requires "verification.k"

module BRIDGE-WITNESS-BASE
  imports VERIFICATION-BASE

  // The loop-summary rule accepts an arbitrary scope at -1.  Here "len" is
  // absent, so fixed execution cannot evaluate the while condition.
  claim [missing-len-fixed]:
    <k> #while(strangeCondition(), strangeLoopBody()) => .K </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst"     |-> list(vCons(1, .ValSeq))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 0,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> scope(.Map, root)
      =>
      1 |-> scope(
        "lst"     |-> list(vCons(1, .ValSeq))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 1,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> scope(.Map, root)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(strangePrefix(vCons(1, .ValSeq), 1, 1))
    </heap>
    <heapLoc> 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-WITNESS-EXTENDED
  imports VERIFICATION

  claim [missing-len-bridge]:
    <k> #while(strangeCondition(), strangeLoopBody()) => .K </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst"     |-> list(vCons(1, .ValSeq))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 0,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> scope(.Map, root)
      =>
      1 |-> scope(
        "lst"     |-> list(vCons(1, .ValSeq))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 1,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> scope(.Map, root)
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(strangePrefix(vCons(1, .ValSeq), 1, 1))
    </heap>
    <heapLoc> 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
