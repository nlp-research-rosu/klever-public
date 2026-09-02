requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical model used by the contract.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(_:Int, REST:ValSeq)) => allInts(REST)
  rule allInts(vCons(V:Val, _:ValSeq)) => false
    requires notBool isInt(V)

  syntax Int ::= sumIntVS(ValSeq) [function, total]
  rule sumIntVS(.ValSeq) => 0
  rule sumIntVS(vCons(I:Int, REST:ValSeq)) => I +Int sumIntVS(REST)

  syntax ValSeq ::= snocVS(ValSeq, Val) [function, total]
  rule snocVS(.ValSeq, V:Val) => vCons(V, .ValSeq)
  rule snocVS(vCons(H:Val, T:ValSeq), V:Val)
    => vCons(H, snocVS(T, V))

  syntax ValSeq ::= reverseVS(ValSeq) [function, total]
  rule reverseVS(.ValSeq) => .ValSeq
  rule reverseVS(vCons(H:Val, T:ValSeq))
    => snocVS(reverseVS(T), H)

  // Symbolic summaries of two terminating folds in the supplied semantics.
  // They agree with subscript.k's q[::-1] and builtins.k's sum(q), while
  // allowing a proof over an arbitrary (rather than fixed-length) ValSeq.
  rule doSlice(list(VS:ValSeq), noB, noB, someB(-1))
    => list(reverseVS(VS))
    [priority(40)]

  rule <k> #sumAcc(list(VS:ValSeq), 0) => sumIntVS(VS) ... </k>
    requires allInts(VS)
    [priority(40)]

  syntax Expr ::= "willItFlyResult"
  rule willItFlyResult
    => BoolOp(
         "and",
         Compare(
           Name("q"),
           CmpOp(
             "==",
             Subscript(
               Name("q"),
               Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))),
         Compare(Call(Name("sum"), Name("q")), CmpOp("<=", Name("w"))))

  // The translated entry point, factored into named terms so the claims can
  // execute definition, lookup, argument binding, return, and frame cleanup.
  syntax Module ::= "willItFlyModule" [function]
  rule willItFlyModule
    => Module(
         FuncDef(
           "will_it_fly",
           Params("q", "w"),
           Return(willItFlyResult)))

  syntax Val ::= "willItFlyClosure" [function]
  rule willItFlyClosure
    => closureVal(("q", "w"), Return(willItFlyResult), 0)
endmodule
