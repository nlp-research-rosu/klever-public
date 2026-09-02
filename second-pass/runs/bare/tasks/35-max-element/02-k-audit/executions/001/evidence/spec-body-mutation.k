requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports MPY-VERIFICATION-BODY-MUTATION

  claim [changed-body]:
    <mpy>
      <k>
        solutionProgramBodyMutation ~> invoke("max_element", [1, 2, 3])
        => .K
      </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("x"))))
      </functions>
      <env> .Map => "l" |-> [1, 2, 3] </env>
      <result> noResult => result(3) </result>
    </mpy>
endmodule
