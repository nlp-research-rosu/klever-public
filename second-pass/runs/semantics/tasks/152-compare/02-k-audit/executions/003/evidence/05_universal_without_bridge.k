requires "verification.k"

module UNIVERSAL-WITHOUT-BRIDGE
  imports COMPARE-COMMON

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
endmodule
