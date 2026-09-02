requires "verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports MPY-VERIFICATION

  claim
    <mpy>
      <k> solutionProgram ~> invoke("max_element", IS:IntSeq) => .K </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Name("l")))
      </functions>
      <env> .Map => "l" |-> IS </env>
      <result> noResult => result(expectedMaximum(IS)) </result>
    </mpy>
endmodule
