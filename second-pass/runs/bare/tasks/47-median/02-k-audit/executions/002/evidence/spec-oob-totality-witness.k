requires "semantic.k"

module SPEC-OOB-TOTALITY-WITNESS
  imports MEDIAN-VERIFICATION

  claim [length-two-normal-return]:
    <median>
      <k>
        Module(
          FuncDef("median", Params("l"),
            Assign(Name("ordered"), Call(Name("sorted"), Name("l")))
            Assign(
              Name("middle"),
              BinOp("//", Call(Name("len"), Name("ordered")), Int(2)))
            If(BinOp("%", Call(Name("len"), Name("ordered")), Int(2)),
              Return(Subscript(Name("ordered"), Name("middle"))),
              Return(
                BinOp(
                  "/",
                  BinOp(
                    "+",
                    Subscript(Name("ordered"), Name("middle")),
                    Subscript(
                      Name("ordered"),
                      BinOp("+", Name("middle"), Int(1)))),
                  Int(2))))))
        => .K
      </k>
      <input> cons(2, cons(10, nil)) </input>
      <result>
        noResult
        => floatVal(10 +Int nthInt(nil, 0), 2)
      </result>
    </median>
endmodule
