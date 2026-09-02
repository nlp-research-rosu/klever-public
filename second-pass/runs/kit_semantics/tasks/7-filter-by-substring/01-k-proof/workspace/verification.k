requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports BOOL

  // The source annotation is List[str].  This predicate states that domain
  // over the semantics' heterogeneous ValSeq representation.
  // A total projection makes string-ness solver-visible: V is a semantic
  // string exactly when V ==K str(strCodes(V)).
  syntax IntSeq ::= strCodes(Val) [function, total]
  rule strCodes(str(S:IntSeq)) => S
  rule strCodes(_:Val)         => .IntSeq [owise]

  syntax Bool ::= allStrVS(ValSeq) [function, total]
  rule allStrVS(.ValSeq) => true
  rule allStrVS(vCons(V:Val, R:ValSeq))
    => (V ==K str(strCodes(V))) andBool allStrVS(R)

  // Constraint-normalization lemma.  Its guard states that the old and new
  // right operands are exactly equal; MPY-STR's fixed rule still evaluates
  // the resulting applyCmp term.
  rule applyCmp("in", str(P:IntSeq), V:Val)
    => applyCmp("in", str(P), str(strCodes(V)))
    requires V ==K str(strCodes(V))
    [simplification]

  // Mathematical filter summary in accumulator form.  Its equations cover
  // every allStrVS input; no equation is asserted for out-of-domain heads.
  syntax ValSeq ::= filterAcc(ValSeq, IntSeq, ValSeq) [function]
  rule filterAcc(A:ValSeq, _:IntSeq, .ValSeq) => A
  rule filterAcc(A:ValSeq, P:IntSeq, vCons(V:Val, R:ValSeq))
    => filterAcc(
         valSeqConcat(A, vCons(V, .ValSeq)),
         P,
         R)
    requires V ==K str(strCodes(V))
      andBool strContains(P, strCodes(V))
    [simplification]
  rule filterAcc(A:ValSeq, P:IntSeq, vCons(V:Val, R:ValSeq))
    => filterAcc(A, P, R)
    requires V ==K str(strCodes(V))
      andBool notBool strContains(P, strCodes(V))
    [simplification]
endmodule
