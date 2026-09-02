requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // The source contract's material domain: arbitrary finite lists whose
  // elements are Python integers or floats.
  syntax Bool ::= numericVal(Val) [function, total]
  rule numericVal(V) => isInt(V) orBool isFloat(V)

  syntax Bool ::= numericVals(ValSeq) [function, total]
  rule numericVals(.ValSeq) => true
  rule numericVals(vCons(V, REST))
    => numericVal(V) andBool numericVals(REST)

  // A total mathematical predicate.  On the numeric domain its two
  // sort-disjoint equations are exactly MPY's `applyCmp(">", _, 0.0)` cases.
  syntax Bool ::= positiveNumeric(Val) [function, total]
  rule positiveNumeric(I:Int) => gtF(intToF(I), 0.0)
  rule positiveNumeric(F:Float) => gtF(F, 0.0)
  rule positiveNumeric(V:Val) => false
    requires notBool numericVal(V)

  // Exact accumulator-style filtering summary.  Its guards are the same
  // positivity atoms reached by MPY execution of `x > 0`.
  syntax ValSeq ::= filterPositive(ValSeq, ValSeq) [function, total]
  rule filterPositive(ACC, .ValSeq) => ACC [simplification]
  rule filterPositive(ACC, vCons(V, REST))
    => filterPositive(valSeqConcat(ACC, vCons(V, .ValSeq)), REST)
    requires positiveNumeric(V)
    [simplification]
  rule filterPositive(ACC, vCons(V, REST))
    => filterPositive(ACC, REST)
    requires notBool positiveNumeric(V)
    [simplification]
endmodule

module VERIFICATION
  imports VERIFICATION-BASE

  // Guarded dynamic-sort dispatch twin.  Its complete domain is numeric
  // values compared with the float literal zero.
  rule applyCmp(">", V:Val, 0.0) => positiveNumeric(V)
    requires numericVal(V)
    [simplification]
endmodule
