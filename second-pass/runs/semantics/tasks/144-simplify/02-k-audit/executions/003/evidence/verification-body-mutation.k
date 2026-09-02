requires "reference-semantics/semantics.k"

module SIMPLIFY-VERIFICATION-BODY-MUTATION
  imports MPY

  syntax IntSeq ::= numCodes(Int)
                  | fractionCodes(Int, Int)

  rule splitSep(fractionCodes(A:Int, B:Int), 47, .IntSeq)
    => vCons(str(numCodes(A)), vCons(str(numCodes(B)), .ValSeq))

  rule applyBuiltin("int", str(numCodes(I:Int)), .Vals) => I

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
                       "+",
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
