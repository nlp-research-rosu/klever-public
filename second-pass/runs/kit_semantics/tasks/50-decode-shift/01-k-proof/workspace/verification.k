requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX

  syntax Int ::= decodeCode(Int) [function, total]
  syntax Int ::= encodeCode(Int) [function, total]
  syntax IntSeq ::= decodeAcc(IntSeq, IntSeq) [function, total]
  syntax Bool ::= lowerCodes(IntSeq) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  // The inverse Caesar shift on one character code.
  rule decodeCode(C:Int) => pyMod(C -Int 102, 26) +Int 97

  // The prompt's forward Caesar shift, stated independently for adequacy.
  rule encodeCode(C:Int) => pyMod(C -Int 92, 26) +Int 97

  // Tail-recursive mathematical summary matching the source accumulator.
  rule decodeAcc(.IntSeq, ACC:IntSeq) => ACC
  rule decodeAcc(iCons(C:Int, REST:IntSeq), ACC:IntSeq)
    => decodeAcc(REST, seqConcat(ACC, iCons(decodeCode(C), .IntSeq)))

  // Domain predicate: every input code is a lowercase ASCII letter.
  rule lowerCodes(.IntSeq) => true
  rule lowerCodes(iCons(C:Int, REST:IntSeq))
    => (97 <=Int C andBool C <=Int 122) andBool lowerCodes(REST)
endmodule
