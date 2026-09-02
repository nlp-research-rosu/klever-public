requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation: require the exact executed program to return one
  // more than its fully defined mathematical contract.
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
      <result>
        noResult => result(validTripleCount(N) +Int 1)
      </result>
    requires N >=Int 1
endmodule
