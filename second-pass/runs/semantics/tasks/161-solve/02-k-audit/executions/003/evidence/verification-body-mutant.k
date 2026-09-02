requires "/tmp/audit-work/161-solve/reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  syntax Stmts ::= solveBodyMutant ( ) [function, total]
  rule solveBodyMutant()
    => Assign(Name("result"),
         Call(Attribute(Name("s"), "lower"), .Exprs))
       If(Compare(Name("result"), CmpOp("==", Name("s"))),
         Return(Subscript(Name("s"),
           Slice(NoBound, NoBound, UnaryOp("-", Int(1))))) .Stmts,
         .Stmts)
       Return(Name("result")) .Stmts

  syntax Module ::= solutionModuleMutant ( ) [function, total]
  rule solutionModuleMutant()
    => Module(FuncDef("solve", Params("s"), solveBodyMutant()))

  syntax Val ::= solutionClosureMutant ( ) [function, total]
  rule solutionClosureMutant()
    => closureVal("s", .ParamNames, solveBodyMutant(), 0)

  rule doSlice(str(CS), noB, noB, someB(-1))
    => str(revIS(CS))
    [simplification]

  rule buildIS(CS, isLen(CS) +Int -1, -1, -1)
    => revIS(CS)
    [simplification]

  syntax KItem ::= #runSolveMutant ( IntSeq )
  rule <k> #runSolveMutant(CS)
        => #loadAll(solutionModuleMutant())
        ~> Call(Name("solve"), (str(CS), .Exprs)) ... </k>
endmodule

module VERIFICATION-BODY-MUTANT-SYNTAX
  imports VERIFICATION-BODY-MUTANT
endmodule
