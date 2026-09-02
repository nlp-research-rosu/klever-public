requires "verification.k"

module SPEC
  imports VERIFICATION

  // The main theorem: for arbitrary integer side and height, interpreting the
  // translated program returns their product divided by two.
  claim
      <k> triangleProgram => .K </k>
      <args> Args(A:Int, H:Int) </args>
      <env> .Map => ("a" |-> PyNum(A, 1)) ("h" |-> PyNum(H, 1)) </env>
      <result> noResult => PyNum(A *Int H, 2) </result>

  // Prompt example: triangle_area(5, 3) == 7.5 == 15/2.
  claim
      <k> triangleProgram => .K </k>
      <args> Args(5, 3) </args>
      <env> .Map => ("a" |-> PyNum(5, 1)) ("h" |-> PyNum(3, 1)) </env>
      <result> noResult => PyNum(15, 2) </result>

  claim
      <k> triangleProgram => .K </k>
      <args> Args(0, 99) </args>
      <env> .Map => ("a" |-> PyNum(0, 1)) ("h" |-> PyNum(99, 1)) </env>
      <result> noResult => PyNum(0, 2) </result>
endmodule
