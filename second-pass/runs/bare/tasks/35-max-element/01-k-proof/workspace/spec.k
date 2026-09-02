requires "verification.k"

module SPEC
  imports MPY-VERIFICATION

  // Universal functional-correctness theorem: for every non-empty integer
  // list, executing the translated function returns its mathematical maximum.
  claim
    <mpy>
      <k> solutionProgram ~> invoke("max_element", IS:IntSeq) => .K </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("l"))))
      </functions>
      <env> .Map => "l" |-> IS </env>
      <result> noResult => result(expectedMaximum(IS)) </result>
    </mpy>

  // The two examples from prompt.py are retained as concrete regression
  // theorems in addition to the universal theorem above.
  claim
    <mpy>
      <k> solutionProgram ~> invoke("max_element", [1, 2, 3]) => .K </k>
      <functions> .Map =>
        "max_element" |-> closure(
          Params("l"), Return(Call(Name("max"), Name("l"))))
      </functions>
      <env> .Map => "l" |-> [1, 2, 3] </env>
      <result> noResult => result(3) </result>
    </mpy>

  claim
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
