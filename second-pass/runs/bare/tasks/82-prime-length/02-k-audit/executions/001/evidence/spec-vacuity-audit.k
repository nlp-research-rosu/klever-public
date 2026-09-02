requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the real K execution returns false for S = "",
  // while this mutation requires true for every input.
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
        noResult => VBool(true)
      </return>
    </py>
endmodule
