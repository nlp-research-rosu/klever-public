// verification.k — sort_array on the UNIFIED semantics, TRAP-FREE (W3 P116).
// solution.py is canonical verbatim; both sorts are the SHARED opaques
// (sortVS + sortKeyVS with the ones-count lambda inside the atom); the
// keyed_sort helper and its Call trap are GONE. No problem-local kit needed.

requires "../../reference/src/lemmas.k"

module SORT-ARRAY-BIN-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val
endmodule
