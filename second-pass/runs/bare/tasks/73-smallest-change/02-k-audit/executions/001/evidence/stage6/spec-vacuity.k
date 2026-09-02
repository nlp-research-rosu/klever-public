requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of submitted example claim 3. The satisfying input
  // returns 0 in both Python implementations and in concrete K execution, so
  // changing finish(0) to finish(1) must leave an unmet result obligation.
  claim [mutated-example-3]:
      <k>
        run(#smallestChangeBody,
             ListItem(1) ListItem(2) ListItem(3)
             ListItem(2) ListItem(1),
             #smallestChangeBody)
        => finish(1)
      </k>
endmodule
