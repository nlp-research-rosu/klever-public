requires "verification.k"

module BRIDGE-FREE-SYMBOLIC
  imports MAX-FILL-DATA

  // Deliberately declare an opaque symbolic sequence without the candidate's
  // operational bridge, so fixed-semantics behavior can be observed.
  syntax ValSeq ::= symRowBF(IntSeq)
endmodule
