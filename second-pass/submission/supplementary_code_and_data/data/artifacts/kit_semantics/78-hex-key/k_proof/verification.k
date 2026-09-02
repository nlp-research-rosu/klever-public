requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical count of one-character strings that occur in "2357BD".
  syntax Int ::= hexCount(IntSeq) [function, total]

  rule hexCount(.IntSeq) => 0
  rule hexCount(iCons(C:Int, CS:IntSeq))
    => (#if strContains(iCons(C, .IntSeq), strToCodes("2357BD"))
        #then 1
        #else 0
        #fi) +Int hexCount(CS)
endmodule
