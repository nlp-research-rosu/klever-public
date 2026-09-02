requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The filtered suffix appended to an already-built result.
  syntax IntSeq ::= deleteAcc(IntSeq, IntSeq, IntSeq) [function, total]
  rule deleteAcc(.IntSeq, _:IntSeq, ACC:IntSeq) => ACC
  rule deleteAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, ACC:IntSeq)
    => #if strContains(iCons(X, .IntSeq), C)
       #then deleteAcc(XS, C, ACC)
       #else deleteAcc(XS, C, seqConcat(ACC, iCons(X, .IntSeq)))
       #fi

  // The filtered suffix prepended, one character at a time, to a reverse
  // accumulator.  With an empty accumulator this is the reverse of deleteAcc.
  syntax IntSeq ::= reverseDeleteAcc(IntSeq, IntSeq, IntSeq)
                    [function, total]
  rule reverseDeleteAcc(.IntSeq, _:IntSeq, ACC:IntSeq) => ACC
  rule reverseDeleteAcc(iCons(X:Int, XS:IntSeq), C:IntSeq, ACC:IntSeq)
    => #if strContains(iCons(X, .IntSeq), C)
       #then reverseDeleteAcc(XS, C, ACC)
       #else reverseDeleteAcc(XS, C, iCons(X, ACC))
       #fi
endmodule
