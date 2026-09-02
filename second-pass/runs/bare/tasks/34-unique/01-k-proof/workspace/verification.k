requires "semantic.k"

module VERIFICATION
  imports MPY

  // The contract as a separately named reference function: eliminate repeated
  // integers and order the representatives increasingly.
  syntax List ::= uniqueSpec(List) [function]
  rule uniqueSpec(L) => sortInts(dedupInts(L))
endmodule
