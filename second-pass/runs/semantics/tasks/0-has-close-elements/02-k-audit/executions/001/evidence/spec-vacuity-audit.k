requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION-WITH-ENTRY

  // Fresh false mutation: demand the Boolean complement of the result produced
  // by the same exact program-load-and-call configuration.
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
