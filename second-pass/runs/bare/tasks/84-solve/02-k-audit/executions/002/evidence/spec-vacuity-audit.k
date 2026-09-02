requires "semantic.k"

module SPEC-VACUITY-AUDIT
  imports SEMANTIC

  // Fresh auditor mutation: the original computation is true for the
  // satisfying concrete input 10000, so requiring false must be rejected.
  claim [false-result-10000]:
    <k> checkRange(10000, 10001) => false </k>
endmodule
