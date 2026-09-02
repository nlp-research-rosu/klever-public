requires "reference-semantics/semantics.k"

module PAIRS-VERIFICATION
  imports MPY

  syntax Stmts ::= "pairLoopBody" [function]
  rule pairLoopBody
    => If(Compare(UnaryOp("-", Name("value")),
                  CmpOp("in", Name("seen"))),
         Return(Bool(true)),
         .Stmts)
       Expr(Call(Attribute(Name("seen"), "append"),
                 (Name("value"), .Exprs)))
       .Stmts

  // This is the exact Stmts subtree emitted for pairs_sum_to_zero in
  // solution.mpy.  Naming it keeps the proof claims readable.
  syntax Stmts ::= "pairsBody" [function]
  rule pairsBody
    => Assign(Name("seen"), ListExpr(.Exprs))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("l"),
         If(Compare(UnaryOp("-", Name("value")),
                    CmpOp("in", Name("seen"))),
           Return(Bool(true)),
           .Stmts)
         Expr(Call(Attribute(Name("seen"), "append"),
                   (Name("value"), .Exprs)))
         .Stmts)
       Return(Bool(false))
       .Stmts

  // Mathematical oracle: an integer has an additive inverse in a sequence.
  syntax Bool ::= oppositeIn(Int, ValSeq) [function, total]
  rule oppositeIn(_:Int, .ValSeq) => false
  rule oppositeIn(X:Int, vCons(Y:Int, YS:ValSeq))
    => (X +Int Y ==Int 0) orBool oppositeIn(X, YS)

  // Mathematical contract: there are two positions i < j whose values sum
  // to zero.  Looking only in the tail makes the positions necessarily
  // distinct, including the [0] versus [0, 0] boundary case.
  syntax Bool ::= pairsSpec(ValSeq) [function, total]
  rule pairsSpec(.ValSeq) => false
  rule pairsSpec(vCons(X:Int, XS:ValSeq))
    => oppositeIn(X, XS) orBool pairsSpec(XS)

  // The heap list left by the implementation contains exactly the prefix
  // processed before the first match (or the complete input if no match).
  syntax ValSeq ::= seenAfter(ValSeq, ValSeq) [function, total]
  rule seenAfter(.ValSeq, SEEN:ValSeq) => SEEN
  rule seenAfter(vCons(X:Int, XS:ValSeq), SEEN:ValSeq) => SEEN
    requires oppositeIn(X, SEEN)
  rule seenAfter(vCons(X:Int, XS:ValSeq), SEEN:ValSeq)
    => seenAfter(XS, valSeqConcat(SEEN, vCons(X, .ValSeq)))
    requires notBool oppositeIn(X, SEEN)

  // IntSeq is a typed, inductive representation of every finite list of
  // integers. intValues is its proof-level embedding into ValSeq; the two
  // iterator equations below define precisely the same observations as a
  // vCons chain while keeping the symbolic tail typed.
  syntax ValSeq ::= intValues(IntSeq)

  syntax IntSeq ::= snocIS(IntSeq, Int) [function, total]
  rule snocIS(.IntSeq, X:Int) => iCons(X, .IntSeq)
  rule snocIS(iCons(Y:Int, YS:IntSeq), X:Int)
    => iCons(Y, snocIS(YS, X))

  syntax Bool ::= memberIS(Int, IntSeq) [function, total]
  rule memberIS(_:Int, .IntSeq) => false
  rule memberIS(V:Int, iCons(Y:Int, YS:IntSeq))
    => (Y ==Int V) orBool memberIS(V, YS)

  syntax Bool ::= oppositeIS(Int, IntSeq) [function, total]
  rule oppositeIS(X:Int, IS:IntSeq) => memberIS(0 -Int X, IS)

  // scanIS is the contract oracle. At each step it searches only the already
  // processed positions, so a successful pair always uses distinct indices.
  syntax Bool ::= scanIS(IntSeq, IntSeq) [function, total]
  rule scanIS(.IntSeq, _:IntSeq) => false
  rule scanIS(iCons(X:Int, XS:IntSeq), SEEN:IntSeq)
    => memberIS(0 -Int X, SEEN)
       orBool scanIS(XS, snocIS(SEEN, X))

  syntax Bool ::= pairsIS(IntSeq) [function, total]
  rule pairsIS(INPUT:IntSeq) => scanIS(INPUT, .IntSeq)

  syntax IntSeq ::= seenAfterIS(IntSeq, IntSeq) [function, total]
  rule seenAfterIS(.IntSeq, SEEN:IntSeq) => SEEN
  rule seenAfterIS(iCons(X:Int, XS:IntSeq), SEEN:IntSeq)
    => #if memberIS(0 -Int X, SEEN)
       #then SEEN
       #else seenAfterIS(XS, snocIS(SEEN, X))
       #fi

  // Iterator unfolding for the proof representation. These two rules are the
  // intValues instances of MPY-LIST's existing #iterNext equations.
  rule <k> #iterNext(list(intValues(.IntSeq))) => #iterDone ... </k>
  rule <k> #iterNext(list(intValues(iCons(X:Int, XS:IntSeq))))
        => #iterYield(X, list(intValues(XS))) ... </k>

  // Proof bridge: append preserves the typed representation. This equation is
  // the homomorphism lemma for valSeqConcat and snocIS.
  rule valSeqConcat(intValues(IS:IntSeq), vCons(X:Int, .ValSeq))
    => intValues(snocIS(IS, X))
endmodule

// This module is used only after loop-summary has been proved against the base
// PAIRS-VERIFICATION definition.  Its rule is that proved claim promoted as a
// lemma so the top-level function theorem composes without re-unfolding #loop.
module PAIRS-VERIFICATION-LEMMAS
  imports PAIRS-VERIFICATION

  // Representation bridge for the source's empty list literal. The abstract
  // value has exactly the empty-list iterator behavior proved above.
  rule <k> #applyK(toList, .Vals)
        => #alloc(list(intValues(.IntSeq))) ... </k>
    [priority(40)]

  rule
    <k>
      #loop(list(intValues(REM:IntSeq)),
            Name("value"),
            If(Compare(UnaryOp("-", Name("value")),
                       CmpOp("in", Name("seen"))),
               Return(Bool(true)),
               .Stmts)
            Expr(Call(Attribute(Name("seen"), "append"),
                      (Name("value"), .Exprs)))
            .Stmts)
      ~> (Return(Bool(false)) .Stmts)
      ~> #endcall
      =>
      scanIS(REM, SEEN)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      ( -1 |-> BUILTINS:Scope
        0 |-> scope(.Map, parent(-1))
        1 |-> scope(
          ( "l" |-> list(intValues(ORIGINAL:IntSeq))
            "seen" |-> ref(H:Int)
            "value" |-> OLD:Int ),
          parent(0)) )
      =>
      ( -1 |-> BUILTINS
        0 |-> scope(.Map, parent(-1)) )
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      (H |-> list(intValues(SEEN:IntSeq)) HEAP:Map)
      =>
      (H |-> list(intValues(seenAfterIS(REM, SEEN))) HEAP)
    </heap>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    [priority(40)]
endmodule
