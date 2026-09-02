requires "semantic.k"

module VERIFICATION
  imports MPY
  imports MAP-SYMBOLIC

  // Proof-only symbolic support.  The executable rules remain in MPY;
  // MAP-SYMBOLIC supplies map reasoning needed by reachability claims.
  rule { M:Map [ K <- V ] #Equals M [ K <- V' ] }
    => { V #Equals V' }
    [simplification]

  rule 0 <=Int lengthString(_S) => true [simplification]
  rule substrString(S, 0, lengthString(S)) => S [simplification]
endmodule
