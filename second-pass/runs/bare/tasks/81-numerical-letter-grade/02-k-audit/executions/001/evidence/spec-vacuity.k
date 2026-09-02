requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh audit mutation of the one-grade entry claim. Input [4.0] is
  // satisfiable and both Python implementations return ["A+"]. The final
  // environment is kept correct; only the result obligation is changed to E.
  claim [false-four-is-e]:
    <k> solutionProgram => .K </k>
    <input> num(4, 1) :: .Vals </input>
    <env>
      .Map
      =>
        "grade" |-> num(4, 1)
        "grades" |-> list(num(4, 1) :: .Vals)
        "result" |-> list(str("A+") :: .Vals)
    </env>
    <result> noResult => list(str("E") :: .Vals) </result>
endmodule
