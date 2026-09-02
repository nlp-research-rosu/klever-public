requires "stage5-wrong-oracle-verification.k"

module WRONG-ORACLE-SPEC
  imports WRONG-ORACLE-VERIFICATION

  // Deliberately false for the satisfying intended input [2], whose real
  // Python result is [2, 0]. This tests value sensitivity, not non-vacuity.
  claim
    <py>
      <k> witnessSolutionProgram ~> start => .K </k>
      <args> VArray(ID, 0, LENGTH) </args>
      <env> .Map => .Map </env>
      <funs> .Map => witnessSolutionFunctions </funs>
      <stack> .List => .List </stack>
      <result> VNone => VList(.Ints) </result>
    </py>
    requires LENGTH >=Int 0
endmodule
