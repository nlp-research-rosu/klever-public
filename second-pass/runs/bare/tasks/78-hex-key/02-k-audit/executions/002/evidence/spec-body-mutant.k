requires "verification.k"

module HEX-KEY-SPEC-BODY-MUTANT
  imports VERIFICATION

  // Reviewer mutation: the executed body counts E instead of D, while the
  // target result remains primeHexCount(S). False for S = "D" (also for "E").
  claim
    <hexKey>
      <k>
        Module(
          FuncDef("hex_key", Params("num"),
            Return(
              BinOp("+",
                BinOp("+",
                  BinOp("+",
                    BinOp("+",
                      BinOp("+",
                        Call(Attribute(Name("num"), "count"), Str("2")),
                        Call(Attribute(Name("num"), "count"), Str("3"))),
                      Call(Attribute(Name("num"), "count"), Str("5"))),
                    Call(Attribute(Name("num"), "count"), Str("7"))),
                  Call(Attribute(Name("num"), "count"), Str("B"))),
                Call(Attribute(Name("num"), "count"), Str("E"))))))
        ~> #invoke("hex_key", S:String)
        => .K
      </k>
      <env> .Map => "num" |-> strVal(S) </env>
      <result> noResult => intVal(primeHexCount(S)) </result>
    </hexKey>
endmodule
