requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact AST shorthands for the generated solution.mpy program.
  syntax Stmts ::= "loopBody" [function, total]
  rule loopBody =>
    If(Compare(Name("char"), CmpOp("==", Str("("))),
      AugAssign(Name("depth"), "+", Int(1))
      If(Compare(Name("depth"), CmpOp(">", Name("deepest"))),
        Assign(Name("deepest"), Name("depth")),
        .Stmts),
      If(Compare(Name("char"), CmpOp("==", Str(")"))),
        AugAssign(Name("depth"), "-", Int(1)),
        If(Compare(Name("deepest"), CmpOp(">", Int(0))),
          Expr(Call(Attribute(Name("depths"), "append"), Name("deepest")))
          Assign(Name("deepest"), Int(0)),
          .Stmts)))

  syntax Stmts ::= "afterLoop" [function, total]
  rule afterLoop =>
    If(Compare(Name("deepest"), CmpOp(">", Int(0))),
      Expr(Call(Attribute(Name("depths"), "append"), Name("deepest"))),
      .Stmts)
    Return(Name("depths"))

  syntax Stmts ::= "solutionBody" [function, total]
  rule solutionBody =>
    Assign(Name("depths"), ListExpr(.Exprs))
    Assign(Name("depth"), Int(0))
    Assign(Name("deepest"), Int(0))
    Assign(Name("char"), Str(""))
    For(Name("char"), Name("paren_string"), loopBody)
    afterLoop

  syntax Module ::= "solutionModule" [function, total]
  rule solutionModule =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("parse_nested_parens", Params("paren_string"), solutionBody))

  // A total character scanner. Codes 40 and 41 are '(' and ')'; every other
  // code follows the program's delimiter branch. The target precondition below
  // narrows delimiters to ASCII space (32).
  syntax Int ::= scanDepth(IntSeq, Int) [function, total]
  syntax Int ::= nextDepth(Int, Int) [function, total]
  rule nextDepth(C, D) => D +Int 1
    requires C ==Int 40
  rule nextDepth(C, D) => D -Int 1
    requires C ==Int 41
  rule nextDepth(C, D) => D
    requires C =/=Int 40 andBool C =/=Int 41

  rule scanDepth(.IntSeq, D) => D
  rule scanDepth(iCons(C, R), D) => scanDepth(R, nextDepth(C, D))

  syntax Int ::= scanDeepest(IntSeq, Int, Int) [function, total]
  syntax Int ::= openDeepest(Int, Int) [function, total]
  rule openDeepest(D, M) => D +Int 1
    requires D +Int 1 >Int M
  rule openDeepest(D, M) => M
    requires D +Int 1 <=Int M

  syntax Int ::= delimiterDeepest(Int) [function, total]
  rule delimiterDeepest(M) => 0
    requires M >Int 0
  rule delimiterDeepest(M) => M
    requires M <=Int 0

  syntax Int ::= nextDeepest(Int, Int, Int) [function, total]
  rule nextDeepest(C, D, M) => openDeepest(D, M)
    requires C ==Int 40
  rule nextDeepest(C, _D, M) => M
    requires C ==Int 41
  rule nextDeepest(C, _D, M) => delimiterDeepest(M)
    requires C =/=Int 40 andBool C =/=Int 41

  rule scanDeepest(.IntSeq, _D, M) => M
  rule scanDeepest(iCons(C, R), D, M)
    => scanDeepest(R, nextDepth(C, D), nextDeepest(C, D, M))

  syntax ValSeq ::= scanOutput(IntSeq, Int, Int, ValSeq) [function, total]
  syntax ValSeq ::= delimiterOutput(Int, ValSeq) [function, total]
  rule delimiterOutput(M, OUT) => valSeqConcat(OUT, vCons(M, .ValSeq))
    requires M >Int 0
  rule delimiterOutput(M, OUT) => OUT
    requires M <=Int 0

  syntax ValSeq ::= nextOutput(Int, Int, ValSeq) [function, total]
  rule nextOutput(C, _M, OUT) => OUT
    requires C ==Int 40
  rule nextOutput(C, _M, OUT) => OUT
    requires C ==Int 41
  rule nextOutput(C, M, OUT) => delimiterOutput(M, OUT)
    requires C =/=Int 40 andBool C =/=Int 41

  rule scanOutput(.IntSeq, _D, _M, OUT) => OUT
  rule scanOutput(iCons(C, R), D, M, OUT)
    => scanOutput(R, nextDepth(C, D), nextDeepest(C, D, M),
                  nextOutput(C, M, OUT))

  syntax Str ::= scanChar(IntSeq, Str) [function, total]
  rule scanChar(.IntSeq, CH) => CH
  rule scanChar(iCons(C, R), _CH) => scanChar(R, str(iCons(C, .IntSeq)))

  syntax ValSeq ::= finishOutput(IntSeq, Int, Int, ValSeq) [function, total]
  rule finishOutput(CS, D, M, OUT)
    => valSeqConcat(scanOutput(CS, D, M, OUT),
                    vCons(scanDeepest(CS, D, M), .ValSeq))
    requires scanDeepest(CS, D, M) >Int 0
  rule finishOutput(CS, D, M, OUT) => scanOutput(CS, D, M, OUT)
    requires scanDeepest(CS, D, M) <=Int 0

  syntax ValSeq ::= expectedDepths(IntSeq) [function, total]
  rule expectedDepths(CS) => finishOutput(CS, 0, 0, .ValSeq)

  // The contract domain: a finite sequence of parentheses and ASCII spaces;
  // every prefix has nonnegative depth, spaces occur only at depth zero, and
  // the final depth is zero.
  syntax Bool ::= wellFormed(IntSeq, Int) [function, total]
  syntax Bool ::= wellFormedStep(Int, IntSeq, Int) [function, total]
  rule wellFormedStep(C, R, D) => wellFormed(R, D +Int 1)
    requires C ==Int 40
  rule wellFormedStep(C, R, D) => D >Int 0 andBool wellFormed(R, D -Int 1)
    requires C ==Int 41
  rule wellFormedStep(C, R, D) => D ==Int 0 andBool wellFormed(R, D)
    requires C ==Int 32
  rule wellFormedStep(C, _R, _D) => false
    requires C =/=Int 40 andBool C =/=Int 41 andBool C =/=Int 32

  rule wellFormed(.IntSeq, D) => D ==Int 0
  rule wellFormed(iCons(C, R), D) => wellFormedStep(C, R, D)

  syntax Bool ::= validInput(IntSeq) [function, total]
  rule validInput(CS) => wellFormed(CS, 0)
endmodule
