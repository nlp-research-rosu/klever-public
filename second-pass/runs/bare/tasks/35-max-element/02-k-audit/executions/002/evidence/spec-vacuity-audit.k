requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports MPY-VERIFICATION

  // Auditor-created false result obligation. The satisfying input [1,2,3]
  // returns 3, so requiring 4 must leave an execution/result residual.
  claim
    <mpy>
      <k> solutionProgram ~> invoke("max_element", [1, 2, 3]) => .K </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("l"))))
      </functions>
      <env> .Map => "l" |-> [1, 2, 3] </env>
      <result> noResult => result(4) </result>
    </mpy>
endmodule
