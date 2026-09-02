requires "verification.k"

module FRESH-VACUITY-SPEC
  imports VERIFICATION

  // "a123.txt" satisfies the prompt with exactly three ASCII digits.
  // The real generated program returns "Yes", so "No" is deliberately false.
  claim <k> runProgram(solutionProgram, "a123.txt")
          => VStr("No")
        </k>
endmodule
