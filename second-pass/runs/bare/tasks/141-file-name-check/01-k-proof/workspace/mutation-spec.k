requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  // Negative validation probe: a known valid name must not return "No".
  claim <k> runProgram(solutionProgram, "example.txt")
          => VStr("No")
        </k>
endmodule
