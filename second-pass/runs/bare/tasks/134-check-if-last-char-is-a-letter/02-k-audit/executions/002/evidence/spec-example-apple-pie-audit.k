requires "verification.k"

module SPEC-EXAMPLE-APPLE-PIE-AUDIT
  imports VERIFICATION
  claim <k> standaloneLastLetter("apple pie") => false ... </k>
endmodule
