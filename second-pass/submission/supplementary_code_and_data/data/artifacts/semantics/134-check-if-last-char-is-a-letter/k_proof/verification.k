requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The harness invokes exactly the closure produced by solution.mpy after
  // its module-level FuncDef has loaded.
  syntax KItem ::= "#checkIfLastChar" "(" Val ")"

  rule #checkIfLastChar(V:Val)
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
                    CmpOp("==", Str(" ")))),
           0),
         V)

  // Symbolic suffix lemmas.  Every string with at least two characters is
  // seqConcat(PREFIX, iCons(PREV, iCons(LAST, .IntSeq))) for some PREFIX.
  // These equations expose len() and Python's negative indexing without
  // assuming anything about that prefix.
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
