requires "verification.k"

module SPEC
  imports VERIFICATION

  // One symbolic reachability claim covers every possible input string.
  // Its postcondition is the independently named primality predicate from
  // verification.k, applied to the K builtin string length.
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
        noResult => VBool(isPrime(lengthString(S)))
      </return>
    </py>
endmodule
