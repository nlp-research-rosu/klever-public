requires "verification.k"

module AUDIT-SPEC-EXAMPLE
  imports MPY-VERIFICATION
  claim
      <k> solutionProgram => .K </k>
      <input> "(()()) ((())) () ((())()())" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result>
        noResult
      => result(pyList(pyInt(2) :: pyInt(3) :: pyInt(1) :: pyInt(3) :: .PyVals))
      </result>
endmodule

module AUDIT-SPEC-INCREASING
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

module AUDIT-SPEC-SINGLE
  imports MPY-VERIFICATION
  claim
      <k> solutionProgram => .K </k>
      <input> "(()(())((())))" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result> noResult => result(pyList(pyInt(4) :: .PyVals)) </result>
endmodule
