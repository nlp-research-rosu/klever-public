requires "verification-mutant.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-MUTANT

  claim [mutated-body-must-not-prove]:
    <k>
      Call(
        Name("median"),
        list(
          vCons(
            3,
            vCons(1, vCons(2, vCons(4, vCons(5, .ValSeq)))))))
      =>
      3
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "median" |-> solutionMedianClosureMutant,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        sortVS(
          vCons(
            3,
            vCons(1, vCons(2, vCons(4, vCons(5, .ValSeq)))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
