requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical reference result: the balance must never become negative,
  // and it must be zero when the input is exhausted.  The prompt promises
  // only '(' and ')' inputs; treating every non-'(' code as ')' merely makes
  // the oracle total outside that promised domain.
  syntax Bool ::= correctCodes(IntSeq, Int) [function, total]
  rule correctCodes(.IntSeq, B:Int) => B ==Int 0
  rule correctCodes(iCons(C:Int, R:IntSeq), B:Int)
    => #if C ==Int 40
       #then correctCodes(R, B +Int 1)
       #else #if B ==Int 0
             #then false
             #else correctCodes(R, B -Int 1)
             #fi
       #fi
endmodule
