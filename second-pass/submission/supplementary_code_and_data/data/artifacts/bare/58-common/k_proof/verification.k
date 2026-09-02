requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Mathematical contract: convert each input to a finite integer set,
  // intersect the sets, then put the elements in ascending order.
  syntax Ints ::= "commonSpec" "(" Ints ";" Ints ")" [function]
  rule commonSpec(IS ; JS)
    => sortInts(intersectInts(uniqueInts(IS) ; uniqueInts(JS)))
endmodule
