requires "reference-semantics/semantics.k"

module ADD-ELEMENTS-VERIFICATION
  imports MPY

  syntax Bool ::= intsOnly(ValSeq) [function, total]
  rule intsOnly(.ValSeq) => true
  rule intsOnly(vCons(V:Val, R:ValSeq))
    => isInt(V) andBool intsOnly(R)

  // The contract's sum, written accumulator-first to align with the loop.
  // intValue is total for symbolic execution and is the identity on Int.
  syntax Int ::= qualifyingSumAcc(Int, ValSeq) [function]
  syntax Int ::= intValue(Val) [function, total]
  rule intValue(I:Int) => I
  rule qualifyingSumAcc(A:Int, .ValSeq) => A
  rule qualifyingSumAcc(A:Int, vCons(V:Val, R:ValSeq))
    => qualifyingSumAcc(A +Int intValue(V), R)
    requires isInt(V) andBool absInt(intValue(V)) <Int 100
  rule qualifyingSumAcc(A:Int, vCons(V:Val, R:ValSeq))
    => qualifyingSumAcc(A, R)
    requires isInt(V) andBool absInt(intValue(V)) >=Int 100

  // Refined-type bridge: under the contract's integer-list predicate, these
  // are exactly the existing MPY rules with the generated Int projection made
  // explicit for a symbolically Val-sorted head.
  rule applyBuiltin("abs", V:Val, .Vals)
    => absInt(intValue(V))
    requires isInt(V)
    [simplification]
  rule applyBin("+", A:Int, V:Val)
    => A +Int intValue(V)
    requires isInt(V)
    [simplification]

  // Symbolic map updates preserve ordinary lookup/key facts.  The concrete
  // MAP hook already computes these cases; these simplifiers expose the same
  // facts to the Haskell prover when the untouched map remainder is symbolic.
  rule K:KItem in_keys(M:Map [ K <- V:KItem ])
    => true [simplification]
  rule K1:KItem in_keys(M:Map [ K2:KItem <- V:KItem ])
    => K1 in_keys(M)
    requires K1 =/=K K2
    [simplification]
  rule (M:Map [ K:KItem <- V:KItem ]) [ K ] => V
    [simplification]
  rule (M:Map [ K2:KItem <- V:KItem ]) [ K1:KItem ] => M [ K1 ]
    requires K1 =/=K K2
    [simplification]

  // Prefix/suffix form is the contract-facing slice lemma. Every valid input
  // has arr = PREFIX ++ SUFFIX and k = len(PREFIX). These equations are the
  // corresponding specializations of MPY-SUBSCRIPT's slAdjust/buildVS rules.
  rule slAdjust(
         vsLen(PREFIX:ValSeq) +Int 1,
         vsLen(valSeqConcat(PREFIX, SUFFIX:ValSeq)) +Int 1,
         1
       )
    => vsLen(PREFIX) +Int 1
    [simplification]
  rule buildVS(
         vCons(HEAD:Val, valSeqConcat(PREFIX:ValSeq, SUFFIX:ValSeq)),
         0,
         vsLen(PREFIX) +Int 1,
         1
       )
    => vCons(HEAD, PREFIX)
    [simplification]
endmodule
