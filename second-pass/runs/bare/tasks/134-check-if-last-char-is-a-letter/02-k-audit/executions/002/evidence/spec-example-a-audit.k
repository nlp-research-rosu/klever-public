requires "verification.k"

module SPEC-EXAMPLE-A-AUDIT
  imports VERIFICATION
  claim <k> standaloneLastLetter("A") => true ... </k>
endmodule
