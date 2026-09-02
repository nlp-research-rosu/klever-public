// verification.k — string_sequence on the UNIFIED semantics. `' '.join([str(x) for x in range(n+1)])`
// = "0 1 2 ... n". The str-of-symbolic-int wall (`str(x)` for x possibly >= 10 in the RETURNED string):
// solution.py rewrites the comprehension+join as an explicit range-loop building the string
// (`result = str(0)`, then `result = result + ' ' + str(x)` for x in 1..n). Diff-tested 0/20009.
//
// The construct: the SHARED multi-digit model `digitCodes(N)` (lemmas/
// str-int-decimal.k) = the decimal digit char codes of a non-negative Int,
// OPAQUE for kprove on a symbolic x and CONCRETE for krun. str(x) rides the
// REAL shared route; its symbolic leftover strToCodes(Int2String(x)) bridges
// to digitCodes(x) by the shared lemma (x >= 0 here from the range PC).
// See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module STRING-SEQUENCE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // seqFold(K, HI, RC) = RC with " " + digitCodes(x) appended for each x in [K, HI): the code sequence
  // the range-loop builds. [total]: it lands in the result scope during the fold.
  syntax IntSeq ::= seqFold(Int, Int, IntSeq) [function, total]
  rule seqFold(K:Int, HI:Int, RC:IntSeq) => RC requires K >=Int HI [simplification]
  rule seqFold(K:Int, HI:Int, RC:IntSeq)
    => seqFold(K +Int 1, HI, seqConcat(seqConcat(RC, iCons(32, .IntSeq)), digitCodes(K)))
    requires K <Int HI [simplification]

  // result = "0 1 2 ... n": start from str(0) = str([48]), then append " " + str(x) for x in 1..n.
  syntax Val ::= strSeqRes(Int) [function]
  rule strSeqRes(N:Int) => str(seqFold(1, N +Int 1, iCons(48, .IntSeq))) [simplification]
endmodule
