requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This macro is the exact constructor translation in solution.mpy.
  syntax Module ::= "solutionProgram" [macro]
  rule solutionProgram
    => Module(
         FuncDef("_evaluate", Params("operator", "operand", "start", "end", "level"),
           If(Compare(Name("level"), CmpOp("==", Int(0))),
             Assign(Name("i"), BinOp("-", Name("end"), Int(1)))
             While(Compare(Name("i"), CmpOp(">=", Name("start"))),
               If(Compare(Subscript(Name("operator"), Name("i")), CmpOp("==", Str("+"))),
                 Return(
                   BinOp("+",
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), Name("start"), Name("i"), Int(0)),
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), BinOp("+", Name("i"), Int(1)),
                       Name("end"), Int(1)))),
                 .Stmts)
               If(Compare(Subscript(Name("operator"), Name("i")), CmpOp("==", Str("-"))),
                 Return(
                   BinOp("-",
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), Name("start"), Name("i"), Int(0)),
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), BinOp("+", Name("i"), Int(1)),
                       Name("end"), Int(1)))),
                 .Stmts)
               AugAssign(Name("i"), "-", Int(1)))
             Return(Call(Name("_evaluate"),
               Name("operator"), Name("operand"), Name("start"), Name("end"), Int(1))),
             .Stmts)
           If(Compare(Name("level"), CmpOp("==", Int(1))),
             Assign(Name("i"), BinOp("-", Name("end"), Int(1)))
             While(Compare(Name("i"), CmpOp(">=", Name("start"))),
               If(Compare(Subscript(Name("operator"), Name("i")), CmpOp("==", Str("*"))),
                 Return(
                   BinOp("*",
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), Name("start"), Name("i"), Int(1)),
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), BinOp("+", Name("i"), Int(1)),
                       Name("end"), Int(2)))),
                 .Stmts)
               If(Compare(Subscript(Name("operator"), Name("i")), CmpOp("==", Str("//"))),
                 Return(
                   BinOp("//",
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), Name("start"), Name("i"), Int(1)),
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), BinOp("+", Name("i"), Int(1)),
                       Name("end"), Int(2)))),
                 .Stmts)
               AugAssign(Name("i"), "-", Int(1)))
             Return(Call(Name("_evaluate"),
               Name("operator"), Name("operand"), Name("start"), Name("end"), Int(2))),
             .Stmts)
           If(Compare(Name("level"), CmpOp("==", Int(2))),
             Assign(Name("i"), Name("start"))
             While(Compare(Name("i"), CmpOp("<", Name("end"))),
               If(Compare(Subscript(Name("operator"), Name("i")), CmpOp("==", Str("**"))),
                 Return(
                   BinOp("**",
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), Name("start"), Name("i"), Int(3)),
                     Call(Name("_evaluate"),
                       Name("operator"), Name("operand"), BinOp("+", Name("i"), Int(1)),
                       Name("end"), Int(2)))),
                 .Stmts)
               AugAssign(Name("i"), "+", Int(1)))
             Return(Call(Name("_evaluate"),
               Name("operator"), Name("operand"), Name("start"), Name("end"), Int(3))),
             .Stmts)
           Return(Subscript(Name("operand"), Name("start"))))
         FuncDef("do_algebra", Params("operator", "operand"),
           Return(Call(Name("_evaluate"),
             Name("operator"), Name("operand"), Int(0),
             Call(Name("len"), Name("operator")), Int(0)))))

  // Values for the five operator tokens. Claims use bare list values as
  // read-only arguments, which the supplied semantics explicitly supports.
  syntax Str ::= "plusV" [macro]
               | "minusV" [macro]
               | "timesV" [macro]
               | "floorDivV" [macro]
               | "powerV" [macro]
  rule plusV     => str(iCons(43, .IntSeq))
  rule minusV    => str(iCons(45, .IntSeq))
  rule timesV    => str(iCons(42, .IntSeq))
  rule floorDivV => str(iCons(47, iCons(47, .IntSeq)))
  rule powerV    => str(iCons(42, iCons(42, .IntSeq)))

  // Mathematical floor quotient used only to state expected results.
  syntax Int ::= floorQuot(Int, Int) [function, total]
  rule floorQuot(A:Int, B:Int) => (A -Int pyMod(A, B)) /Int B

  syntax KItem ::= runDoAlgebra(ValSeq, ValSeq)
  rule <k> runDoAlgebra(OPS:ValSeq, NDS:ValSeq)
        => #loadAll(solutionProgram)
           ~> Call(Name("do_algebra"), list(OPS), list(NDS))
        ... </k>
endmodule
