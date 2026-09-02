requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  syntax Stmts ::= solveBody ( ) [function, total]
  rule solveBody()
    => Assign(Name("result"),
         Call(Attribute(Name("s"), "swapcase"), .Exprs))
       If(Compare(Name("result"), CmpOp("==", Name("s"))),
         Return(Subscript(Name("s"),
           Slice(NoBound, NoBound, UnaryOp("-", Int(1))))) .Stmts,
         .Stmts)
       Return(Name("result")) .Stmts

  syntax Module ::= solutionModule ( ) [function, total]
  rule solutionModule()
    => Module(FuncDef("solve", Params("s"), solveBody()))

  syntax Val ::= solutionClosure ( ) [function, total]
  rule solutionClosure()
    => closureVal("s", .ParamNames, solveBody(), 0)

  syntax Bool ::= containsLetter ( IntSeq ) [function, total]
  rule containsLetter(CS) => notBool (mapSwap(CS) ==K CS)

  syntax IntSeq ::= solveSpec ( IntSeq ) [function, total]
  rule solveSpec(CS)
    => #if containsLetter(CS)
       #then mapSwap(CS)
       #else revIS(CS)
       #fi

  // Both candidate reverse simplifications are intentionally omitted.

  syntax KItem ::= #runSolve ( IntSeq )
  rule <k> #runSolve(CS)
        => #loadAll(solutionModule())
        ~> Call(Name("solve"), (str(CS), .Exprs)) ... </k>
endmodule

module VERIFICATION-SYNTAX
  imports VERIFICATION
endmodule
