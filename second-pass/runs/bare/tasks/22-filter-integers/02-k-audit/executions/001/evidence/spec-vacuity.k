requires "verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Fresh audit mutation of the first concrete entry claim.  For the
  // satisfying input ["a", 3.14, 5], both trusted and submitted Python return
  // [5], so requiring [6] is deliberately false.
  claim [false-entry-result]:
      <k> bootstrap ~> invoke("filter_integers",
            VList(VString("a"), VFloat("3.14"), VInt(5))) => .K </k>
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
        bind("values",
          VList(VString("a"), VFloat("3.14"), VInt(5)), .Env)
      </env>
      <return> noResult => result(VList(VInt(6))) </return>
endmodule
