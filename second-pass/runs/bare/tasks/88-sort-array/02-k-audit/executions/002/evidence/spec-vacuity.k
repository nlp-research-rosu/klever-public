requires "semantic.k"

module SPEC-VACUITY
  imports MPY
  imports MPY-VERIFICATION

  // Empty-list case.  In particular, short-circuit `and` prevents either
  // subscript from being evaluated.
  claim [empty]:
    <k>
      Module(
        FuncDef("sort_array", Params("array"),
          Return(
            Call(
              Name("sorted"),
              Name("array"),
              KwArg(
                "reverse",
                BoolOp(
                  "and",
                  Compare(
                    Call(Name("len"), Name("array")),
                    CmpOp(">", Int(0))),
                  Compare(
                    BinOp(
                      "%",
                      BinOp(
                        "+",
                        Subscript(Name("array"), Int(0)),
                        Subscript(Name("array"), UnaryOp("-", Int(1)))),
                      Int(2)),
                    CmpOp("==", Int(0)))))))))
      ~> invoke("sort_array", ListVal(nil))
      => .K
    </k>
    <input> ListVal(nil) </input>
    <result> NoneVal => ListVal(nil) </result>

  // Complete nonempty case, symbolic in the first element and arbitrary
  // tail.  expectedSort independently states the endpoint-parity contract.
  // The unchanged input cell is part of the postcondition.
  claim [symbolic-nonempty]:
    <k>
      Module(
        FuncDef("sort_array", Params("array"),
          Return(
            Call(
              Name("sorted"),
              Name("array"),
              KwArg(
                "reverse",
                BoolOp(
                  "and",
                  Compare(
                    Call(Name("len"), Name("array")),
                    CmpOp(">", Int(0))),
                  Compare(
                    BinOp(
                      "%",
                      BinOp(
                        "+",
                        Subscript(Name("array"), Int(0)),
                        Subscript(Name("array"), UnaryOp("-", Int(1)))),
                      Int(2)),
                    CmpOp("==", Int(0)))))))))
      ~> invoke("sort_array", ListVal(cons(F, REST)))
      => .K
    </k>
    <input> ListVal(cons(F, REST)) </input>
    <result> NoneVal => ListVal(expectedSort(cons(F, REST))) </result>
    requires nonnegative(cons(F, REST))

  // Prompt examples are also executable proof claims.  These make the two
  // parity branches and the concrete insertion-sort behavior immediately
  // inspectable in proof output.
  claim [example-ascending]:
    <k>
      Module(
        FuncDef("sort_array", Params("array"),
          Return(
            Call(
              Name("sorted"), Name("array"),
              KwArg("reverse",
                BoolOp("and",
                  Compare(Call(Name("len"), Name("array")), CmpOp(">", Int(0))),
                  Compare(
                    BinOp("%",
                      BinOp("+", Subscript(Name("array"), Int(0)),
                        Subscript(Name("array"), UnaryOp("-", Int(1)))),
                      Int(2)),
                    CmpOp("==", Int(0)))))))))
      ~> invoke("sort_array",
           ListVal(cons(2, cons(4, cons(3, cons(0, cons(1, cons(5, nil))))))))
      => .K
    </k>
    <input>
      ListVal(cons(2, cons(4, cons(3, cons(0, cons(1, cons(5, nil)))))))
    </input>
    <result>
      NoneVal
      => ListVal(cons(5, cons(4, cons(3, cons(2, cons(1, cons(0, nil)))))))
    </result>

  claim [example-descending]:
    <k>
      Module(
        FuncDef("sort_array", Params("array"),
          Return(
            Call(
              Name("sorted"), Name("array"),
              KwArg("reverse",
                BoolOp("and",
                  Compare(Call(Name("len"), Name("array")), CmpOp(">", Int(0))),
                  Compare(
                    BinOp("%",
                      BinOp("+", Subscript(Name("array"), Int(0)),
                        Subscript(Name("array"), UnaryOp("-", Int(1)))),
                      Int(2)),
                    CmpOp("==", Int(0)))))))))
      ~> invoke("sort_array",
           ListVal(cons(2, cons(4, cons(3, cons(0, cons(1, cons(5, cons(6, nil)))))))))
      => .K
    </k>
    <input>
      ListVal(cons(2, cons(4, cons(3, cons(0, cons(1, cons(5, cons(6, nil))))))))
    </input>
    <result>
      NoneVal
      => ListVal(cons(6, cons(5, cons(4, cons(3, cons(2, cons(1, cons(0, nil))))))))
    </result>
endmodule
