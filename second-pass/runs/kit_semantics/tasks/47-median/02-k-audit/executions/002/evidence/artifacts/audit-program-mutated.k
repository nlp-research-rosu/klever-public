requires "reference-semantics/semantics.k"

module AUDIT-MEDIAN-MUTATED
  imports MPY

  syntax Val ::= "solutionMedianClosureMutated" [function, total]
  rule solutionMedianClosureMutated
    => closureVal(
      "l",
      Expr(
            Str(
              "Return median of elements in the list l.\n    >>> median([3, 1, 2, 4, 5])\n    3\n    >>> median([-10, 4, 6, 1000, 10, 20])\n    15.0\n    "))
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
