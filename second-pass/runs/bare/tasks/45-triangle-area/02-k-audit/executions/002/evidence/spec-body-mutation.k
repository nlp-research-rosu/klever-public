requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim
      <k> triangleProgramMutated => .K </k>
      <args> Args(5, 3) </args>
      <env> .Map => ("a" |-> PyNum(5, 1)) ("h" |-> PyNum(3, 1)) </env>
      <result> noResult => PyNum(15, 2) </result>
endmodule
