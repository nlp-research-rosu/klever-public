requires "reference-semantics/semantics.k"

module SIMPLIFY-VERIFICATION
  imports MPY

  // Symbolic encodings of a positive decimal numeral and of "A/B".
  //
  // The reference semantics defines split and int on concrete IntSeq values.
  // These constructors summarize the same two operations for symbolic A and B,
  // allowing the proof to range over arbitrary positive integers rather than
  // over a fixed number of decimal digits.
  syntax IntSeq ::= numCodes(Int)
                  | fractionCodes(Int, Int)

  rule splitSep(fractionCodes(A:Int, B:Int), 47, .IntSeq)
    => vCons(str(numCodes(A)), vCons(str(numCodes(B)), .ValSeq))

  rule applyBuiltin("int", str(numCodes(I:Int)), .Vals) => I

  // This is exactly the translated function body from solution.mpy, packaged
  // as a callable closure so that claims can supply symbolic argument values.
  syntax KItem ::= runSimplify(Val, Val)
  rule <k> runSimplify(X:Val, N:Val)
        => #applyK(
             toCall(
               closureVal(
                 ("x", "n"),
                 Assign(
                   TupleExpr(Name("x_num"), Name("x_den")),
                   Call(Attribute(Name("x"), "split"), Str("/")))
                 Assign(
                   TupleExpr(Name("n_num"), Name("n_den")),
                   Call(Attribute(Name("n"), "split"), Str("/")))
                 Return(
                   Compare(
                     BinOp(
                       "%",
                       BinOp(
                         "*",
                         Call(Name("int"), Name("x_num")),
                         Call(Name("int"), Name("n_num"))),
                       BinOp(
                         "*",
                         Call(Name("int"), Name("x_den")),
                         Call(Name("int"), Name("n_den")))),
                     CmpOp("==", Int(0)))),
                 0)),
             (X, N, .Vals))
        ... </k>
endmodule
