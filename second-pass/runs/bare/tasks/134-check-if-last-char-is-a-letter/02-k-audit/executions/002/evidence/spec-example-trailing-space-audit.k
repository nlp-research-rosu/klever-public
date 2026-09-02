requires "verification.k"

module SPEC-EXAMPLE-TRAILING-SPACE-AUDIT
  imports VERIFICATION
  claim <k> standaloneLastLetter("apple pi e ") => false ... </k>
endmodule
