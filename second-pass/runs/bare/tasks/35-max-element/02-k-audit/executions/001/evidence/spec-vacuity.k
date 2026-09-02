requires "verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Fresh false mutation of documented example 1: the real maximum is 3,
  // while the mutated result-constraining obligation requires 4.
  claim [false-result]:
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
