// verification.k — circular_shift on the UNIFIED semantics, TRAP-FREE (P65).
// solution.py is canonical verbatim (one function; real str/len/slices).
// All bridges are SHARED lemmas: str(symbolic int) -> digitCodes
// (lemmas/str-int-decimal.k) and the three slice forms ride the REAL
// doSlice/buildIS route reshaped to take/drop/rev (lemmas/subscript.k +
// the minus-minus cancellation in lemmas/arith.k).

requires "../../reference/src/lemmas.k"

module CIRCULAR-SHIFT-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // digitCodes, takeIS, dropIS, revIS are all SHARED (lemmas/str-int-decimal.k,
  // lemmas/subscript.k, semantics/methods.k)

  // ---- the result summary: reverse if shift > len, else rotate
  syntax Val ::= circShiftRes(Int, Int) [function]
  rule circShiftRes(X:Int, SHIFT:Int) => str(revIS(digitCodes(X)))
    requires SHIFT >Int isLen(digitCodes(X)) [simplification]
  // the suffix spells as the executed take-after-drop (the forward reshape's
  // count cancels to SHIFT by the shared minus-minus lemma)
  rule circShiftRes(X:Int, SHIFT:Int)
    => str(seqConcat(takeIS(dropIS(digitCodes(X), isLen(digitCodes(X)) -Int SHIFT), SHIFT),
                     takeIS(digitCodes(X), isLen(digitCodes(X)) -Int SHIFT)))
    requires SHIFT <=Int isLen(digitCodes(X)) [simplification]
endmodule
