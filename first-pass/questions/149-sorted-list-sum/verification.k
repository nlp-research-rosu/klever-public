// verification.k — sorted_list_sum on the UNIFIED semantics, TRAP-FREE
// (P149, W3 keyed-sort rung). solution.py is canonical verbatim: real
// lst.sort() (the trusted sortVS, now with the concrete str-element leg),
// the even-length append filter, and the REAL sorted(new_lst, key=len) —
// the SHARED opaque sortKeyVS with the len builtin as the key value. The
// is_even_len/keyed_sort helpers and their Call traps are GONE.

requires "../../reference/src/lemmas.k"

module SORTED-LIST-SUM-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // the even-length filter fold; guards spell the EXECUTED atoms (shared
  // seqLen echo under isStr + the pyMod parity compare)
  syntax ValSeq ::= evenFilt(ValSeq, ValSeq) [function, total]
  rule evenFilt(.ValSeq, R:ValSeq) => R [simplification]
  rule evenFilt(vCons(V:Val, T:ValSeq), R:ValSeq)
    => evenFilt(T, valSeqConcat(R, vCons(V, .ValSeq)))
    requires pyMod(isLen(codesProj(V)), 2) ==Int 0 [simplification]
  rule evenFilt(vCons(V:Val, T:ValSeq), R:ValSeq) => evenFilt(T, R)
    requires notBool (pyMod(isLen(codesProj(V)), 2) ==Int 0) [simplification]
endmodule
