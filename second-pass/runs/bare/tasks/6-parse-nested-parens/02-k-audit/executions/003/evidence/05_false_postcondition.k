requires "verification.k"

module AUDIT-FALSE-POSTCONDITION
  imports MPY-VERIFICATION

  // Fresh audit mutation of the third positive claim: both Python programs
  // return depth 4 for this satisfying input, so requiring 5 is false.
  claim
      <k> solutionProgram => .K </k>
      <input> "(()(())((())))" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result> noResult => result(pyList(pyInt(5) :: .PyVals)) </result>
endmodule
