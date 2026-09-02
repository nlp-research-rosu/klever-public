requires "verification.k"

module SPEC-UNIVERSAL-AUDIT
  imports MPY-VERIFICATION

  // The natural modeled-domain target missing from candidate spec.k:
  // execute the whole submitted algorithm for an arbitrary finite PyVals list
  // and return exactly the stable integer-instance filter of that list.
  claim [universal-entry]:
      <k> bootstrap ~> invoke("filter_integers", VList(VS:PyVals)) => .K </k>
      <program> solutionModule() </program>
      <functions>
        .Functions
        =>
        bindFunction("filter_integers",
          function("values", Return(filterExpression())), .Functions)
      </functions>
      <env>
        .Env
        =>
        bind("values", VList(VS), .Env)
      </env>
      <return>
        noResult => result(VList(onlyIntegerInstances(VS)))
      </return>
endmodule
