requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The code emitted for one source character by solution.py.
  syntax Int ::= rot4Code(Int) [function, total]
  rule rot4Code(C)
    => pyMod(C -Int 97 +Int 4, 26) +Int 97

  // A source character outside the lowercase alphabet passes through.
  syntax IntSeq ::= encryptedChar(Int) [function, total]
  rule encryptedChar(C) => iCons(C, .IntSeq)
    requires C <Int 97
  rule encryptedChar(C) => iCons(rot4Code(C), .IntSeq)
    requires 97 <=Int C andBool C <=Int 122
  rule encryptedChar(C) => iCons(C, .IntSeq)
    requires C >Int 122

  // Tail-recursive left fold matching the program's `out += ...` updates.
  syntax IntSeq ::= encryptFold(IntSeq, IntSeq) [function, total]
  rule encryptFold(A, .IntSeq) => A
  rule encryptFold(A, iCons(C, R))
    => encryptFold(
         seqConcat(A, encryptedChar(C)),
         R)

  syntax IntSeq ::= encryptResult(IntSeq) [function, total]
  rule encryptResult(S) => encryptFold(.IntSeq, S)

  // Python leaves the for-target bound to its last value, if there is one.
  syntax Val ::= finalLoopChar(IntSeq, Val) [function, total]
  rule finalLoopChar(.IntSeq, V) => V
  rule finalLoopChar(iCons(C, R), _V)
    => finalLoopChar(R, str(iCons(C, .IntSeq)))
endmodule
