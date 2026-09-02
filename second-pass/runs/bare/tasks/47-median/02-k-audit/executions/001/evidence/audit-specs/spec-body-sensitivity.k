requires "semantic.k"

module SPEC-BODY-SENSITIVITY
  imports MEDIAN-VERIFICATION

  // Deliberately mutate the real program's even return from middle+1 to
  // middle+0 while retaining the original result obligation.
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
                      BinOp("+", Name("middle"), Int(0)))),
                  Int(2))))))
        => .K
      </k>
      <input> cons(1, cons(2, cons(3, cons(4, nil)))) </input>
      <result> noResult => floatVal(7, 2) </result>
    </median>
endmodule
