requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION-WITH-ENTRY

  // Fresh false mutation: negate the result-constraining all-pairs summary.
  // Satisfying witness ALL=[0.0,0.0], T=1.0 has actual result true, while
  // this destination demands false.
  claim <k> #loadAll(solutionModule())
              ~> Call(Name("has_close_elements"),
                      list(ALL:FloatSeq), T:Float, .Exprs)
         => notBool hasPairs(ALL, ALL, T, 1) ... </k>
        <env> 0 </env>
        <scopes>
          0  |-> (scope(.Map, parent(-1)) => solutionScope())
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule
