requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Declarative contract: after duplicate elimination and ascending sort,
  // return position 1 when present, and Python None otherwise.
  syntax PyVal ::= "secondSmallest" "(" IntList ")" [function, total]
  rule secondSmallest(L)
    => iteVal(lenInt(uniqueSort(L)) >Int 1,
              itemAt(uniqueSort(L), 1),
              none)
endmodule
