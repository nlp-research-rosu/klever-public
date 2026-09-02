requires "verification.k"

module SPEC-INTENDED
  imports VERIFICATION

  // The unrestricted entry theorem required by the HumanEval contract.
  claim [all-integer-lists]:
    <k> boot(solutionProgram) => .K </k>
    <input> input(IS:Ints) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map => ?FINAL:Map </env>
    <result> noResult => result(contract(IS)) </result>
endmodule
