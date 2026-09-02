requires "verification.k"

module SPEC-CLAIM-03
  imports VERIFICATION

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 3 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult => result(vl(1 :: 3 :: 5 :: .Ints)) </result>
    </python>

  // This is the example required by prompt.py.
endmodule
