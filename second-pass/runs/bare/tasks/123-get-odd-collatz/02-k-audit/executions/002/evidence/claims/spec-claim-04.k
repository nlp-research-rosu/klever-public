requires "verification.k"

module SPEC-CLAIM-04
  imports VERIFICATION

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 5 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: 5 :: .Ints)) </result>
    </python>

endmodule
