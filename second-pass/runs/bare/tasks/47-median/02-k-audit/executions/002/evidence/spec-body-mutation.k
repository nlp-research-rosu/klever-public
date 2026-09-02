requires "semantic.k"

module SPEC-BODY-MUTATION
  imports MEDIAN-VERIFICATION

  // Main correctness theorem: execution of the translated solution refines
  // the independently stated promptMedian reference for every integer list
  // in the implementation's safe domain (at least three elements).
  claim [main]:
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
                      BinOp("+", Name("middle"), Int(0)))),
                  Int(2))))))
        => .K
      </k>
      <input> IS:Ints </input>
      <result> noResult => promptMedian(IS) </result>
    </median>
    requires lenInts(IS) >=Int 3

  // The two examples in prompt.py are retained as direct end-to-end claims.
  claim [example-odd]:
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
                      BinOp("+", Name("middle"), Int(0)))),
                  Int(2))))))
        => .K
      </k>
      <input>
        cons(3, cons(1, cons(2, cons(4, cons(5, nil)))))
      </input>
      <result> noResult => intVal(3) </result>
    </median>

  claim [example-even]:
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
                      BinOp("+", Name("middle"), Int(0)))),
                  Int(2))))))
        => .K
      </k>
      <input>
        cons(-10, cons(4, cons(6, cons(1000, cons(10, cons(20, nil))))))
      </input>
      <result> noResult => floatVal(30, 2) </result>
    </median>
endmodule
