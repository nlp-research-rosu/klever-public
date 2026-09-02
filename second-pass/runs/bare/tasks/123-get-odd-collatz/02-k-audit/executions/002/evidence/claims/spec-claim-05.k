requires "verification.k"

module SPEC-CLAIM-05
  imports VERIFICATION

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 6 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: 3 :: 5 :: .Ints)) </result>
    </python>

endmodule
