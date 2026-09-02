requires "verification.k"

module SPEC-SUMMARY-GROUND
  imports VERIFICATION

  claim [n0]:  <k> fibFrom(0, 1, 0)  => 0  ... </k>
  claim [n1]:  <k> fibFrom(0, 1, 1)  => 1  ... </k>
  claim [n2]:  <k> fibFrom(0, 1, 2)  => 1  ... </k>
  claim [n8]:  <k> fibFrom(0, 1, 8)  => 21 ... </k>
  claim [n10]: <k> fibFrom(0, 1, 10) => 55 ... </k>
endmodule
