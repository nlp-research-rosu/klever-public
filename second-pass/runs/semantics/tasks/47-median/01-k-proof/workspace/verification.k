requires "reference-semantics/semantics.k"

module MEDIAN-VERIFICATION
  imports MPY

  // `sortVS` is the supplied trusted ascending-permutation primitive.
  // Sorting preserves length; exposing that fact lets the prover relate the
  // program's `len(sorted(l))` to the input sequence used in the contract.
  rule vsLen(sortVS(VS:ValSeq)) => vsLen(VS) [simplification]

  // HumanEval exercises this task on integer lists.  This structural
  // predicate records that domain without unrolling an arbitrary sequence.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(_:Int, VS:ValSeq)) => allInts(VS)
  rule allInts(vCons(_:Val, _:ValSeq)) => false [owise]

  // The supplied `sortVS` is deliberately opaque to symbolic execution.
  // Name an in-bounds element of its integer result with an Int-sorted
  // symbol, preserving enough type information for `+` and `/ 2.0`.
  syntax Int ::= sortedIntAt(ValSeq, Int)
    [function, total, symbol(sortedIntAt), no-evaluators]
  rule valSeqAt(sortVS(VS:ValSeq), I:Int) => sortedIntAt(VS, I)
    requires allInts(VS)
     andBool I >=Int 0
     andBool I <Int vsLen(VS)
    [simplification]
endmodule
