requires "semantic.k"

module MAXIMUM-VERIFICATION
  imports MAXIMUM

  // Mathematical contract: sorting the full input and dropping all but its
  // final K values yields exactly the sorted multiset of the K largest values.
  syntax List ::= "maximumSpec" "(" List "," Int ")" [function]
  rule maximumSpec(L:List, K:Int)
    => dropInts(size(L) -Int K, sortInts(L))
endmodule
