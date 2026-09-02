// verification.k — summary for the filter_by_substring proof, on the UNIFIED semantics.
// List-of-strings filter by substring containment; reuses the codesProj Str projection
// ([[list-of-strings-proj]]) and the reference substring `in` (strContains).

requires "../../reference/src/lemmas.k"

module FILTER-BY-SUBSTRING-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // substring `in` on a symbolic str element bridges through codesProj.
  rule applyCmp("in", str(SC:IntSeq), V:Val)
    => strContains(SC, codesProj(V)) requires isStr(V) [simplification]

  // filterSub(SC, VS) = the order-preserving sublist of VS containing substring SC.
  syntax ValSeq ::= filterSub(IntSeq, ValSeq) [function, total]
  rule filterSub(_:IntSeq, .ValSeq) => .ValSeq [simplification]
  rule filterSub(SC:IntSeq, vCons(V:Val, VS:ValSeq))
    => vCons(V, filterSub(SC, VS)) requires strContains(SC, codesProj(V))         [simplification]
  rule filterSub(SC:IntSeq, vCons(V:Val, VS:ValSeq))
    =>            filterSub(SC, VS)  requires notBool strContains(SC, codesProj(V)) [simplification]

endmodule
