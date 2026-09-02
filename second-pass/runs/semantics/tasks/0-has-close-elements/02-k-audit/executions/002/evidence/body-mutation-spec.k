requires "verification-body-mutated.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION-WITH-ENTRY

  claim <k> #loadAll(solutionModule())
              ~> Call(Name("has_close_elements"),
                      list(ALL:FloatSeq), T:Float, .Exprs)
         => hasPairs(ALL, ALL, T, 1) ... </k>
        <env> 0 </env>
        <scopes>
          0  |-> (scope(.Map, parent(-1)) => solutionScope())
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <ret> noRet </ret>
endmodule
