requires "bridge-verification.k"

module BRIDGE-NEGATIVE-SPEC
  imports BRIDGE-VERIFICATION

  // Fixed MPY evaluates 157 % 10 to 7, so the opposite value 8 must fail.
  claim [wrong-mod]:
    <k> applyBin("%", 157, 10) => 8 </k>

  // Fixed MPY evaluates 157 // 10 to 15, so the opposite value 16 must fail.
  claim [wrong-floordiv]:
    <k> applyBin("//", 157, 10) => 16 </k>
endmodule
