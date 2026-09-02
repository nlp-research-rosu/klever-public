requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // True exactly when every member of the native ValSeq is a Float.
  syntax Bool ::= allFloats(ValSeq) [function, total]
  rule allFloats(.ValSeq)           => true
  rule allFloats(vCons(V:Val, R))   => isFloat(V) andBool allFloats(R)

  // The exact opaque float atom evaluated by the Python program.
  syntax Bool ::= pairNear(Float, Float, Float) [function, total]
  rule pairNear(A, B, T) => floatLt(absF(subF(A, B)), T)

  syntax Float ::= asFloat(Val) [function, total]
  rule asFloat(F:Float) => F
  rule asFloat(V:Val)   => 0.0
    requires notBool isFloat(V)

  // Derived sort-elimination lemma for the fixed Float subtraction dispatch.
  rule applyBin("-", A:Val, B:Val) => subF(asFloat(A), asFloat(B))
    requires isFloat(A) andBool isFloat(B)
    [simplification]

  // Final accumulator after scanning REM with positions J, J+1, ...
  syntax Bool ::= rowAcc(Bool, Float, Float, Int, Int, ValSeq)
                  [function, total]
  rule rowAcc(B, _, _, _, _, .ValSeq) => B
  rule rowAcc(B, A, T, I, J, vCons(V:Val, R))
    => rowAcc(
         #if I <Int J
         #then B orBool pairNear(A, asFloat(V), T)
         #else B
         #fi,
         A, T, I, J +Int 1, R)

  // Final accumulator after scanning outer REM with positions I, I+1, ...
  syntax Bool ::= outerAcc(Bool, ValSeq, Float, Int, ValSeq)
                  [function, total]
  rule outerAcc(B, _, _, _, .ValSeq) => B
  rule outerAcc(B, VS, T, I, vCons(A:Val, R))
    => outerAcc(rowAcc(B, asFloat(A), T, I, 0, VS),
                VS, T, I +Int 1, R)
endmodule
