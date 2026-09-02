requires "verification.k"

module SPEC-CLAIM-01
  imports VERIFICATION

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 1 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: .Ints)) </result>
    </python>

endmodule
