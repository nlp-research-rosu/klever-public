requires "semantic.k"

module SOLUTION-PROGRAM
  imports MPY

  // prove.sh regenerates solution.mpy and checks that this proof constant and
  // the actual translator output produce identical KORE after module loading.
  rule solutionProgram =>
    Module(
      FuncDef("_water_in", Params("row"),
        Return(
          IfExp(
            Compare(Name("row"), CmpOp("==", ListExpr(.ExprList))),
            Int(0),
            BinOp(
              "+",
              Subscript(Name("row"), Int(0)),
              Call(
                Name("_water_in"),
                Subscript(Name("row"), Slice(Int(1), NoBound, NoBound)))))))
      FuncDef("_buckets_for", Params("grid", "capacity"),
        Return(
          IfExp(
            Compare(Name("grid"), CmpOp("==", ListExpr(.ExprList))),
            Int(0),
            BinOp(
              "+",
              BinOp(
                "//",
                BinOp(
                  "-",
                  BinOp(
                    "+",
                    Call(Name("_water_in"), Subscript(Name("grid"), Int(0))),
                    Name("capacity")),
                  Int(1)),
                Name("capacity")),
              Call(
                Name("_buckets_for"),
                Subscript(Name("grid"), Slice(Int(1), NoBound, NoBound)),
                Name("capacity"))))))
      FuncDef("max_fill", Params("grid", "capacity"),
        Return(Call(Name("_buckets_for"), Name("grid"), Name("capacity")))))
endmodule
