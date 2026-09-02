requires "verification.k"

module SPEC-POSITIVE-3
  imports VERIFICATION

  claim
      <k> triangleProgram => .K </k>
      <args> Args(0, 99) </args>
      <env> .Map => ("a" |-> PyNum(0, 1)) ("h" |-> PyNum(99, 1)) </env>
      <result> noResult => PyNum(0, 2) </result>
endmodule
