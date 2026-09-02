requires "verification.k"

module AUDIT-VACUITY
  imports MPY-VERIFICATION

  // Fresh reviewer mutation: for this satisfying input the second result is 2,
  // not 9. The result-bearing destination is the only changed obligation.
  claim
      <k> solutionProgram => .K </k>
      <input> "() (()) ((())) (((())))" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result>
        noResult
      => result(pyList(pyInt(1) :: pyInt(9) :: pyInt(3) :: pyInt(4) :: .PyVals))
      </result>
endmodule
