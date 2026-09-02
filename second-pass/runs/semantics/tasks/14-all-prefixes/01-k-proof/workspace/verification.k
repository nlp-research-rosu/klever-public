requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The mathematical result of finishing the source loop from END to STOP,
  // starting with accumulator ACC.  doSlice is the reference semantics'
  // definition of Python slicing, so this definition also covers empty and
  // out-of-range slice bounds without an extra assumption.
  syntax ValSeq ::= prefixesAcc(IntSeq, Int, Int, ValSeq) [function]
  rule prefixesAcc(S:IntSeq, END:Int, STOP:Int, ACC:ValSeq)
    => prefixesAcc(
         S,
         END +Int 1,
         STOP,
         valSeqConcat(
           ACC,
           vCons(doSlice(str(S), noB, someB(END), noB), .ValSeq)))
    requires END <Int STOP
  rule prefixesAcc(_:IntSeq, END:Int, STOP:Int, ACC:ValSeq) => ACC
    requires END >=Int STOP

  syntax ValSeq ::= allPrefixes(IntSeq) [function]
  rule allPrefixes(S:IntSeq)
    => prefixesAcc(S, 1, isLen(S) +Int 1, .ValSeq)

  // Constructor terms copied exactly from solution.mpy.  Keeping them named
  // makes the claims readable while still executing the translated program.
  syntax Stmts ::= allPrefixesLoopBody() [function, total]
  rule allPrefixesLoopBody()
    => Expr(Call(
         Attribute(Name("prefixes"), "append"),
         Subscript(
           Name("string"),
           Slice(NoBound, Name("end"), NoBound))))
       .Stmts

  syntax Stmts ::= allPrefixesBody() [function, total]
  rule allPrefixesBody()
    => Expr(Str("Return all nonempty prefixes of string, shortest first."))
       Assign(Name("prefixes"), ListExpr(.Exprs))
       For(
         Name("end"),
         Call(
           Name("range"),
           Int(1),
           BinOp("+", Call(Name("len"), Name("string")), Int(1))),
         allPrefixesLoopBody())
       Return(Name("prefixes"))
       .Stmts

  syntax Stmt ::= allPrefixesDef() [function, total]
  rule allPrefixesDef()
    => FuncDef("all_prefixes", Params("string"), allPrefixesBody())

  syntax Module ::= solutionModule() [function, total]
  rule solutionModule()
    => Module(ImportFrom("typing", "List") allPrefixesDef())
endmodule
