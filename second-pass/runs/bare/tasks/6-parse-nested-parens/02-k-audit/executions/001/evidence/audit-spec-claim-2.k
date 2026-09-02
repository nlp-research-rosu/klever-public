requires "verification.k"

module AUDIT-SPEC-CLAIM-2
  imports MPY-VERIFICATION

  claim
      <k> solutionProgram => .K </k>
      <input> "() (()) ((())) (((())))" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result>
        noResult
      => result(pyList(pyInt(1) :: pyInt(2) :: pyInt(3) :: pyInt(4) :: .PyVals))
      </result>
endmodule
