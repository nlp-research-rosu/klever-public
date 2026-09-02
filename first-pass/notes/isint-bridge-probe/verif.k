// verif.k — probe: can a guarded applyBin/applyCmp ECHO reduce arithmetic on two symbolic
// SAME-LIST elements (valSeqAt(NUMS,I), valSeqAt(NUMS,J)) under an allInt(NUMS) precondition?
// This is the isInt wall that blocks element-based nested loops (Q43/Q40/Q20/Q87). isInt cannot
// be a [simplification] LHS (hooked predicate), so we cannot say isInt(valSeqAt(..)) => true.
// Instead echo applyBin/applyCmp (function symbols, OK as LHS) directly, casting via {}:>Int
// under the allInt guard (SOUND: allInt(NUMS) => every element IS an Int, so the projection is
// faithful). If this fires, the existing Int-arith rules take over.

requires "../../src/lemmas.k"

module ISINT-PROBE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // candidate echo — same-list elements under allInt
  rule applyBin(OP:String, valSeqAt(NUMS:ValSeq, I:Int), valSeqAt(NUMS:ValSeq, J:Int))
    => applyBin(OP, {valSeqAt(NUMS, I)}:>Int, {valSeqAt(NUMS, J)}:>Int)
    requires allInt(NUMS)
    [simplification]

  rule applyCmp(OP:String, valSeqAt(NUMS:ValSeq, I:Int), valSeqAt(NUMS:ValSeq, J:Int))
    => applyCmp(OP, {valSeqAt(NUMS, I)}:>Int, {valSeqAt(NUMS, J)}:>Int)
    requires allInt(NUMS)
    [simplification]
endmodule
