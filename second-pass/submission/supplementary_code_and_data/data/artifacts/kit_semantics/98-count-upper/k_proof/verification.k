requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Number of uppercase vowels at offsets 0, 2, 4, ... in a code sequence.
  syntax Int ::= countUpperEven(IntSeq) [function, total]
  rule countUpperEven(.IntSeq) => 0
  rule countUpperEven(CODES:IntSeq)
    => (#if strContains(
                  iCons(intSeqAt(CODES, 0), .IntSeq),
                  strToCodes("AEIOU"))
        #then 1 #else 0 #fi)
       +Int countUpperEven(
         buildIS(
           CODES,
           clampHi(2, isLen(CODES), 1),
           isLen(CODES),
           1))
    requires notBool (CODES ==K .IntSeq)
    [simplification]

  // Normalize the accumulator shape used by the loop invariant.
  rule (A:Int +Int B:Int) +Int C:Int
    => A +Int (B +Int C)
    [simplification]
endmodule
