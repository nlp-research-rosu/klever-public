requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim [body-sensitivity]:
    <python>
      <k> verifyMutant(mutantProgram, vlist(1, 2, 3, 4, 5, .Rats))
           => doneMutant(vlist(0, 1 /Rat 4, 1 /Rat 2, 3 /Rat 4, 1, .Rats))
      </k>
      <functions> .Map </functions>
      <env> .Map </env>
      <result> noResult </result>
    </python>
endmodule
