requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Tail-recursive specification of filtering the remaining input codes,
  // starting from the codes already accumulated by the Python loop.
  syntax IntSeq ::= removeVowelsFrom(IntSeq, IntSeq) [function, total]

  rule removeVowelsFrom(.IntSeq, ACC:IntSeq) => ACC

  rule removeVowelsFrom(iCons(C:Int, REST:IntSeq), ACC:IntSeq)
    => removeVowelsFrom(REST, ACC)
    requires strContains(
      iCons(C, .IntSeq),
      iCons(97,
        iCons(101,
          iCons(105,
            iCons(111,
              iCons(117,
                iCons(65,
                  iCons(69,
                    iCons(73,
                      iCons(79,
                        iCons(85, .IntSeq)))))))))))
    [simplification]

  rule removeVowelsFrom(iCons(C:Int, REST:IntSeq), ACC:IntSeq)
    => removeVowelsFrom(
         REST,
         seqConcat(ACC, iCons(C, .IntSeq)))
    requires notBool strContains(
      iCons(C, .IntSeq),
      iCons(97,
        iCons(101,
          iCons(105,
            iCons(111,
              iCons(117,
                iCons(65,
                  iCons(69,
                    iCons(73,
                      iCons(79,
                        iCons(85, .IntSeq)))))))))))
    [simplification]
endmodule
