requires "verification.k"

module SPEC-INTENDED-ENTRY
  imports VERIFICATION

  // The missing universal entry-to-return theorem for every integer list.
  claim
    <k> boot(solutionProgram) => .K </k>
    <input> input(IS:Ints) </input>
    <function> .Function => function("arr", solutionBody) </function>
    <env> .Map => ?FINAL:Map </env>
    <result> noResult => result(contract(IS)) </result>
endmodule
