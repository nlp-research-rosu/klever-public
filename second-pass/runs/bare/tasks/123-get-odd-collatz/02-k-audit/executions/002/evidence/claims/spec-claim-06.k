requires "verification.k"

module SPEC-CLAIM-06
  imports VERIFICATION

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 7 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result>
        noResult => result(vl(1 :: 5 :: 7 :: 11 :: 13 :: 17 :: .Ints))
      </result>
    </python>

endmodule
