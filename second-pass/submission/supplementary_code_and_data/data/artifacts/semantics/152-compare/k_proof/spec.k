requires "verification.k"

module COMPARE-SPEC
  imports COMPARE-VERIFICATION

  // Universal functional-correctness theorem.  GAME and GUESS range over
  // arbitrary finite integer sequences.  Since absDiffs follows zip, this
  // proves the required equal-length case and the stronger truncating case.
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(intVals(GAME:IntSeq)),
           list(intVals(GUESS:IntSeq)))
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
      0 |-> list(absDiffs(intVals(GAME), intVals(GUESS)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  // The two examples in prompt.py are also closed as concrete proof claims.
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
endmodule
