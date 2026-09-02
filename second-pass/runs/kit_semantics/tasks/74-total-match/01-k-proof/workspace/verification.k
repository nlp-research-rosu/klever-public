requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The prompt's list-of-strings domain, unfolded one ValSeq constructor at a
  // time.  isStrV is supplied by the fixed semantics.
  syntax Bool ::= onlyStrings(ValSeq) [function, total]
  rule onlyStrings(.ValSeq) => true
  rule onlyStrings(vCons(V:Val, REST:ValSeq))
    => isStrV(V) andBool onlyStrings(REST)

  // A total projection used only under isStrV.  Its non-string case makes the
  // definition exhaustive but cannot affect a claim in the formal domain.
  syntax IntSeq ::= stringCodes(Val) [function, total]
  rule stringCodes(str(CS:IntSeq)) => CS
  rule stringCodes(_V:Val) => .IntSeq [owise]

  // This is the reference rule seqLen(str(CS)) => isLen(CS), generalized under
  // the exact fixed-semantics string recognizer.
  rule seqLen(V:Val) => isLen(stringCodes(V))
    requires isStrV(V)
    [simplification]

  // A left-fold summary that exactly follows the program's accumulator update.
  syntax Int ::= totalLen(ValSeq) [function, total]
               | totalLenFrom(Int, ValSeq) [function, total]
  rule totalLen(ITEMS:ValSeq) => totalLenFrom(0, ITEMS)
  rule totalLenFrom(ACC:Int, .ValSeq) => ACC
  rule totalLenFrom(ACC:Int, vCons(V:Val, REST:ValSeq))
    => totalLenFrom(ACC +Int isLen(stringCodes(V)), REST)

  // The exact final value left in a Python for-loop target.
  syntax Val ::= lastLoopValue(ValSeq, Val) [function, total]
  rule lastLoopValue(.ValSeq, OLD:Val) => OLD
  rule lastLoopValue(vCons(V:Val, REST:ValSeq), _OLD:Val)
    => lastLoopValue(REST, V)
endmodule
