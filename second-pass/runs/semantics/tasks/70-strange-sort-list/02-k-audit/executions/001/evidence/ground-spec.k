requires "verification.k"

module GROUND-SPEC
  imports VERIFICATION-BASE

  claim [ground-empty]:
    <k>
      Call(
        closureVal(("lst", .ParamNames), strangeBody(), 0),
        list(.ValSeq))
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
      0 |-> list(.ValSeq)
      1 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [ground-three]:
    <k>
      Call(
        closureVal(("lst", .ParamNames), strangeBody(), 0),
        list(vCons(2, vCons(1, vCons(3, .ValSeq)))))
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
      0 |-> list(vCons(1, vCons(2, vCons(3, .ValSeq))))
      1 |-> list(vCons(1, vCons(3, vCons(2, .ValSeq))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [ground-four]:
    <k>
      Call(
        closureVal(("lst", .ParamNames), strangeBody(), 0),
        list(vCons(4, vCons(1, vCons(3, vCons(2, .ValSeq))))))
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
      0 |-> list(vCons(1, vCons(2, vCons(3, vCons(4, .ValSeq)))))
      1 |-> list(vCons(1, vCons(4, vCons(2, vCons(3, .ValSeq)))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-CONTINUATION-SPEC
  imports VERIFICATION-BASE

  claim [continuation]:
    <k>
      #while(strangeCondition(), strangeLoopBody())
      ~> Assign(Name("marker"), Int(99))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst"     |-> list(vCons(2, vCons(1, vCons(3, .ValSeq))))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 0,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      1 |-> scope(
        "lst"     |-> list(vCons(2, vCons(1, vCons(3, .ValSeq))))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 3
        "marker"  |-> 99,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(vCons(1, vCons(2, vCons(3, .ValSeq))))
      1 |-> list(.ValSeq)
      =>
      0 |-> list(vCons(1, vCons(2, vCons(3, .ValSeq))))
      1 |-> list(vCons(1, vCons(3, vCons(2, .ValSeq))))
    </heap>
    <heapLoc> 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-OVERBREADTH-SPEC
  imports VERIFICATION-BASE

  // The summary rule accepts this state because its BS variable does not
  // require builtinsScope. Fixed execution cannot resolve len in this state.
  claim [missing-builtins]:
    <k> #while(strangeCondition(), strangeLoopBody()) => .K </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "lst"     |-> list(vCons(7, .ValSeq))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 0,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> scope(.Map, parent(-1))
      =>
      1 |-> scope(
        "lst"     |-> list(vCons(7, .ValSeq))
        "ordered" |-> ref(0)
        "result"  |-> ref(1)
        "i"       |-> 1,
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> scope(.Map, parent(-1))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(vCons(7, .ValSeq))
      1 |-> list(strangePrefix(vCons(7, .ValSeq), 0, 1))
      =>
      0 |-> list(vCons(7, .ValSeq))
      1 |-> list(strangePrefix(vCons(7, .ValSeq), 1, 1))
    </heap>
    <heapLoc> 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
