requires "semantic.k"

module VERIFICATION
  imports MPY

  // A mathematical restatement of the prompt's table over exact rationals.
  // The first two equations preserve the program's deliberate special case:
  // exactly 4.0 is A+, while any other value above 3.7 is A.
  syntax Value ::= expectedGrade(Int, Int) [function, total]
  rule expectedGrade(P, Q) => str("A+")
    requires P ==Int (4 *Int Q)
  rule expectedGrade(P, Q) => str("A")
    requires (P =/=Int (4 *Int Q)) andBool ((10 *Int P) >Int (37 *Int Q))
  rule expectedGrade(P, Q) => str("A-")
    requires ((10 *Int P) <=Int (37 *Int Q)) andBool ((10 *Int P) >Int (33 *Int Q))
  rule expectedGrade(P, Q) => str("B+")
    requires ((10 *Int P) <=Int (33 *Int Q)) andBool ((10 *Int P) >Int (30 *Int Q))
  rule expectedGrade(P, Q) => str("B")
    requires ((10 *Int P) <=Int (30 *Int Q)) andBool ((10 *Int P) >Int (27 *Int Q))
  rule expectedGrade(P, Q) => str("B-")
    requires ((10 *Int P) <=Int (27 *Int Q)) andBool ((10 *Int P) >Int (23 *Int Q))
  rule expectedGrade(P, Q) => str("C+")
    requires ((10 *Int P) <=Int (23 *Int Q)) andBool ((10 *Int P) >Int (20 *Int Q))
  rule expectedGrade(P, Q) => str("C")
    requires ((10 *Int P) <=Int (20 *Int Q)) andBool ((10 *Int P) >Int (17 *Int Q))
  rule expectedGrade(P, Q) => str("C-")
    requires ((10 *Int P) <=Int (17 *Int Q)) andBool ((10 *Int P) >Int (13 *Int Q))
  rule expectedGrade(P, Q) => str("D+")
    requires ((10 *Int P) <=Int (13 *Int Q)) andBool ((10 *Int P) >Int (10 *Int Q))
  rule expectedGrade(P, Q) => str("D")
    requires ((10 *Int P) <=Int (10 *Int Q)) andBool ((10 *Int P) >Int (7 *Int Q))
  rule expectedGrade(P, Q) => str("D-")
    requires ((10 *Int P) <=Int (7 *Int Q)) andBool (P >Int 0)
  rule expectedGrade(P, _Q) => str("E")
    requires P <=Int 0

  syntax Vals ::= expectedGrades(Vals) [function, total]
  rule expectedGrades(.Vals) => .Vals
  rule expectedGrades(num(P, Q) :: REST)
    => expectedGrade(P, Q) :: expectedGrades(REST)

  // The exact loop body is named so the proof can state and verify its
  // per-iteration invariant independently of list length.
  syntax Stmts ::= "gradingBody" [function, total]
  rule gradingBody =>
    If(Compare(Name("grade"), CmpOp("==", Float(4.0))),
      Expr(Call(Attribute(Name("result"), "append"), Str("WRONG"))),
      If(Compare(Name("grade"), CmpOp(">", Float(3.7))),
        Expr(Call(Attribute(Name("result"), "append"), Str("A"))),
        If(Compare(Name("grade"), CmpOp(">", Float(3.3))),
          Expr(Call(Attribute(Name("result"), "append"), Str("A-"))),
          If(Compare(Name("grade"), CmpOp(">", Float(3.0))),
            Expr(Call(Attribute(Name("result"), "append"), Str("B+"))),
            If(Compare(Name("grade"), CmpOp(">", Float(2.7))),
              Expr(Call(Attribute(Name("result"), "append"), Str("B"))),
              If(Compare(Name("grade"), CmpOp(">", Float(2.3))),
                Expr(Call(Attribute(Name("result"), "append"), Str("B-"))),
                If(Compare(Name("grade"), CmpOp(">", Float(2.0))),
                  Expr(Call(Attribute(Name("result"), "append"), Str("C+"))),
                  If(Compare(Name("grade"), CmpOp(">", Float(1.7))),
                    Expr(Call(Attribute(Name("result"), "append"), Str("C"))),
                    If(Compare(Name("grade"), CmpOp(">", Float(1.3))),
                      Expr(Call(Attribute(Name("result"), "append"), Str("C-"))),
                      If(Compare(Name("grade"), CmpOp(">", Float(1.0))),
                        Expr(Call(Attribute(Name("result"), "append"), Str("D+"))),
                        If(Compare(Name("grade"), CmpOp(">", Float(0.7))),
                          Expr(Call(Attribute(Name("result"), "append"), Str("D"))),
                          If(Compare(Name("grade"), CmpOp(">", Float(0.0))),
                            Expr(Call(Attribute(Name("result"), "append"), Str("D-"))),
                            Expr(Call(Attribute(Name("result"), "append"), Str("E")))))))))))))))

  // This term is an exact K copy of solution.mpy. Keeping it here makes each
  // reachability claim explicitly start from the submitted translated program.
  syntax Module ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      FuncDef("numerical_letter_grade", Params("grades"),
        Expr(
          Str("Convert each numerical GPA in grades to its letter grade."))
        Assign(Name("result"), ListExpr(.Exprs))
        For(Name("grade"), Name("grades"), gradingBody)
        Return(Name("result"))))
endmodule
