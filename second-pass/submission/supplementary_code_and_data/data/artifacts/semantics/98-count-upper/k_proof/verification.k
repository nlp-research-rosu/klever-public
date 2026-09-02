requires "reference-semantics/semantics.k"

module COUNT-UPPER-VERIFICATION
  imports MPY

  // Mathematical result for scanning the remaining character codes.  The
  // Boolean records whether the next character has an even original index.
  syntax Int ::= countUpperFrom(IntSeq, Bool) [function, total]

  rule countUpperFrom(.IntSeq, _:Bool) => 0
  rule countUpperFrom(iCons(C:Int, REST:IntSeq), EVEN:Bool)
    => (#if EVEN andBool strContains(
                       iCons(C, .IntSeq),
                       strToCodes("AEIOU"))
        #then 1 #else 0 #fi)
       +Int countUpperFrom(REST, notBool EVEN)
endmodule
