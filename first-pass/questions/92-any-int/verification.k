// verification.k — proof scaffolding: a symbolic-input subsort. The spec is the
// closed boolean form (orBool of the three pairwise-sum equalities) directly —
// any_int has no loop, so there is no recursive summary function to define.
// See ../../NOTES.md. On the UNIFIED semantics.

requires "../../reference/src/lemmas.k"

module ANY-INT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  // proof-only: let a Val sit in expression position (so symbolic Ints are args).
  syntax Expr ::= Val
endmodule
