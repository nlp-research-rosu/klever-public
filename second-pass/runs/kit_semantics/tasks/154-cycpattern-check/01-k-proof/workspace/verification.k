requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports BOOL
  imports INT

  // One source-level update rotation = rotation[1:] + c.
  syntax IntSeq ::= rotateWith(IntSeq, Int) [function, total]
  rule rotateWith(ROT:IntSeq, C:Int)
    => seqConcat(
         buildIS(
           ROT,
           clampHi(1, isLen(ROT), 1),
           isLen(ROT),
           1),
         iCons(C, .IntSeq))

  // Exact structural fold for the remaining loop iterator.  Each constructor
  // corresponds to one fixed-semantics execution of the loop body.
  syntax Bool ::= cycScan(IntSeq, IntSeq, IntSeq, Bool)
                  [function, total]
  rule cycScan(_A:IntSeq, .IntSeq, _ROT:IntSeq, FOUND:Bool)
    => FOUND
  rule cycScan(A:IntSeq, iCons(C:Int, REST:IntSeq), ROT:IntSeq, FOUND:Bool)
    => cycScan(
         A,
         REST,
         rotateWith(ROT, C),
         FOUND orBool strContains(rotateWith(ROT, C), A))

  syntax IntSeq ::= finalRotation(IntSeq, IntSeq) [function, total]
  rule finalRotation(.IntSeq, ROT:IntSeq) => ROT
  rule finalRotation(iCons(C:Int, REST:IntSeq), ROT:IntSeq)
    => finalRotation(REST, rotateWith(ROT, C))

  syntax IntSeq ::= finalChar(IntSeq, IntSeq) [function, total]
  rule finalChar(.IntSeq, CURRENT:IntSeq) => CURRENT
  rule finalChar(iCons(C:Int, REST:IntSeq), _CURRENT:IntSeq)
    => finalChar(REST, iCons(C, .IntSeq))

  // The HumanEval predicate: b itself is checked first, then all non-identity
  // left rotations.  For empty b, strContains(.IntSeq, A) is true.
  syntax Bool ::= cycPattern(IntSeq, IntSeq) [function, total]
  rule cycPattern(A:IntSeq, B:IntSeq)
    => cycScan(
         A,
         buildIS(B, 0, clampLo(isLen(B) +Int -1, 1), 1),
         B,
         strContains(B, A))
endmodule
