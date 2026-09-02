requires "verification.k"

module SPEC-STRING-LENGTH-ONE
  imports VERIFICATION

  claim [emoji-length-one]:
    <k> lengthString("\U0001f642") => 1 </k>
endmodule
