requires "reference-semantics/semantics.k"

module AUDIT-MEDIAN-PROGRAM-MUTANT
  imports MPY

  syntax Val ::= "auditSolutionClosure" [function, total]
  rule auditSolutionClosure
    => closureVal(
      "l",
      Assign(Name("ordered"), Call(Name("sorted"), Name("l")))
          Assign(Name("size"), Call(Name("len"), Name("ordered")))
          If(Compare(BinOp("%", Name("size"), Int(2)), CmpOp("==", Int(1))),
            Return(Int(0)),
            Return(
              BinOp(
                "/",
                BinOp(
                  "+",
                  Subscript(
                    Name("ordered"),
                    BinOp("-", BinOp("//", Name("size"), Int(2)), Int(1))),
                  Subscript(
                    Name("ordered"),
                    BinOp("//", Name("size"), Int(2)))),
                Int(2)))),
      0)
endmodule
