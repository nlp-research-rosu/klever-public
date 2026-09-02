requires "verification.k"

module SPEC-STRING-LENGTH-FOUR
  imports VERIFICATION

  claim [emoji-length-four]:
    <k> lengthString("\U0001f642") => 4 </k>
endmodule
