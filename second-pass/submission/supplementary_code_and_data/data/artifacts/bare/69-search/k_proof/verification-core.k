requires "semantic.k"

module VERIFICATION-CORE
  imports MPY

  // A readable name for the exact constructor tree generated from solution.py.
  syntax Module ::= "searchProgram" [macro]
  syntax Stmts ::= "searchBody" [macro]
  syntax Stmts ::= "searchLoopBody" [macro]
  rule searchProgram => Module(FuncDef("search", Params("lst"), searchBody))
  rule searchBody =>
    Assign(Name("answer"), UnaryOp("-", Int(1)))
    For(Name("value"), Name("lst"), searchLoopBody)
    Return(Name("answer"))
  rule searchLoopBody =>
    If(Compare(
         Call(Attribute(Name("lst"), "count"), Name("value")),
         CmpOp(">=", Name("value"))),
       If(Compare(Name("value"), CmpOp(">", Name("answer"))),
          Assign(Name("answer"), Name("value")),
          .Stmts),
       .Stmts)

  // Mathematical reference model.  promote retains the current answer unless
  // the candidate occurs at least candidate-many times and is strictly larger.
  // searchSpec is therefore the greatest qualifying integer, or -1 if absent.
  syntax Int ::= promote(IntSeq, Int, Int) [function, total]
  rule promote(L, I, A) => I
    requires count(I, L) >=Int I andBool I >Int A
  rule promote(L, I, A) => A
    requires notBool (count(I, L) >=Int I andBool I >Int A)

  syntax Int ::= scan(IntSeq, IntSeq, Int) [function, total]
  rule scan(_, .Ints, A) => A
  rule scan(L, cons(I, IS), A) => scan(L, IS, promote(L, I, A))

  syntax Int ::= searchSpec(IntSeq) [function, total]
  rule searchSpec(L) => scan(L, L, -1)

  syntax Bool ::= positive(IntSeq) [function, total]
  rule positive(.Ints) => true
  rule positive(cons(I, IS)) => (I >Int 0) andBool positive(IS)
endmodule
