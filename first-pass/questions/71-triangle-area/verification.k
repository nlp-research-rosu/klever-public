// verification.k — triangle_area on the UNIFIED semantics, TRAP-FREE (P71).
// solution.py is canonical verbatim (one function, inline float chain); NO
// interceptions — the inline chain reduces through the shared float leaves to
// exactly heronV's composition; triangleAreaRes selects by the or-condition.

requires "../../reference/src/lemmas.k"

module TRIANGLE-AREA-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // heronV: the DEFINED composition of shared float primitives — s = divII(a+b+c,2)
  // (the NEW shared Int/Int true division), the product of differences via subF/mulF/intToF,
  // sqrt via powF(_, 0.5), and round(_, 2) via roundFN. Residue = the shared float.k leaves only.
  syntax Float ::= heronV(Int, Int, Int) [function, total, symbol(heronV)]
  rule heronV(A:Int, B:Int, C:Int)
    => roundFN(powF(mulF(mulF(mulF(divII(A +Int B +Int C, 2),
                subF(divII(A +Int B +Int C, 2), intToF(A))),
                subF(divII(A +Int B +Int C, 2), intToF(B))),
                subF(divII(A +Int B +Int C, 2), intToF(C))), 0.5), 2)
    [simplification]

  // result = the area if (a,b,c) is a valid triangle, else -1.
  syntax Val ::= triangleAreaRes(Int, Int, Int) [function]
  rule triangleAreaRes(A:Int, B:Int, C:Int) => heronV(A, B, C)
       requires notBool ((A +Int B <=Int C) orBool (A +Int C <=Int B) orBool (B +Int C <=Int A)) [simplification]
  rule triangleAreaRes(A:Int, B:Int, C:Int) => -1
       requires (A +Int B <=Int C) orBool (A +Int C <=Int B) orBool (B +Int C <=Int A) [simplification]
endmodule
