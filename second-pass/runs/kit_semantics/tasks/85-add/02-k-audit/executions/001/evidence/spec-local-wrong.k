requires "/tmp/audit-work/fresh/verification.k"

module SPEC-LOCAL-WRONG
  imports VERIFICATION

  // Opposite ground interpretation of the result-bearing projection.
  claim [wrong-projection]:
    <k> projectIntTotal(-2) => 7 </k>
endmodule
