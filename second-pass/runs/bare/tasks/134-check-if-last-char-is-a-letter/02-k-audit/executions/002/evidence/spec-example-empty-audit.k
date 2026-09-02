requires "verification.k"

module SPEC-EXAMPLE-EMPTY-AUDIT
  imports VERIFICATION
  claim <k> standaloneLastLetter("") => false ... </k>
endmodule
