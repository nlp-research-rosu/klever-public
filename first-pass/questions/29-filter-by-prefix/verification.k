// verification.k — summary for the filter_by_prefix proof, on the UNIFIED semantics.
// List-of-strings filter by a string prefix; reuses the codesProj Str projection
// ([[list-of-strings-proj]]) and the reference .startswith method (startsWith).

requires "../../reference/src/lemmas.k"

module FILTER-BY-PREFIX-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // .startswith on a symbolic str element bridges through codesProj.
  rule applyMethod(V:Val, "startswith", str(PC:IntSeq), .Vals)
    => startsWith(PC, codesProj(V)) requires isStr(V) [simplification]

  // filterPrefix(PC, VS) = the sublist of VS whose elements start with prefix PC.
  syntax ValSeq ::= filterPrefix(IntSeq, ValSeq) [function, total]
  rule filterPrefix(_:IntSeq, .ValSeq) => .ValSeq [simplification]
  rule filterPrefix(PC:IntSeq, vCons(V:Val, VS:ValSeq))
    => vCons(V, filterPrefix(PC, VS)) requires startsWith(PC, codesProj(V))         [simplification]
  rule filterPrefix(PC:IntSeq, vCons(V:Val, VS:ValSeq))
    =>            filterPrefix(PC, VS)  requires notBool startsWith(PC, codesProj(V)) [simplification]

  // Left-built accumulator lemmas.
endmodule
