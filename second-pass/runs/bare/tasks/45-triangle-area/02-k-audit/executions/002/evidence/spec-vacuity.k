requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: 5 * 3 / 2 is 15/2, not 16/2.
  claim
      <k> triangleProgram => .K </k>
      <args> Args(5, 3) </args>
      <env> .Map => ("a" |-> PyNum(5, 1)) ("h" |-> PyNum(3, 1)) </env>
      <result> noResult => PyNum(16, 2) </result>
endmodule
