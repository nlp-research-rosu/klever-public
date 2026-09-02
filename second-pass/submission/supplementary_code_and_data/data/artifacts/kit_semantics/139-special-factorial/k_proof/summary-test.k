requires "verification.k"

module SUMMARY-TEST
  imports VERIFICATION

  claim [n1]: <k> productAfter(1, 1, 1, 1) => 1 </k>
  claim [n2]: <k> productAfter(1, 2, 1, 1) => 2 </k>
  claim [n3]: <k> productAfter(1, 3, 1, 1) => 12 </k>
  claim [n4]: <k> productAfter(1, 4, 1, 1) => 288 </k>
  claim [n5]: <k> productAfter(1, 5, 1, 1) => 34560 </k>
  claim [n6]: <k> productAfter(1, 6, 1, 1) => 24883200 </k>

  claim [factorial-n1]: <k> factorialAfter(1, 1, 1) => 1 </k>
  claim [factorial-n2]: <k> factorialAfter(1, 2, 1) => 2 </k>
  claim [factorial-n3]: <k> factorialAfter(1, 3, 1) => 6 </k>
  claim [factorial-n4]: <k> factorialAfter(1, 4, 1) => 24 </k>
  claim [factorial-n5]: <k> factorialAfter(1, 5, 1) => 120 </k>
  claim [factorial-n6]: <k> factorialAfter(1, 6, 1) => 720 </k>
endmodule
