requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation. Input [4.0] is satisfiable and the real program
  // returns ["A+"], so requiring ["WRONG"] in the result cell is false.
  claim [false-single-result]:
    <k> solutionProgram => .K </k>
    <input> num(4, 1) :: .Vals </input>
    <env>
      .Map
      =>
        "grade" |-> num(4, 1)
        "grades" |-> list(num(4, 1) :: .Vals)
        "result" |-> list(str("A+") :: .Vals)
    </env>
    <result> noResult => list(str("WRONG") :: .Vals) </result>
endmodule
