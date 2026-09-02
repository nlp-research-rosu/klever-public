// verification.k — is_nested on the UNIFIED semantics. True iff a bracket string has >=2 nested
// brackets. The canonical builds two index lists + a greedy 2-pointer match; solution.py is a
// SINGLE-PASS rewrite over the string, tracking 6 scalars (open/close counts, first/second open
// positions, last/second-last close positions). KEY reduction (diff-tested 0/60013): the greedy loop
// matches a LEADING PREFIX (once open[k] >= close_rev[k] all later opens fail, opens ascend), so
// cnt >= 2 iff the first two opens beat the last two closes:
//   is_nested = num_opens>=2 and num_closes>=2 and first_open<last_close and second_open<second_last_close
//
// The per-char test `string[i] == '['` is intSeqAt(CS, I) ==Int 91 — a SYMBOLIC-Int compare that is
// CASE-SPLITTABLE (not opaque). The 6 scalars fold via a single nstate accumulator. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module IS-NESTED-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // the 6-scalar loop state: num_opens, num_closes, first_open, second_open, last_close, second_last_close.
  syntax NState ::= nstate(Int, Int, Int, Int, Int, Int)

  // nestFold(CS, I, N, S): fold the single-pass scan from I to N. Case-split on intSeqAt(CS,I)==91 each
  // step (case-splittable), and on num_opens for the first/second-open capture (guarded, primeAcc style).
  syntax NState ::= nestFold(IntSeq, Int, Int, NState) [function, total]
  rule nestFold(_CS:IntSeq, I:Int, N:Int, S:NState) => S requires I >=Int N [simplification]
  // '[' (char == 91): first open (no==0) -> no=1, fo=I
  rule nestFold(CS:IntSeq, I:Int, N:Int, nstate(NO:Int, NC:Int, _FO:Int, SO:Int, LC:Int, SLC:Int))
    => nestFold(CS, I +Int 1, N, nstate(1, NC, I, SO, LC, SLC))
    requires I <Int N andBool intSeqAt(CS, I) ==Int 91 andBool NO ==Int 0 [simplification]
  // '[' second open (no==1) -> no=2, so=I
  rule nestFold(CS:IntSeq, I:Int, N:Int, nstate(NO:Int, NC:Int, FO:Int, _SO:Int, LC:Int, SLC:Int))
    => nestFold(CS, I +Int 1, N, nstate(2, NC, FO, I, LC, SLC))
    requires I <Int N andBool intSeqAt(CS, I) ==Int 91 andBool NO ==Int 1 [simplification]
  // '[' later open (no>=2) -> no+=1, positions unchanged
  rule nestFold(CS:IntSeq, I:Int, N:Int, nstate(NO:Int, NC:Int, FO:Int, SO:Int, LC:Int, SLC:Int))
    => nestFold(CS, I +Int 1, N, nstate(NO +Int 1, NC, FO, SO, LC, SLC))
    requires I <Int N andBool intSeqAt(CS, I) ==Int 91 andBool NO >=Int 2 [simplification]
  // non-'[' (char =/= 91): nc+=1, slc=lc, lc=I
  rule nestFold(CS:IntSeq, I:Int, N:Int, nstate(NO:Int, NC:Int, FO:Int, SO:Int, LC:Int, _SLC:Int))
    => nestFold(CS, I +Int 1, N, nstate(NO, NC +Int 1, FO, SO, I, LC))
    requires I <Int N andBool notBool (intSeqAt(CS, I) ==Int 91) [simplification]

  // projections (the loop invariant threads the 6 scalars as separate store slots).
  syntax Int ::= nNo(NState) [function, total] | nNc(NState) [function, total]
               | nFo(NState) [function, total] | nSo(NState) [function, total]
               | nLc(NState) [function, total] | nSlc(NState) [function, total]
  rule nNo(nstate(NO:Int, _, _, _, _, _))  => NO
  rule nNc(nstate(_, NC:Int, _, _, _, _))  => NC
  rule nFo(nstate(_, _, FO:Int, _, _, _))  => FO
  rule nSo(nstate(_, _, _, SO:Int, _, _))  => SO
  rule nLc(nstate(_, _, _, _, LC:Int, _))  => LC
  rule nSlc(nstate(_, _, _, _, _, SLC:Int)) => SLC

  // the result: num_opens>=2 and num_closes>=2 and first_open<last_close and second_open<second_last_close.
  // isNestState(CS) = the final scan state; isNestedRes reads its 6 fields.
  syntax NState ::= isNestState(IntSeq) [function, total]
  rule isNestState(CS:IntSeq) => nestFold(CS, 0, isLen(CS), nstate(0, 0, -1, -1, -1, -1)) [simplification]

  syntax Bool ::= isNestedRes(IntSeq) [function]
  rule isNestedRes(CS:IntSeq)
    => nNo(isNestState(CS)) >=Int 2 andBool nNc(isNestState(CS)) >=Int 2
       andBool nFo(isNestState(CS)) <Int nLc(isNestState(CS))
       andBool nSo(isNestState(CS)) <Int nSlc(isNestState(CS)) [simplification]
endmodule
