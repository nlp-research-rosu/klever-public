requires "semantic.k"

module SPEC-EXAMPLE-EVEN-ONLY
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
      <input>
        cons(-10, cons(4, cons(6, cons(1000, cons(10, cons(20, nil))))))
      </input>
      <result> noResult => floatVal(30, 2) </result>
    </median>
endmodule
