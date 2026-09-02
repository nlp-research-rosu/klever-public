requires "semantic.k"

module SPEC-MAIN-ONLY
  imports MEDIAN-VERIFICATION

  claim
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
      <input> IS:Ints </input>
      <result> noResult => promptMedian(IS) </result>
    </median>
    requires lenInts(IS) >=Int 3
endmodule
