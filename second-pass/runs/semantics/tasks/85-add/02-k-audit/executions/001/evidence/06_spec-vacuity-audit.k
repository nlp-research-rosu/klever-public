requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation. For the satisfying input [4, 2, 6, 7], the program
  // and both Python implementations return 2, while this postcondition requires 3.
  claim [add-false-off-by-one]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("add"), (list(intVals(INPUT:IntSeq)), .Exprs))
      =>
      addAccSpec(INPUT, false, 0) +Int 1
    </k>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <env> 0 </env>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
