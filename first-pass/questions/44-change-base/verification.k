// verification.k — change_base on the UNIFIED semantics. Build the base-B digit string of x by the
// numeric while `while x>0: ret = str(x%base) + ret; x //= base` (base < 10, so every remainder is a
// single digit). solution.py is the canonical (docstring stripped).
//
// `str(x % base)` rides the REAL shared route; its symbolic leftover
// strToCodes(Int2String(..)) bridges to digitCodes by the SHARED lemma
// (str-int-decimal.k), and the single-digit unfold (0 <= x%base < base <= 10)
// discharges through the shared pyMod range facts (lemmas/arith.k). krun runs
// the real str (Int2String) on the shared semantics. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module CHANGE-BASE-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // str(x % base) rides the REAL shared route: its symbolic leftover bridges
  // to digitCodes (lemmas/str-int-decimal.k), whose single-digit unfold fires
  // under the shared pyMod range facts (lemmas/arith.k) with base <= 10

  // baseFold(X, B, RC) = the base-B digit CODES of X (most-significant first) prepended before RC —
  // exactly `ret` when the loop starts from (x=X, ret=str(RC)). The body prepends the current
  // least-significant digit code (48 + X%B) and recurses on X//B (the reference's pyMod-based % and
  // //). Threads RC like the body, so the circularity closes lemma-free. [total]: scope-map value.
  syntax IntSeq ::= baseFold(Int, Int, IntSeq) [function, total]
  rule baseFold(X:Int, _B:Int, RC:IntSeq) => RC requires X <=Int 0 [simplification]
  rule baseFold(X:Int, B:Int, RC:IntSeq)
    => baseFold((X -Int pyMod(X, B)) /Int B, B, iCons(48 +Int pyMod(X, B), RC))
    requires X >Int 0 [simplification]
endmodule
