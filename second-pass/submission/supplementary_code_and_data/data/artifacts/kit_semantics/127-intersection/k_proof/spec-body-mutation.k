requires "mutation-verification.k"

module SPEC-BODY-MUTATION
  imports MUTATION-VERIFICATION

  // The mutant changes the final YES return to NO. Keeping the correct
  // length-2 expectation must therefore fail.
  claim [mutated-body-must-not-prove]:
    <k>
      #loadAll(mutantSolutionModule)
      ~> Call(Name("intersection"),
              TupleExpr(Int(-3), Int(-1)),
              TupleExpr(Int(-5), Int(5)))
      => str(strToCodes("YES"))
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
