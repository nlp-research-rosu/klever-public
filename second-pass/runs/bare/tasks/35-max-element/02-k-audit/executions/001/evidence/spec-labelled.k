requires "verification.k"

module SPEC-LABELLED
  imports MPY-VERIFICATION

  claim [universal]:
    <mpy>
      <k> solutionProgram ~> invoke("max_element", IS:IntSeq) => .K </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("l"))))
      </functions>
      <env> .Map => "l" |-> IS </env>
      <result> noResult => result(expectedMaximum(IS)) </result>
    </mpy>

  claim [documented-example-1]:
    <mpy>
      <k> solutionProgram ~> invoke("max_element", [1, 2, 3]) => .K </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("l"))))
      </functions>
      <env> .Map => "l" |-> [1, 2, 3] </env>
      <result> noResult => result(3) </result>
    </mpy>

  claim [documented-example-2]:
    <mpy>
      <k>
        solutionProgram ~> invoke(
          "max_element", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]
        )
        => .K
      </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("l"))))
      </functions>
      <env> .Map =>
        "l" |-> [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]
      </env>
      <result> noResult => result(123) </result>
    </mpy>
endmodule
