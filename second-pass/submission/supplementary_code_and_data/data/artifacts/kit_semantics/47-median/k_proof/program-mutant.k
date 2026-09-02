requires "reference-semantics/semantics.k"

module MEDIAN-PROGRAM-MUTANT
  imports MPY

  syntax Val ::= "solutionMedianClosureMutant" [function, total]
  rule solutionMedianClosureMutant
    => closureVal(
      "l",
      Expr(
            Str(
              "Gate A body-sensitivity mutant: the odd result is deliberately wrong."))
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
