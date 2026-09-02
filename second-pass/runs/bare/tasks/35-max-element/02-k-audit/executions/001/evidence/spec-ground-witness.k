requires "verification.k"

module SPEC-GROUND-WITNESS
  imports MPY-VERIFICATION

  claim [universal-substitution]:
    <mpy>
      <k>
        solutionProgram ~> invoke("max_element", [-4, 8, 8, 1])
        => .K
      </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("l"))))
      </functions>
      <env> .Map => "l" |-> [-4, 8, 8, 1] </env>
      <result> noResult => result(8) </result>
    </mpy>
endmodule
