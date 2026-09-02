requires "verification.k"

module SPEC-POSITIVE-1
  imports VERIFICATION

  claim
      <k> triangleProgram => .K </k>
      <args> Args(A:Int, H:Int) </args>
      <env> .Map => ("a" |-> PyNum(A, 1)) ("h" |-> PyNum(H, 1)) </env>
      <result> noResult => PyNum(A *Int H, 2) </result>
endmodule
