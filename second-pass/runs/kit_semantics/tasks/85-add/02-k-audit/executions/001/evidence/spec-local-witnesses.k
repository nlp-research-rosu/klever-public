requires "/tmp/audit-work/fresh/verification.k"

module SPEC-LOCAL-WITNESSES
  imports VERIFICATION

  claim [projection-negative]:
    <k> projectIntTotal(-2) => -2 ... </k>

  claim [negative-modulo]:
    <k> applyBin("%", -3, 2) => 1 ... </k>

  claim [integer-addition]:
    <k> applyBin("+", 5, -2) => 3 ... </k>
endmodule
