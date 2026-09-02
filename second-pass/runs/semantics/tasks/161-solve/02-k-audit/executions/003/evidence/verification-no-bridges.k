requires "/tmp/audit-work/161-solve/reference-semantics/semantics.k"

module VERIFICATION-NO-BRIDGES
  imports MPY

  syntax Stmts ::= solveBodyNoBridges ( ) [function, total]
  rule solveBodyNoBridges()
    => Assign(Name("result"),
         Call(Attribute(Name("s"), "swapcase"), .Exprs))
       If(Compare(Name("result"), CmpOp("==", Name("s"))),
         Return(Subscript(Name("s"),
           Slice(NoBound, NoBound, UnaryOp("-", Int(1))))) .Stmts,
         .Stmts)
       Return(Name("result")) .Stmts

  syntax Module ::= solutionModuleNoBridges ( ) [function, total]
  rule solutionModuleNoBridges()
    => Module(FuncDef("solve", Params("s"), solveBodyNoBridges()))

  syntax Val ::= solutionClosureNoBridges ( ) [function, total]
  rule solutionClosureNoBridges()
    => closureVal("s", .ParamNames, solveBodyNoBridges(), 0)

  syntax KItem ::= #runSolveNoBridges ( IntSeq )
  rule <k> #runSolveNoBridges(CS)
        => #loadAll(solutionModuleNoBridges())
        ~> Call(Name("solve"), (str(CS), .Exprs)) ... </k>
endmodule

module VERIFICATION-NO-BRIDGES-SYNTAX
  imports VERIFICATION-NO-BRIDGES
endmodule
