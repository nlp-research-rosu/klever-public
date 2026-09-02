requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Exact AST abbreviations for solution.mpy. These are compile-time macros;
  // no program step is replaced at runtime.
  syntax Stmts ::= "GRADE-STEP" [macro]
  rule GRADE-STEP
    => If(Compare(Name("grade"), CmpOp("==", Float(4.0))),
          Expr(Call(Attribute(Name("letter_grades"), "append"), Str("A+"))),
          If(Compare(Name("grade"), CmpOp(">", Float(3.7))),
            Expr(Call(Attribute(Name("letter_grades"), "append"), Str("A"))),
            If(Compare(Name("grade"), CmpOp(">", Float(3.3))),
              Expr(Call(Attribute(Name("letter_grades"), "append"), Str("A-"))),
              If(Compare(Name("grade"), CmpOp(">", Float(3.0))),
                Expr(Call(Attribute(Name("letter_grades"), "append"), Str("B+"))),
                If(Compare(Name("grade"), CmpOp(">", Float(2.7))),
                  Expr(Call(Attribute(Name("letter_grades"), "append"), Str("B"))),
                  If(Compare(Name("grade"), CmpOp(">", Float(2.3))),
                    Expr(Call(Attribute(Name("letter_grades"), "append"), Str("B-"))),
                    If(Compare(Name("grade"), CmpOp(">", Float(2.0))),
                      Expr(Call(Attribute(Name("letter_grades"), "append"), Str("C+"))),
                      If(Compare(Name("grade"), CmpOp(">", Float(1.7))),
                        Expr(Call(Attribute(Name("letter_grades"), "append"), Str("C"))),
                        If(Compare(Name("grade"), CmpOp(">", Float(1.3))),
                          Expr(Call(Attribute(Name("letter_grades"), "append"), Str("C-"))),
                          If(Compare(Name("grade"), CmpOp(">", Float(1.0))),
                            Expr(Call(Attribute(Name("letter_grades"), "append"), Str("D+"))),
                            If(Compare(Name("grade"), CmpOp(">", Float(0.7))),
                              Expr(Call(Attribute(Name("letter_grades"), "append"), Str("D"))),
                              If(Compare(Name("grade"), CmpOp(">", Float(0.0))),
                                Expr(Call(Attribute(Name("letter_grades"), "append"), Str("D-"))),
                                Expr(Call(Attribute(Name("letter_grades"), "append"), Str("E")))
                              )
                            )
                          )
                        )
                      )
                    )
                  )
                )
              )
            )
          )
        )

  syntax Module ::= "GRADE-PROGRAM" [macro]
  rule GRADE-PROGRAM
    => Module(
         FuncDef("numerical_letter_grade", Params("grades"),
           Assign(Name("letter_grades"), ListExpr(.Exprs))
           Assign(Name("grade"), Float(0.0))
           For(Name("grade"), Name("grades"), GRADE-STEP)
           Return(Name("letter_grades"))
         )
       )

  // Dynamic-domain predicate used by the claims.
  syntax Bool ::= isGradeNumber(Val) [function, total]
  rule isGradeNumber(V:Val) => isInt(V) orBool isFloat(V)

  syntax Bool ::= allGradeNumbers(ValSeq) [function, total]
  rule allGradeNumbers(.ValSeq) => true
  rule allGradeNumbers(vCons(V:Val, REST:ValSeq))
    => isGradeNumber(V) andBool allGradeNumbers(REST)

  // Total dynamic twins of MPY-FLOAT's Int/Float-vs-Float comparison cases.
  // Their constructor equations are exhaustive and disjoint. The nonnumeric
  // case totalizes the helper but is excluded by every dispatch use.
  syntax Bool ::= gradeEq(Val, Float) [function, total]
  rule gradeEq(I:Int, F:Float) => eqF(intToF(I), F)
  rule gradeEq(G:Float, F:Float) => G ==Float F
  rule gradeEq(V:Val, _:Float) => false
    requires notBool isGradeNumber(V)

  syntax Bool ::= gradeGt(Val, Float) [function, total]
  rule gradeGt(I:Int, F:Float) => gtF(intToF(I), F)
  rule gradeGt(G:Float, F:Float) => gtF(G, F)
  rule gradeGt(V:Val, _:Float) => false
    requires notBool isGradeNumber(V)

  // Guarded dynamic-dispatch restatements of the fixed MPY equations.
  rule applyCmp("==", V:Val, F:Float)
    => gradeEq(V, F)
    requires isGradeNumber(V)
    [simplification]
  rule applyCmp(">", V:Val, F:Float)
    => gradeGt(V, F)
    requires isGradeNumber(V)
    [simplification]

  // The single-element grading table, expressed with the same comparison
  // atoms that fixed MPY execution produces.
  syntax Val ::= gradeValue(Val) [function, total]
  rule gradeValue(V:Val)
    => #if gradeEq(V, 4.0)
       #then str(strToCodes("A+"))
       #else #if gradeGt(V, 3.7)
             #then str(strToCodes("A"))
             #else #if gradeGt(V, 3.3)
                   #then str(strToCodes("A-"))
                   #else #if gradeGt(V, 3.0)
                         #then str(strToCodes("B+"))
                         #else #if gradeGt(V, 2.7)
                               #then str(strToCodes("B"))
                               #else #if gradeGt(V, 2.3)
                                     #then str(strToCodes("B-"))
                                     #else #if gradeGt(V, 2.0)
                                           #then str(strToCodes("C+"))
                                           #else #if gradeGt(V, 1.7)
                                                 #then str(strToCodes("C"))
                                                 #else #if gradeGt(V, 1.3)
                                                       #then str(strToCodes("C-"))
                                                       #else #if gradeGt(V, 1.0)
                                                             #then str(strToCodes("D+"))
                                                             #else #if gradeGt(V, 0.7)
                                                                   #then str(strToCodes("D"))
                                                                   #else #if gradeGt(V, 0.0)
                                                                         #then str(strToCodes("D-"))
                                                                         #else str(strToCodes("E"))
                                                                         #fi
                                                                   #fi
                                                             #fi
                                                       #fi
                                                 #fi
                                           #fi
                                     #fi
                               #fi
                         #fi
                   #fi
             #fi
       #fi

  // Tail-recursive result summary. Its step is exactly one list append
  // followed by grading the remaining finite suffix.
  syntax ValSeq ::= gradeAcc(ValSeq, ValSeq) [function, total]
  rule gradeAcc(ACC:ValSeq, .ValSeq) => ACC
  rule gradeAcc(ACC:ValSeq, vCons(V:Val, REST:ValSeq))
    => gradeAcc(
         valSeqConcat(ACC, vCons(gradeValue(V), .ValSeq)),
         REST
       )
endmodule
