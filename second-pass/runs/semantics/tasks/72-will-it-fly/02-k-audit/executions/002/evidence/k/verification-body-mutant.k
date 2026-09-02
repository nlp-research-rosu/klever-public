requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Bool ::= mutantAllInts(ValSeq) [function, total]
  rule mutantAllInts(.ValSeq) => true
  rule mutantAllInts(vCons(_:Int, REST:ValSeq)) => mutantAllInts(REST)
  rule mutantAllInts(vCons(V:Val, _:ValSeq)) => false
    requires notBool isInt(V)

  syntax Int ::= mutantSumIntVS(ValSeq) [function, total]
  rule mutantSumIntVS(.ValSeq) => 0
  rule mutantSumIntVS(vCons(I:Int, REST:ValSeq))
    => I +Int mutantSumIntVS(REST)

  syntax ValSeq ::= mutantSnocVS(ValSeq, Val) [function, total]
  rule mutantSnocVS(.ValSeq, V:Val) => vCons(V, .ValSeq)
  rule mutantSnocVS(vCons(H:Val, T:ValSeq), V:Val)
    => vCons(H, mutantSnocVS(T, V))

  syntax ValSeq ::= mutantReverseVS(ValSeq) [function, total]
  rule mutantReverseVS(.ValSeq) => .ValSeq
  rule mutantReverseVS(vCons(H:Val, T:ValSeq))
    => mutantSnocVS(mutantReverseVS(T), H)

  rule doSlice(list(VS:ValSeq), noB, noB, someB(-1))
    => list(mutantReverseVS(VS))
    [priority(40)]

  rule <k> #sumAcc(list(VS:ValSeq), 0) => mutantSumIntVS(VS) ... </k>
    requires mutantAllInts(VS)
    [priority(40)]

  // Material body mutation: strict < replaces submitted <=.
  syntax Expr ::= "mutantWillItFlyResult"
  rule mutantWillItFlyResult
    => BoolOp(
         "and",
         Compare(
           Name("q"),
           CmpOp(
             "==",
             Subscript(
               Name("q"),
               Slice(NoBound, NoBound, UnaryOp("-", Int(1)))))),
         Compare(Call(Name("sum"), Name("q")), CmpOp("<", Name("w"))))

  syntax Module ::= "mutantWillItFlyModule" [function]
  rule mutantWillItFlyModule
    => Module(
         FuncDef(
           "will_it_fly",
           Params("q", "w"),
           Return(mutantWillItFlyResult)))

  syntax Val ::= "mutantWillItFlyClosure" [function]
  rule mutantWillItFlyClosure
    => closureVal(("q", "w"), Return(mutantWillItFlyResult), 0)
endmodule
