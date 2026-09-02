requires "semantic.k"

module VERIFICATION
  imports MPY-SEMANTIC

  // The input domain from the HumanEval prompt.
  syntax Bool ::= "positiveInts" "(" IntSeq ")" [function, total]
  rule positiveInts(.Ints) => true
  rule positiveInts(cons(N, NS)) => (N >Int 0 andBool positiveInts(NS))

  // Contract-level vocabulary.  These equations say directly that an item is
  // retained iff its repeated base-10 quotient has no even remainder, that
  // every occurrence is retained, and that the retained sequence is sorted.
  syntax Bool ::= "allDecimalDigitsOdd" "(" Int ")" [function, total]
  rule allDecimalDigitsOdd(N) => oddDigits(N)

  syntax IntSeq ::= "retainAllOddDigitItems" "(" IntSeq ")"
                    [function, total]
  rule retainAllOddDigitItems(NS) => filterOddDigits(NS)

  syntax IntSeq ::= "inIncreasingOrder" "(" IntSeq ")" [function, total]
  rule inIncreasingOrder(NS) => sortInts(NS)

  syntax IntSeq ::= "uniqueDigitsSpec" "(" IntSeq ")" [function, total]
  rule uniqueDigitsSpec(NS)
    => inIncreasingOrder(retainAllOddDigitItems(NS))
endmodule
