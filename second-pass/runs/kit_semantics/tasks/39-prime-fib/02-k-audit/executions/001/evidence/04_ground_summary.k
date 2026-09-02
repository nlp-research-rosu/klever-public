requires "verification.k"

module GROUND-SUMMARY
  imports VERIFICATION

  claim [n1]:
    <k> primeFibSearch(1, 0, 0, 1) => 2 ... </k>

  claim [n5]:
    <k> primeFibSearch(5, 0, 0, 1) => 89 ... </k>
endmodule
