// verification.k — summary for the encrypt proof, on the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module ENCRYPT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // encC(C) = rotate a lowercase letter down 4 within a-z (else unchanged).
  syntax Int ::= encC(Int) [function, total]
  rule encC(C:Int) => pyMod(C -Int 97 +Int 4, 26) +Int 97 requires C >=Int 97 andBool C <=Int 122 [simplification]
  rule encC(C:Int) => C requires notBool (C >=Int 97 andBool C <=Int 122) [simplification]

  syntax IntSeq ::= encMap(IntSeq) [function, total]
  rule encMap(.IntSeq) => .IntSeq [simplification]
  rule encMap(iCons(C:Int, S:IntSeq)) => iCons(encC(C), encMap(S)) [simplification]

endmodule
