requires "/tmp/audit-work/scratch/verification.k"

module SUMMARY-PROBE
  imports VERIFICATION

  claim [composite-four]:
    <k> scanPrime(4, 2, true) => false </k>

  claim [prime-two]:
    <k> scanPrime(2, 2, true) => true </k>

  claim [prime-five]:
    <k> scanPrime(5, 2, true) => true </k>

  claim [nine-divisor-at-three]:
    <k> scanPrime(9, 3, true) => false </k>

  claim [nine-fold-at-three]:
    <k> scanPrime(9, 3, true) => scanPrime(9, 2, true) </k>
endmodule
