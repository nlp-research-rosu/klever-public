requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // These are exactly the statement constructors generated in solution.mpy.
  syntax Stmts ::= "loopBody" [function, total]
  rule loopBody =>
    Expr(
      Call(
        Attribute(Name("result"), "append"),
        Subscript(Name("evens"), Name("i"))))
    Expr(Call(Attribute(Name("result"), "append"), Int(999)))
    AugAssign(Name("i"), "+", Int(1))

  syntax Stmts ::= "sortEvenBody" [function, total]
  rule sortEvenBody =>
    Assign(
      Name("evens"),
      Call(
        Name("sorted"),
        Subscript(Name("l"), Slice(NoBound, NoBound, Int(2)))))
    Assign(
      Name("odds"),
      Subscript(Name("l"), Slice(Int(1), NoBound, Int(2))))
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("i"), Int(0))
    Assign(Name("odd"), Int(0))
    For(Name("odd"), Name("odds"), loopBody)
    Return(
      BinOp(
        "+",
        Name("result"),
        Subscript(
          Name("evens"),
          Slice(Call(Name("len"), Name("odds")), NoBound, NoBound))))

  syntax Val ::= "sortEvenClosure" [function, total]
  rule sortEvenClosure => closureVal(("l"), sortEvenBody, 0)

  // Specialized instance of MPY-FUNCTIONS' ordinary parameter-binding rule.
  // Making the singleton shape explicit avoids a Haskell-backend narrowing
  // ambiguity with the higher-priority closure-cell binding rule.
  rule <k> #bindP(("l"), (V:Val, .Vals)) => .K ... </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(.Map => ("l" |-> V), _P:Parent) ... </scopes>
       [priority(30)]

  // The source list's even- and odd-index subsequences.  These formulae use
  // the supplied slice.indices helpers exactly as Subscript evaluation does.
  syntax ValSeq ::= evenIndices(ValSeq) [function, total]
                  | oddIndices(ValSeq)  [function, total]
  rule evenIndices(VS:ValSeq) =>
    buildVS(
      VS,
      slStart(noB, someB(2), vsLen(VS)),
      slStop(noB, someB(2), vsLen(VS)),
      slStep(someB(2)))
  rule oddIndices(VS:ValSeq) =>
    buildVS(
      VS,
      slStart(someB(1), someB(2), vsLen(VS)),
      slStop(noB, someB(2), vsLen(VS)),
      slStep(someB(2)))

  // Values appended by the for-loop while it consumes the odd-index list.
  syntax ValSeq ::= pairedVS(ValSeq, ValSeq, Int) [function, total]
  rule pairedVS(_:ValSeq, .ValSeq, _:Int) => .ValSeq
  rule pairedVS(EVS:ValSeq, vCons(O:Val, OS:ValSeq), I:Int) =>
    vCons(
      valSeqAt(EVS, normIdx(I, vsLen(EVS))),
      vCons(O, pairedVS(EVS, OS, I +Int 1)))

  syntax Int ::= advancedIndex(Int, ValSeq) [function, total]
  rule advancedIndex(I:Int, .ValSeq) => I
  rule advancedIndex(I:Int, vCons(_:Val, OS:ValSeq)) =>
    advancedIndex(I +Int 1, OS)

  // The suffix evens[len(odds):], which is empty for even-length inputs and
  // contains the final sorted even value for odd-length inputs.
  syntax ValSeq ::= evenSuffix(ValSeq, ValSeq) [function, total]
  rule evenSuffix(EVS:ValSeq, OVS:ValSeq) =>
    buildVS(
      EVS,
      slStart(someB(vsLen(OVS)), noB, vsLen(EVS)),
      slStop(noB, noB, vsLen(EVS)),
      slStep(noB))

  syntax ValSeq ::= assembledEvenSort(ValSeq, ValSeq) [function, total]
  rule assembledEvenSort(EVS:ValSeq, OVS:ValSeq) =>
    valSeqConcat(pairedVS(EVS, OVS, 0), evenSuffix(EVS, OVS))

  // Symbolic ACC does not expose its head, so the reference definition's
  // left-recursive concat rules cannot discover this right-identity case.
  // The equation is the standard list-concatenation identity.
  rule valSeqConcat(VS:ValSeq, .ValSeq) => VS [simplification]
  rule valSeqConcat(
         valSeqConcat(A:ValSeq, B:ValSeq),
         C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]

  // Plain (non-closure-cell) loop frames contain these five explicit
  // locals.  Exposing that "$cells" can only occur in the framed remainder
  // prevents the prover from exploring the annotated-cell assignment rule.
  rule "$cells" in_keys(
         ("evens" |-> _EV:Val)
         ("odds" |-> _OV:Val)
         ("result" |-> _RV:Val)
         ("i" |-> _IV:Val)
         ("odd" |-> _ODD:Val)
         M:Map)
    => "$cells" in_keys(M)
    [simplification]

  // Returned Python lists are heap references.  Observe their structural
  // value so the postcondition is independent of fresh heap addresses.
  syntax KItem ::= "#observeResult"
  rule <k> ref(H:Int) ~> #observeResult => V ... </k>
       <heap> ... H |-> V:Val ... </heap>
       [priority(40)]
  rule <k> V:Val ~> #observeResult => V ... </k>
       requires notBool isRefV(V)
endmodule
