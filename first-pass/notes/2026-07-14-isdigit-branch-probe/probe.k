// probe.k — what does an If on the isdigit composite leave in the TRUE
// branch's PC? P124's isdigit-all-true branch carries dgN(F)==1 atoms but
// NOT the notBool(isLen(F)==0) halves the shared echo emits — the
// dg-composite guards can't fire. #pbS advances only when its Bool is
// ENTAILED (k-cell guards entailment-gate), so a green probe means the
// branch assertion keeps both halves; a stuck probe reproduces P124.

requires "../../src/lemmas.k"

module ISDIGIT-BRANCH-PROBE
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Stmt ::= #pbS(Bool)
  rule <k> #pbS(B:Bool) => .K ... </k>
    requires B
endmodule
