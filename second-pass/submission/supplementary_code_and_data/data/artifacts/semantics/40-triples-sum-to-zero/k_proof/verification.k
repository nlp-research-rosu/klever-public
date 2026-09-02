requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Independent executable specification:
  //   hasZeroTriple([a, ...]) =
  //     (some pair in the tail sums with a to zero)
  //     or hasZeroTriple(tail).
  syntax Bool ::= hasZeroTriple(ValSeq) [function]
                | hasZeroPair(Int, ValSeq) [function]
                | hasZeroThird(Int, ValSeq) [function]

  rule hasZeroTriple(.ValSeq) => false
  rule hasZeroTriple(vCons(A:Int, REST:ValSeq))
    => hasZeroPair(A, REST) orBool hasZeroTriple(REST)

  rule hasZeroPair(_:Int, .ValSeq) => false
  rule hasZeroPair(A:Int, vCons(B:Int, REST:ValSeq))
    => hasZeroThird(A +Int B, REST) orBool hasZeroPair(A, REST)

  rule hasZeroThird(_:Int, .ValSeq) => false
  rule hasZeroThird(S:Int, vCons(C:Int, REST:ValSeq))
    => (S +Int C ==Int 0) orBool hasZeroThird(S, REST)

  // A proof-only entry point which calls a closure containing exactly the
  // function body emitted in solution.mpy.  Concrete execution separately
  // checks normal FuncDef loading and Name-based call dispatch.
  syntax KItem ::= "#runTriples" "(" ValSeq ")"
  rule <k> #runTriples(VS:ValSeq)
        => #applyK(
             toCall(
               closureVal(
                 "l", .ParamNames,
                 For(Name("i"),
                   Call(Name("range"), Call(Name("len"), Name("l"))),
                   For(Name("j"),
                     Call(Name("range"),
                       BinOp("+", Name("i"), Int(1)),
                       Call(Name("len"), Name("l"))),
                     For(Name("k"),
                       Call(Name("range"),
                         BinOp("+", Name("j"), Int(1)),
                         Call(Name("len"), Name("l"))),
                       If(
                         Compare(
                           BinOp("+",
                             BinOp("+",
                               Subscript(Name("l"), Name("i")),
                               Subscript(Name("l"), Name("j"))),
                             Subscript(Name("l"), Name("k"))),
                           CmpOp("==", Int(0))),
                         Return(Bool(true)) .Stmts,
                         .Stmts)
                       .Stmts)
                     .Stmts)
                   .Stmts)
                 Return(Bool(false)) .Stmts,
                 0)),
             list(VS), .Vals)
        ... </k>
endmodule
