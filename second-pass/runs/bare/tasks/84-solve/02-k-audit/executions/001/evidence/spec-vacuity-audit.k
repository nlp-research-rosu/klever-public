requires "semantic.k"

module SPEC-VACUITY-AUDIT
  imports SEMANTIC

  // Deliberately false: solve(147) returns "1100", not "1101".
  // This mutates the result-bearing destination itself.
  claim [wrong-result-147]:
    <k> runProgram(solutionProgram, 147) => VStr("1101") </k>
endmodule
