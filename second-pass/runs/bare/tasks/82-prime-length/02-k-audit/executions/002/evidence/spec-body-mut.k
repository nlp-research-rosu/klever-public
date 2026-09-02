requires "verification-body-mut.k"

module SPEC-BODY-MUT
  imports VERIFICATION-BODY-MUT

  claim
    <py>
      <k>
        run(mutatedSolutionProgram, VStr(S))
        => .K
      </k>
      <env>
        .Map
        => ("string" |-> VStr(S)
            "n" |-> VInt(lengthString(S)))
      </env>
      <return>
        noResult => VBool(isPrimeMutTarget(lengthString(S)))
      </return>
    </py>
endmodule
