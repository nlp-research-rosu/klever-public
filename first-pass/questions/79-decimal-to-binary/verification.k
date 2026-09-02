// verification.k — decimal_to_binary on the UNIFIED semantics, TRAP-FREE
// (P79). solution.py is canonical verbatim: "db" + bin(decimal)[2:] + "db".
// The shared bin() builtin produces str(iCons(48, iCons(98, binCodes(N))));
// the [2:] slice (sliceIS operator interception) drops the two concrete
// prefix codes and leaves the opaque binCodes(N).

requires "../../reference/src/lemmas.k"

module DECIMAL-TO-BINARY-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // bin(decimal)[2:] rides the REAL doSlice/buildIS route; the SHARED slice
  // lemmas (lemmas/subscript.k, lemmas/str.k) reduce it to binCodes(decimal)

  syntax Val ::= d2bRes(Int) [function]
  rule d2bRes(N:Int)
    => str(seqConcat(iCons(100, iCons(98, .IntSeq)),
            seqConcat(binCodes(N), iCons(100, iCons(98, .IntSeq)))))
    [simplification]
endmodule
