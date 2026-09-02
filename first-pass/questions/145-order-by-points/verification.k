// verification.k — order_by_points on the UNIFIED semantics, TRAP-FREE
// (P145, W3 keyed-sort rung). solution.py is canonical verbatim: the nested
// digits_sum def and the REAL sorted(nums, key=digits_sum). The keyed sort is
// the SHARED trusted sortKeyVS (semantics/sort.k): opaque for kprove with the
// key CLOSURE VALUE inside the atom; krun computes keys by real calls. The
// old keyed_sort Call trap and the manual insertion-sort rewrite are GONE.

requires "../../reference/src/lemmas.k"

module ORDER-BY-POINTS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val
endmodule
