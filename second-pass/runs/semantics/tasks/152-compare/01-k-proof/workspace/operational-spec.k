requires "verification.k"

module COMPARE-OPERATIONAL-SPEC
  imports COMPARE-COMMON

  // These claims deliberately import COMPARE-COMMON instead of
  // COMPARE-VERIFICATION, so the concrete lists execute through every raw
  // #loop/#iterNext, tuple bind, subtraction, abs, and append rule.
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(1, vCons(2, vCons(3, vCons(4, vCons(5, vCons(1, .ValSeq))))))),
           list(vCons(1, vCons(2, vCons(3, vCons(4, vCons(2, vCons(-2, .ValSeq))))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(0, vCons(0, vCons(0, vCons(0, vCons(3, vCons(3, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(0, vCons(5, vCons(0, vCons(0, vCons(0, vCons(4, .ValSeq))))))),
           list(vCons(4, vCons(1, vCons(1, vCons(0, vCons(0, vCons(-2, .ValSeq))))))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(4, vCons(4, vCons(1, vCons(0, vCons(0, vCons(6, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k>
      compareDef
      ~> Call(Name("compare"), list(.ValSeq), list(.ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(-7, vCons(9, .ValSeq))),
           list(vCons(5, vCons(-4, .ValSeq))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
               "compare" |-> closureVal(
                 ("game", "guess"),
                 compareBody,
                 0),
               parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(12, vCons(13, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
