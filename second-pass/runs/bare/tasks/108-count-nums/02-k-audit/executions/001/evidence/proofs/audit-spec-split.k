requires "verification.k"

module AUDIT-SPEC-1
  imports VERIFICATION
  claim
    <k> IntV(N) ~> callK("digit_sum") ~> CONT
      => IntV(signedDigitSum(N)) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
endmodule

module AUDIT-SPEC-2
  imports VERIFICATION
  claim
    <k> ListV(VNil) ~> callK("count_nums") ~> CONT
      => IntV(0) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
endmodule

module AUDIT-SPEC-3
  imports VERIFICATION
  claim
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) >Int 0
endmodule

module AUDIT-SPEC-4
  imports VERIFICATION
  claim
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) <=Int 0
endmodule

module AUDIT-SPEC-5
  imports VERIFICATION
  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VNil))
      => IntV(0) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
endmodule

module AUDIT-SPEC-6
  imports VERIFICATION
  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) >Int 0
endmodule

module AUDIT-SPEC-7
  imports VERIFICATION
  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) <=Int 0
endmodule
