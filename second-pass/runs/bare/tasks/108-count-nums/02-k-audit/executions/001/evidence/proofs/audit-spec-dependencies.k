requires "verification.k"

module AUDIT-HELPERS
  imports VERIFICATION

  claim
    <k> IntV(N) ~> callK("digit_sum") ~> CONT
      => IntV(signedDigitSum(N)) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>

  claim
    <k> ListV(VNil) ~> callK("count_nums") ~> CONT
      => IntV(0) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>

  claim
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) >Int 0

  claim
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) <=Int 0
endmodule

module AUDIT-ENTRY-EMPTY
  imports AUDIT-HELPERS
  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VNil))
      => IntV(0) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
endmodule

module AUDIT-ENTRY-POSITIVE
  imports AUDIT-HELPERS
  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) >Int 0
endmodule

module AUDIT-ENTRY-NONPOSITIVE
  imports AUDIT-HELPERS
  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) <=Int 0
endmodule
