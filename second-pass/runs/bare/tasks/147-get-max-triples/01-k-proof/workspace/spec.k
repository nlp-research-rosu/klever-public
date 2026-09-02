requires "verification.k"

module SPEC
  imports VERIFICATION

  claim
      <k>
        Module(FuncDef("get_max_triples", Params("n"),
          Return(
            BinOp("+",
              BinOp("//",
                BinOp("*",
                  BinOp("*",
                    BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3)),
                    BinOp("-",
                      BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3)),
                      Int(1))),
                  BinOp("-",
                    BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3)),
                    Int(2))),
                Int(6)),
              BinOp("//",
                BinOp("*",
                  BinOp("*",
                    BinOp("-", Name("n"),
                      BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3))),
                    BinOp("-",
                      BinOp("-", Name("n"),
                        BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3))),
                      Int(1))),
                  BinOp("-",
                    BinOp("-", Name("n"),
                      BinOp("//", BinOp("+", Name("n"), Int(1)), Int(3))),
                    Int(2))),
                Int(6))))))
        => .K
      </k>
      <input> N </input>
      <env> .Map => "n" |-> N </env>
      <result> noResult => result(validTripleCount(N)) </result>
    requires N >=Int 1
endmodule
