requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false result mutation of submitted claim 3. The realizable input
  // is numbers = [] and threshold = 0; both Python functions and concrete K
  // execution return false, so the mutated true obligation must be rejected.
  claim <k> verify(VList(.PValues), VInt(0)) => VBool(true) </k>
endmodule
