requires "verification.k"

module SPEC
  imports VERIFICATION

  // Lemma 1: the translated recursive helper implements the mathematical
  // signed decimal digit sum for every mathematical integer.
  claim
    <k> IntV(N) ~> callK("digit_sum") ~> CONT
      => IntV(signedDigitSum(N)) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>

  // Lemma 2, empty constructor case.
  claim
    <k> ListV(VNil) ~> callK("count_nums") ~> CONT
      => IntV(0) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>

  // Lemma 2, nonempty constructor with a positive signed digit sum.
  claim
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) >Int 0

  // Lemma 2, complementary nonpositive-head case.  The three Lemma 2 claims
  // are exhaustive and form structural induction over every finite VList.
  claim
    <k> ListV(VCons(I, REST)) ~> callK("count_nums") ~> CONT
      => IntV(countPositive(VCons(I, REST))) ~> CONT </k>
    <funs> solutionFuns </funs>
    <env> _ENV </env>
    <stack> _STACK </stack>
    requires signedDigitSum(I) <=Int 0

  // End-to-end theorem cases: load the exact program tree and invoke its
  // required entry point from a clean initial machine state.
  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VNil))
      => IntV(0) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>

  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) >Int 0

  claim
    <k> solutionProgram ~> invoke("count_nums", ListV(VCons(I, REST)))
      => IntV(countPositive(VCons(I, REST))) </k>
    <funs> .Map => solutionFuns </funs>
    <env> .Map </env>
    <stack> .List </stack>
    requires signedDigitSum(I) <=Int 0
endmodule
