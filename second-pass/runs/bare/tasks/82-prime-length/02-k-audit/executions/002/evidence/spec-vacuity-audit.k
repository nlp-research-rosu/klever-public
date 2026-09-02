requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: for satisfying witness S = "ab", actual is true while
  // this mutated result obligation requires false.
  claim
    <py>
      <k>
        run(solutionProgram, VStr(S))
        => .K
      </k>
      <env>
        .Map
        => ("string" |-> VStr(S)
            "n" |-> VInt(lengthString(S)))
      </env>
      <return>
        noResult => VBool(notBool isPrime(lengthString(S)))
      </return>
    </py>
endmodule
