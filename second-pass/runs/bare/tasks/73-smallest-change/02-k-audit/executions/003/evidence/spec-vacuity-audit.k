requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the trusted implementations return 4 for this
  // documented input, while this mutation requires finish(5).
  claim [false-example-result]:
        <k>
          run(#smallestChangeBody,
               ListItem(1) ListItem(2) ListItem(3) ListItem(5)
               ListItem(4) ListItem(7) ListItem(9) ListItem(6),
               #smallestChangeBody)
          => finish(5)
        </k>
endmodule
