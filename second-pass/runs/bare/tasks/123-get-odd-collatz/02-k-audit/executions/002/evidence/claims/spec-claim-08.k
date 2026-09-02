requires "verification.k"

module SPEC-CLAIM-08
  imports VERIFICATION

  claim
    <python>
      <k> run(solutionProgram) => .K </k>
      <input> 27 </input>
      <functions> .Map </functions>
      <env> .Map </env>
      <result>
        noResult => result(vl(
          1 :: 5 :: 23 :: 27 :: 31 :: 35 :: 41 :: 47 :: 53 :: 61 ::
          71 :: 91 :: 103 :: 107 :: 121 :: 137 :: 155 :: 161 :: 167 ::
          175 :: 233 :: 251 :: 263 :: 283 :: 319 :: 325 :: 377 :: 395 ::
          425 :: 433 :: 445 :: 479 :: 577 :: 593 :: 719 :: 911 :: 1079 ::
          1367 :: 1619 :: 2051 :: 2429 :: 3077 :: .Ints))
      </result>
    </python>

  // Symbolic branch correctness for every positive even current term.
endmodule
