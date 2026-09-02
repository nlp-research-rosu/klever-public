requires "verification.k"

module GROUND-SUMMARY-SPEC
  imports DIGITS-VERIFICATION

  claim <k> oddDigitProduct(1, 0) => 1 </k>
  claim <k> oddDigitProduct(4, 0) => 0 </k>
  claim <k> oddDigitProduct(235, 0) => 15 </k>
  claim <k> oddDigitProduct(10203, 0) => 3 </k>
  claim <k> oddDigitProduct(13579, 0) => 945 </k>
  claim <k> oddDigitProduct(246, 5) => 5 </k>
endmodule
