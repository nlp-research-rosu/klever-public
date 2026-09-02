requires "solution-program.k"

module VERIFICATION
  imports MPY
  imports SOLUTION-PROGRAM

  // A finite mathematical characterization of the contract.  Each disjunct
  // is p*q*r for one nondecreasing prime triple p<=q<=r whose product is below
  // 100.  Ordering loses nothing because multiplication is commutative.
  syntax Bool ::= isThreePrimeProductBelow100(Int) [function]
  rule isThreePrimeProductBelow100(A) =>
       A ==Int (2 *Int 2 *Int 2)
    orBool A ==Int (2 *Int 2 *Int 3)
    orBool A ==Int (2 *Int 3 *Int 3)
    orBool A ==Int (2 *Int 2 *Int 5)
    orBool A ==Int (3 *Int 3 *Int 3)
    orBool A ==Int (2 *Int 2 *Int 7)
    orBool A ==Int (2 *Int 3 *Int 5)
    orBool A ==Int (2 *Int 3 *Int 7)
    orBool A ==Int (2 *Int 2 *Int 11)
    orBool A ==Int (3 *Int 3 *Int 5)
    orBool A ==Int (2 *Int 5 *Int 5)
    orBool A ==Int (2 *Int 2 *Int 13)
    orBool A ==Int (3 *Int 3 *Int 7)
    orBool A ==Int (2 *Int 3 *Int 11)
    orBool A ==Int (2 *Int 2 *Int 17)
    orBool A ==Int (2 *Int 5 *Int 7)
    orBool A ==Int (3 *Int 5 *Int 5)
    orBool A ==Int (2 *Int 2 *Int 19)
    orBool A ==Int (2 *Int 3 *Int 13)
    orBool A ==Int (2 *Int 2 *Int 23)
    orBool A ==Int (2 *Int 7 *Int 7)
    orBool A ==Int (3 *Int 3 *Int 11)
    [simplification]
endmodule
