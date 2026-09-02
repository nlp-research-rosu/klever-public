requires "verification.k"

module SIMPLE-POWER-SPEC-VACUITY
  imports SIMPLE-POWER-VERIFICATION

  // Deliberately false: the submitted program returns true when x is 1.
  // N = 4 is a concrete satisfying witness.
  claim [function-one-false]:
    <k> #loadAll(solutionModule)
         ~> Call(Name("is_simple_power"), Int(1), Int(N))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINAL_SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
endmodule
