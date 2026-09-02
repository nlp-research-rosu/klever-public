// verification.k — summary for the hex_key proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module HEX-KEY-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // isPrimeHex(C): C is a prime hex digit — '2' '3' '5' '7' 'B' 'D' (codes 50 51 53 55 66 68).
  syntax Bool ::= isPrimeHex(Int) [function, total]
  rule isPrimeHex(C:Int)
    => C ==Int 50 orBool C ==Int 51 orBool C ==Int 53 orBool C ==Int 55 orBool C ==Int 66 orBool C ==Int 68
    [simplification]

  // countPH(CS): number of prime-hex-digit codes.
  syntax Int ::= countPH(IntSeq) [function, total]
  rule countPH(.IntSeq) => 0 [simplification]
  rule countPH(iCons(C:Int, S:IntSeq)) => 1 +Int countPH(S) requires isPrimeHex(C)       [simplification]
  rule countPH(iCons(C:Int, S:IntSeq)) =>       countPH(S) requires notBool isPrimeHex(C) [simplification]
endmodule
