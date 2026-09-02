requires "verification.k"

module SPEC-CLAIM-07
  imports VERIFICATION

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 19 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result>
        noResult =>
          result(vl(1 :: 5 :: 11 :: 13 :: 17 :: 19 :: 29 :: .Ints))
      </result>
    </python>

  // A long trajectory (112 Collatz transitions) stress-tests the loop.
endmodule
