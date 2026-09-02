requires "reference-semantics/semantics.k"

module VERIFICATION-NO-SPLIT
  imports MPY

  // A proof-only representation of a string whose whitespace split is TS.
  // It lets claims quantify over token contents while retaining the supplied
  // split and loop semantics for the implementation itself.
  syntax IntSeq ::= tokenText(ValSeq) [constructor]

  // The translated solution plus one oracle assertion.  This macro is kept
  // byte-for-byte structurally aligned with solution.mpy.
  syntax Module ::= histogramCheck(Expr, Expr) [macro]
  rule histogramCheck(INPUT:Expr, EXPECTED:Expr)
    => Module(
         FuncDef("histogram", Params("test"),
           Assign(Name("counts"), DictExpr(.Entries))
           Assign(Name("maximum"), Int(0))
           For(Name("letter"), Call(Attribute(Name("test"), "split"), .Exprs),
             If(Compare(
               Name("letter"),
               CmpOp("in", Call(Attribute(Name("counts"), "keys"), .Exprs))),
               Assign(
                 Subscript(Name("counts"), Name("letter")),
                 BinOp("+", Subscript(Name("counts"), Name("letter")), Int(1))),
               Assign(Subscript(Name("counts"), Name("letter")), Int(1)))
             If(Compare(
               Subscript(Name("counts"), Name("letter")),
               CmpOp(">", Name("maximum"))),
               Assign(
                 Name("maximum"),
                 Subscript(Name("counts"), Name("letter"))),
               .Stmts))
           Assign(Name("result"), DictExpr(.Entries))
           For(Name("letter"), Call(Attribute(Name("counts"), "keys"), .Exprs),
             If(Compare(
               Subscript(Name("counts"), Name("letter")),
               CmpOp("==", Name("maximum"))),
               Assign(
                 Subscript(Name("result"), Name("letter")),
                 Subscript(Name("counts"), Name("letter"))),
               .Stmts))
           Return(Name("result")))
         Assert(Compare(
           Call(Name("histogram"), INPUT),
           CmpOp("==", EXPECTED))))
endmodule
