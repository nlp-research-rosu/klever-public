requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result obligation. The precondition is true and the
  // satisfying witness input "zero" actually returns VStr("zero").
  claim [false-zero-result]:
    <k> solutionProgram ~> invoke("zero") => VStr("one") </k>
endmodule
