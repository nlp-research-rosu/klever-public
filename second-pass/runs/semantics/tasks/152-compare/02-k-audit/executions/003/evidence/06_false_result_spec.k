requires "verification.k"

module AUDITOR-FALSE-RESULT-SPEC
  imports COMPARE-VERIFICATION

  // Satisfiable witness: compare([1], [2]) returns [1], not [2].
  // This mutates only the result-bearing heap obligation.
  claim
    <k>
      compareDef
      ~> Call(
           Name("compare"),
           list(vCons(1, .ValSeq)),
           list(vCons(2, .ValSeq)))
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
      0 |-> list(vCons(2, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
