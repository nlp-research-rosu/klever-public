requires "verification.k"

module MUTATION-SPEC
  imports MPY-VERIFICATION

  // Deliberately false: the last group has depth 3, not 4.  prove.sh requires
  // this claim to fail, demonstrating that the positive claims are sensitive
  // to an incorrect result.
  claim
      <k> solutionProgram => .K </k>
      <input> "(()()) ((())) () ((())()())" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result>
        noResult
      => result(pyList(pyInt(2) :: pyInt(3) :: pyInt(1) :: pyInt(4) :: .PyVals))
      </result>
endmodule
