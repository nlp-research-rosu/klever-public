requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [digit-helper]:
    <k> IntV(N) ~> callK("digit_sum") ~> CONT
      => IntV(signedDigitSum(N)) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>

  claim [count-empty]:
    <k> ListV(VNil) ~> callK("count_nums") ~> CONT
      => IntV(0) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>

  claim [count-positive-head]:
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) >Int 0

  claim [count-nonpositive-head]:
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) <=Int 0

  claim [entry-empty]:
    <k> solutionProgram ~> invoke("count_nums", ListV(VNil))
      => IntV(0) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>

  claim [entry-positive-head]:
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) >Int 0

  claim [entry-nonpositive-head]:
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) <=Int 0
endmodule
