requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // These macros expand to exactly the body emitted in solution.mpy.
  syntax Stmt ::= "numericalLetterGradeStep" [macro]
  rule numericalLetterGradeStep
    => If(Compare(Name("grade"), CmpOp("==", Float(4.0))),
           Expr(Call(Attribute(Name("result"), "append"),
                     (Str("A+"), .Exprs))),
           If(Compare(Name("grade"), CmpOp(">", Float(3.7))),
             Expr(Call(Attribute(Name("result"), "append"),
                       (Str("A"), .Exprs))),
             If(Compare(Name("grade"), CmpOp(">", Float(3.3))),
               Expr(Call(Attribute(Name("result"), "append"),
                         (Str("A-"), .Exprs))),
               If(Compare(Name("grade"), CmpOp(">", Float(3.0))),
                 Expr(Call(Attribute(Name("result"), "append"),
                           (Str("B+"), .Exprs))),
                 If(Compare(Name("grade"), CmpOp(">", Float(2.7))),
                   Expr(Call(Attribute(Name("result"), "append"),
                             (Str("B"), .Exprs))),
                   If(Compare(Name("grade"), CmpOp(">", Float(2.3))),
                     Expr(Call(Attribute(Name("result"), "append"),
                               (Str("B-"), .Exprs))),
                     If(Compare(Name("grade"), CmpOp(">", Float(2.0))),
                       Expr(Call(Attribute(Name("result"), "append"),
                                 (Str("C+"), .Exprs))),
                       If(Compare(Name("grade"), CmpOp(">", Float(1.7))),
                         Expr(Call(Attribute(Name("result"), "append"),
                                   (Str("C"), .Exprs))),
                         If(Compare(Name("grade"), CmpOp(">", Float(1.3))),
                           Expr(Call(Attribute(Name("result"), "append"),
                                     (Str("C-"), .Exprs))),
                           If(Compare(Name("grade"), CmpOp(">", Float(1.0))),
                             Expr(Call(Attribute(Name("result"), "append"),
                                       (Str("D+"), .Exprs))),
                             If(Compare(Name("grade"), CmpOp(">", Float(0.7))),
                               Expr(Call(Attribute(Name("result"), "append"),
                                         (Str("D"), .Exprs))),
                               If(Compare(Name("grade"), CmpOp(">", Float(0.0))),
                                 Expr(Call(Attribute(Name("result"), "append"),
                                           (Str("D-"), .Exprs))),
                                 Expr(Call(Attribute(Name("result"), "append"),
                                           (Str("E"), .Exprs)))))))))))))))

  syntax Stmts ::= "numericalLetterGradeBody" [macro]
  rule numericalLetterGradeBody
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("grade"), Float(0.0))
       For(Name("grade"), Name("grades"),
         Assign(Name("grade"),
           Call(Name("float"), (Name("grade"), .Exprs)))
         numericalLetterGradeStep)
       Return(Name("result"))

  syntax KItem ::= runGrades(ValSeq)
  rule <k> runGrades(VS:ValSeq)
        => #applyK(
             toCall(closureVal("grades", numericalLetterGradeBody, 0)),
             (list(VS), .Vals))
        ... </k>

  syntax Val ::= letter(String) [function, total]
  rule letter(S:String) => str(strToCodes(S))

  syntax Bool ::= eqFour(Float) [function, total]
                | above(Float, Float) [function, total]
  syntax Bool ::= gpaEqFour(Val)
                  [function, total, symbol(gpaEqFour), no-evaluators]
  rule <k> Compare(F:Float, CmpOp("==", 4.0))
        => gpaEqFour(F)
        ... </k>
       [priority(40)]
  rule eqFour(F:Float)  => gpaEqFour(F)
  rule above(F:Float, T:Float) => gtF(F, T)

  // A symbolic numeric-list domain and its mathematical map.  mappedAppend mirrors
  // append's left-to-right accumulator shape, which gives the loop invariant
  // an induction-friendly postcondition.
  syntax NumericGrades ::= ".NumericGrades"
                         | fGrade(Float, NumericGrades)
                         | iGrade(Int, NumericGrades)
  syntax ValSeq ::= numericValues(NumericGrades)
  rule <k> #iterNext(list(numericValues(.NumericGrades)))
        => #iterDone
        ... </k>
       [priority(40)]
  rule <k> #iterNext(list(numericValues(fGrade(F:Float, GS:NumericGrades))))
        => #iterYield(F, list(numericValues(GS)))
        ... </k>
       [priority(40)]
  rule <k> #iterNext(list(numericValues(iGrade(I:Int, GS:NumericGrades))))
        => #iterYield(I, list(numericValues(GS)))
        ... </k>
       [priority(40)]

  syntax Val ::= gradeOf(Float) [function]
  rule gradeOf(F:Float) => letter("A+")
    requires eqFour(F)
  rule gradeOf(F:Float) => letter("A")
    requires notBool eqFour(F)
     andBool above(F, 3.7)
  rule gradeOf(F:Float) => letter("A-")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool above(F, 3.3)
  rule gradeOf(F:Float) => letter("B+")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool above(F, 3.0)
  rule gradeOf(F:Float) => letter("B")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool above(F, 2.7)
  rule gradeOf(F:Float) => letter("B-")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool above(F, 2.3)
  rule gradeOf(F:Float) => letter("C+")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool notBool above(F, 2.3)
     andBool above(F, 2.0)
  rule gradeOf(F:Float) => letter("C")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool notBool above(F, 2.3)
     andBool notBool above(F, 2.0)
     andBool above(F, 1.7)
  rule gradeOf(F:Float) => letter("C-")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool notBool above(F, 2.3)
     andBool notBool above(F, 2.0)
     andBool notBool above(F, 1.7)
     andBool above(F, 1.3)
  rule gradeOf(F:Float) => letter("D+")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool notBool above(F, 2.3)
     andBool notBool above(F, 2.0)
     andBool notBool above(F, 1.7)
     andBool notBool above(F, 1.3)
     andBool above(F, 1.0)
  rule gradeOf(F:Float) => letter("D")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool notBool above(F, 2.3)
     andBool notBool above(F, 2.0)
     andBool notBool above(F, 1.7)
     andBool notBool above(F, 1.3)
     andBool notBool above(F, 1.0)
     andBool above(F, 0.7)
  rule gradeOf(F:Float) => letter("D-")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool notBool above(F, 2.3)
     andBool notBool above(F, 2.0)
     andBool notBool above(F, 1.7)
     andBool notBool above(F, 1.3)
     andBool notBool above(F, 1.0)
     andBool notBool above(F, 0.7)
     andBool above(F, 0.0)
  rule gradeOf(F:Float) => letter("E")
    requires notBool eqFour(F)
     andBool notBool above(F, 3.7)
     andBool notBool above(F, 3.3)
     andBool notBool above(F, 3.0)
     andBool notBool above(F, 2.7)
     andBool notBool above(F, 2.3)
     andBool notBool above(F, 2.0)
     andBool notBool above(F, 1.7)
     andBool notBool above(F, 1.3)
     andBool notBool above(F, 1.0)
     andBool notBool above(F, 0.7)
     andBool notBool above(F, 0.0)

  syntax ValSeq ::= mappedAppend(ValSeq, NumericGrades) [function, total]
  rule mappedAppend(PREFIX:ValSeq, .NumericGrades) => PREFIX
  rule mappedAppend(PREFIX:ValSeq, fGrade(F:Float, GS:NumericGrades))
    => mappedAppend(
         valSeqConcat(PREFIX, vCons(gradeOf(F), .ValSeq)),
         GS)
  rule mappedAppend(PREFIX:ValSeq, iGrade(I:Int, GS:NumericGrades))
    => mappedAppend(
         valSeqConcat(PREFIX, vCons(gradeOf(intToF(I)), .ValSeq)),
         GS)

  syntax Float ::= afterGradeValue(Float, NumericGrades) [function, total]
  rule afterGradeValue(OLD:Float, .NumericGrades) => OLD
  rule afterGradeValue(_:Float, fGrade(F:Float, GS:NumericGrades))
    => afterGradeValue(F, GS)
  rule afterGradeValue(_:Float, iGrade(I:Int, GS:NumericGrades))
    => afterGradeValue(intToF(I), GS)
endmodule
