requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This is the exact translated body of the loop in solution.mpy.
  syntax Stmts ::= "parseLoopBody" [function]
  rule parseLoopBody
    => If(Compare(Name("char"), CmpOp("==", Str("("))),
          AugAssign(Name("depth"), "+", Int(1))
          If(Compare(Name("depth"), CmpOp(">", Name("maximum"))),
            Assign(Name("maximum"), Name("depth")),
            .Stmts),
          If(Compare(Name("char"), CmpOp("==", Str(")"))),
            AugAssign(Name("depth"), "-", Int(1)),
            If(Compare(Name("char"), CmpOp("==", Str(" "))),
              Expr(Call(Attribute(Name("result"), "append"), Name("maximum")))
              Assign(Name("depth"), Int(0))
              Assign(Name("maximum"), Int(0)),
              .Stmts)))

  // This closure is the exact translated implementation in solution.mpy.
  syntax Stmts ::= "parseFunctionBody" [function]
  rule parseFunctionBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("depth"), Int(0))
       Assign(Name("maximum"), Int(0))
       Assign(Name("char"), Str(""))
       For(Name("char"), Name("paren_string"), parseLoopBody)
       Expr(Call(Attribute(Name("result"), "append"), Name("maximum")))
       Return(Name("result"))

  syntax Val ::= "parseNestedParensClosure" [function]
  rule parseNestedParensClosure
    => closureVal("paren_string", parseFunctionBody, 0)

  // Pure mathematical scan used only on the specification side.  The state
  // records current depth, maximum depth in the current group, and completed
  // group maxima.  Non-parenthesis, non-space characters are ignored; the
  // HumanEval precondition is therefore a subset of what is proved.
  syntax ScanState ::= scanDone(Int, Int, ValSeq)
                     | scanParens(IntSeq, Int, Int, ValSeq) [function]

  syntax Int ::= parenMax(Int, Int) [function, total]
  rule parenMax(A:Int, B:Int) => A requires A >Int B
  rule parenMax(A:Int, B:Int) => B requires A <=Int B

  rule scanParens(.IntSeq, D:Int, M:Int, VS:ValSeq)
    => scanDone(D, M, VS)
  rule scanParens(iCons(40, R:IntSeq), D:Int, M:Int, VS:ValSeq)
    => scanParens(R, D +Int 1, parenMax(D +Int 1, M), VS)
  rule scanParens(iCons(41, R:IntSeq), D:Int, M:Int, VS:ValSeq)
    => scanParens(R, D -Int 1, M, VS)
  rule scanParens(iCons(32, R:IntSeq), D:Int, M:Int, VS:ValSeq)
    => scanParens(R, 0, 0, valSeqConcat(VS, vCons(M, .ValSeq)))
  rule scanParens(iCons(C:Int, R:IntSeq), D:Int, M:Int, VS:ValSeq)
    => scanParens(R, D, M, VS)
    [owise]

  syntax Int ::= scanDepth(ScanState) [function, total]
               | scanMaximum(ScanState) [function, total]
  syntax ValSeq ::= scanValues(ScanState) [function, total]
  rule scanDepth(scanDone(D:Int, _:Int, _:ValSeq)) => D
  rule scanMaximum(scanDone(_:Int, M:Int, _:ValSeq)) => M
  rule scanValues(scanDone(_:Int, _:Int, VS:ValSeq)) => VS

  syntax Val ::= finalChar(IntSeq, Val) [function, total]
  rule finalChar(.IntSeq, OLD:Val) => OLD
  rule finalChar(iCons(C:Int, R:IntSeq), _:Val)
    => finalChar(R, str(iCons(C, .IntSeq)))

  syntax ValSeq ::= parsedParens(IntSeq) [function]
  rule parsedParens(S:IntSeq)
    => valSeqConcat(
         scanValues(scanParens(S, 0, 0, .ValSeq)),
         vCons(scanMaximum(scanParens(S, 0, 0, .ValSeq)), .ValSeq))

  syntax Bool ::= parenInput(IntSeq) [function, total]
  rule parenInput(.IntSeq) => true
  rule parenInput(iCons(C:Int, R:IntSeq))
    => (C ==Int 40 orBool C ==Int 41 orBool C ==Int 32)
       andBool parenInput(R)
endmodule
