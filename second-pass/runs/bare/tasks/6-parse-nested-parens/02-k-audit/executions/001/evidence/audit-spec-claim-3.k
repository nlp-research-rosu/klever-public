requires "verification.k"

module AUDIT-SPEC-CLAIM-3
  imports MPY-VERIFICATION

  claim
      <k> solutionProgram => .K </k>
      <input> "(()(())((())))" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result> noResult => result(pyList(pyInt(4) :: .PyVals)) </result>
endmodule
