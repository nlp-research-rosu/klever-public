requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A direct executable statement of the contract: take the values at
  // positions 0,3,6,..., sort them, and weave them back into those positions.
  syntax Value ::= "contractResult" "(" Ints ")"
                     [function, symbol(contractResult)]
  rule contractResult(IS)
    => VList(replaceThirdInts(0 ; IS ; sortInts(thirds(IS))))
endmodule
