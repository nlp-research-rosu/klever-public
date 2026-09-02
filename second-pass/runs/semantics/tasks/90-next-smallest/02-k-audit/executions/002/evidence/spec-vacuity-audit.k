requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports NEXT-SMALLEST-WITH-LOOP-LEMMA

  // Deliberately false: every input is claimed to return None.  The satisfying
  // input [3, 1, 2, 1] returns 2 in the canonical and generated Python code.
  claim
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("next_smallest"),
              (list(intVals(INPUT:Ints)), .Exprs))
    =>
      noneV
    </k>
    <env> 0 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    =>
      ?FINAL_ENTRY_SCOPES:Map
    </scopes>
    <scopeLoc> 1 => 1 </scopeLoc>
    <heap> .Map => .Map </heap>
    <heapLoc> 0 => 0 </heapLoc>
    <stack> .List => .List </stack>
    <ret> noRet => noRet </ret>
    <exc> NoExc => NoExc </exc>
    <exit-code> 0 => 0 </exit-code>
endmodule
