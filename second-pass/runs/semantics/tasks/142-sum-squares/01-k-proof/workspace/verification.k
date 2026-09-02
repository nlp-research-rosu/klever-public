requires "reference-semantics/semantics.k"

module SUM-SQUARES-VERIFICATION
  imports MPY

  // A mathematical sequence containing only integers.  intVals embeds it in
  // the semantic ValSeq used by Python lists.
  syntax Ints ::= ".Ints" | intCons(Int, Ints)

  syntax ValSeq ::= intVals(Ints)

  // Symbolic iterator bridge.  It presents Ints through the reference
  // semantics' iterator protocol and makes the constructor split visible to
  // the prover.
  rule <k> #iterNext(list(intVals(.Ints))) => #iterDone ... </k>
    [priority(40)]
  rule <k> #iterNext(list(intVals(intCons(X:Int, XS:Ints))))
        => #iterYield(X, list(intVals(XS))) ... </k>
    [priority(40)]

  // The contribution prescribed by the prompt.  The multiple-of-3 case has
  // priority over the multiple-of-4 case, including at index zero.
  syntax Int ::= contribution(Int, Int) [function]
  rule contribution(I:Int, X:Int) => X *Int X
    requires pyMod(I, 3) ==Int 0
  rule contribution(I:Int, X:Int) => X *Int X *Int X
    requires pyMod(I, 3) =/=Int 0 andBool pyMod(I, 4) ==Int 0
  rule contribution(I:Int, X:Int) => X
    requires pyMod(I, 3) =/=Int 0 andBool pyMod(I, 4) =/=Int 0

  // Tail-recursive contract for the complete result.
  syntax Int ::= sumSquares(Ints, Int, Int) [function, total]
  rule sumSquares(.Ints, _:Int, ACC:Int) => ACC
  rule sumSquares(intCons(X:Int, XS:Ints), I:Int, ACC:Int)
    => sumSquares(XS, I +Int 1, ACC +Int contribution(I, X))

  // The other two pieces of the exact loop post-state.
  syntax Int ::= endIndex(Ints, Int) [function, total]
  rule endIndex(.Ints, I:Int) => I
  rule endIndex(intCons(_:Int, XS:Ints), I:Int)
    => endIndex(XS, I +Int 1)

  syntax Int ::= endValue(Ints, Int) [function, total]
  rule endValue(.Ints, OLD:Int) => OLD
  rule endValue(intCons(X:Int, XS:Ints), _:Int)
    => endValue(XS, X)

  syntax Stmts ::= "sumSquaresLoopBody" [macro]
  rule sumSquaresLoopBody
    => If(
         Compare(
           BinOp("%", Name("index"), Int(3)),
           CmpOp("==", Int(0))),
         AugAssign(
           Name("total"),
           "+",
           BinOp("*", Name("value"), Name("value")))
         .Stmts,
         If(
           Compare(
             BinOp("%", Name("index"), Int(4)),
             CmpOp("==", Int(0))),
           AugAssign(
             Name("total"),
             "+",
             BinOp(
               "*",
               BinOp("*", Name("value"), Name("value")),
               Name("value")))
           .Stmts,
           AugAssign(Name("total"), "+", Name("value"))
           .Stmts)
         .Stmts)
       AugAssign(Name("index"), "+", Int(1))
       .Stmts

  syntax Stmts ::= "sumSquaresFunctionBody" [macro]
  rule sumSquaresFunctionBody
    => Assign(Name("total"), Int(0))
       Assign(Name("index"), Int(0))
       For(Name("value"), Name("lst"), sumSquaresLoopBody)
       Return(Name("total"))
       .Stmts
endmodule
