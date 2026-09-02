requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUT
  imports MPY

  syntax KItem ::= "#checkIfLastCharMut" "(" Val ")"

  // Deliberate body mutation: compare the penultimate character to "x"
  // instead of the submitted body's " ".
  rule #checkIfLastCharMut(V:Val)
    => Call(
         closureVal(
           "txt",
           If(Compare(Call(Name("len"), Name("txt")),
                      CmpOp("==", Int(0))),
              Return(Bool(false)),
              .Stmts)
           If(UnaryOp("not",
                      Call(Attribute(
                             Subscript(Name("txt"), UnaryOp("-", Int(1))),
                             "isalpha"),
                           .Exprs)),
              Return(Bool(false)),
              .Stmts)
           If(Compare(Call(Name("len"), Name("txt")),
                      CmpOp("==", Int(1))),
              Return(Bool(true)),
              .Stmts)
           Return(Compare(
                    Subscript(Name("txt"), UnaryOp("-", Int(2))),
                    CmpOp("==", Str("x")))),
           0),
         V)

  rule isLen(seqConcat(P:IntSeq, iCons(A:Int, iCons(B:Int, .IntSeq))))
    => isLen(P) +Int 2
    [simplification]

  rule intSeqAt(
         seqConcat(P:IntSeq, iCons(A:Int, iCons(B:Int, .IntSeq))),
         isLen(P))
    => A
    [simplification]

  rule intSeqAt(
         seqConcat(P:IntSeq, iCons(A:Int, iCons(B:Int, .IntSeq))),
         isLen(P) +Int 1)
    => B
    [simplification]
endmodule
