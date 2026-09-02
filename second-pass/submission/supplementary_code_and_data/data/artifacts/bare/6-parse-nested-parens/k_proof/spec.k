requires "verification.k"

module SPEC
  imports MPY-VERIFICATION

  // The example in prompt.py.
  claim
      <k> solutionProgram => .K </k>
      <input> "(()()) ((())) () ((())()())" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result>
        noResult
      => result(pyList(pyInt(2) :: pyInt(3) :: pyInt(1) :: pyInt(3) :: .PyVals))
      </result>

  // Increasing nesting depths across four groups.
  claim
      <k> solutionProgram => .K </k>
      <input> "() (()) ((())) (((())))" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result>
        noResult
      => result(pyList(pyInt(1) :: pyInt(2) :: pyInt(3) :: pyInt(4) :: .PyVals))
      </result>

  // A single group whose deepest point is nested four levels.
  claim
      <k> solutionProgram => .K </k>
      <input> "(()(())((())))" </input>
      <env> .Map => .Map </env>
      <functions> .Map => .Map </functions>
      <result> noResult => result(pyList(pyInt(4) :: .PyVals)) </result>
endmodule
