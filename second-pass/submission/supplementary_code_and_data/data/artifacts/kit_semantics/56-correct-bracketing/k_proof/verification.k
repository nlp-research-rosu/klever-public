requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Net change in balance caused by a suffix.  The implementation treats
  // every non-"<" character as a closing bracket, so the second step case
  // faithfully covers the complete Int code domain.
  syntax Int ::= bracketDelta(IntSeq) [function, total]
  rule bracketDelta(.IntSeq) => 0
  rule bracketDelta(iCons(C:Int, REST:IntSeq))
    => (#if C ==Int 60 #then 1 #else 0 -Int 1 #fi)
       +Int bracketDelta(REST)

  // True exactly when every balance observed after consuming a character in
  // the suffix is nonnegative, starting from BAL.
  syntax Bool ::= bracketPrefixOK(IntSeq, Int) [function, total]
  rule bracketPrefixOK(.IntSeq, _BAL:Int) => true
  rule bracketPrefixOK(iCons(C:Int, REST:IntSeq), BAL:Int)
    => #if C ==Int 60
       #then (BAL +Int 1 >=Int 0)
             andBool bracketPrefixOK(REST, BAL +Int 1)
       #else (BAL -Int 1 >=Int 0)
             andBool bracketPrefixOK(REST, BAL -Int 1)
       #fi

  // The HumanEval input domain: strings consist only of "<" and ">".
  syntax Bool ::= bracketChars(IntSeq) [function, total]
  rule bracketChars(.IntSeq) => true
  rule bracketChars(iCons(C:Int, REST:IntSeq))
    => (C ==Int 60 orBool C ==Int 62) andBool bracketChars(REST)

  syntax Bool ::= bracketCorrect(IntSeq) [function, total]
  rule bracketCorrect(CODES:IntSeq)
    => bracketPrefixOK(CODES, 0)
       andBool bracketDelta(CODES) ==Int 0
endmodule
