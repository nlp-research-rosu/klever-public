requires "verification.k"

module BRIDGE-GROUND-SPEC
  imports VERIFICATION

  claim [correct-plus]:
    <k> applyBin("+", 2, 3) => 5 </k>

  claim [correct-times]:
    <k> applyBin("*", 2, 3) => 6 </k>

  claim [wrong-plus]:
    <k> applyBin("+", 2, 3) => 6 </k>

  claim [wrong-times]:
    <k> applyBin("*", 2, 3) => 7 </k>
endmodule
