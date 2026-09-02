requires "verification.k"

module SIMPLE-POWER-SPEC-VACUITY
  imports SIMPLE-POWER-VERIFICATION

  // Deliberately false: the submitted function always returns true when x=1,
  // independently of n.  The fixed witness n=4 makes the precondition concrete.
  claim [false-function-one]:
    <k> #loadAll(solutionModule)
         ~> Call(Name("is_simple_power"), Int(1), Int(4))
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
