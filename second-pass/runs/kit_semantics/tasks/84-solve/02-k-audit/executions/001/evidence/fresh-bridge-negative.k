requires "bridge-verification.k"

module FRESH-BRIDGE-NEGATIVE
  imports BRIDGE-VERIFICATION

  // Fixed MPy gives 83 % 10 = 3, not 4.
  claim [wrong-mod]:
    <k> applyBin("%", 83, 10) => 4 </k>

  // Fixed MPy gives 83 // 10 = 8, not 9.
  claim [wrong-floordiv]:
    <k> applyBin("//", 83, 10) => 9 </k>
endmodule
