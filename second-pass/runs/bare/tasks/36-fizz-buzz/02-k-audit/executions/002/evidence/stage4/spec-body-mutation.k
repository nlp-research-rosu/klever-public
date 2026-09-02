requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Ground body-sensitivity check. The executed constructor term increments
  // count by 2 for each digit 7, so at N=78 it returns 4, not the claimed 2.
  claim <fizz>
          <k>
            Module(
              FuncDef("fizz_buzz", Params("n"),
                Assign(Name("count"), Int(0))
                Assign(Name("i"), Int(0))
                While(Compare(Name("i"), CmpOp("<", Name("n"))),
                  If(BoolOp("or",
                      Compare(BinOp("%", Name("i"), Int(11)),
                              CmpOp("==", Int(0))),
                      Compare(BinOp("%", Name("i"), Int(13)),
                              CmpOp("==", Int(0)))),
                    Assign(Name("x"), Name("i"))
                    While(Compare(Name("x"), CmpOp(">", Int(0))),
                      If(Compare(BinOp("%", Name("x"), Int(10)),
                                 CmpOp("==", Int(7))),
                        Assign(Name("count"),
                          BinOp("+", Name("count"), Int(2))),
                        .Stmts)
                      Assign(Name("x"),
                        BinOp("//", Name("x"), Int(10)))),
                    .Stmts)
                  Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
                Return(Name("count"))))
            => .K
          </k>
          <input> 78 </input>
          <env> .Map =>
            "count" |-> 4
            "i" |-> 78
            "n" |-> 78
            "x" |-> 0
          </env>
          <result> 0 => 2 </result>
        </fizz>
endmodule
