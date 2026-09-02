requires "semantic.k"

module VERIFICATION
  imports MPY

  // Independent recursive contract used only on the right-hand side of proof
  // claims: retain every input integer and put D between adjacent elements.
  syntax Ints ::= intersperseSpec(Ints, Int) [function, total]
  rule intersperseSpec(.Ints, _D) => .Ints
  rule intersperseSpec(I, .Ints, _D) => I, .Ints
  rule intersperseSpec(I, J, REST, D)
    => I, D, intersperseSpec(J, REST, D)
endmodule
