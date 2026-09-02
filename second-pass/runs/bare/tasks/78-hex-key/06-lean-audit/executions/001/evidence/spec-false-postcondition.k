requires "verification.k"

module HEX-KEY-SPEC-FALSE-POST
  imports VERIFICATION

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
                Call(Attribute(Name("num"), "count"), Str("D"))))))
        ~> #invoke("hex_key", S:String)
        => .K
      </k>
      <env> .Map => "num" |-> strVal(S) </env>
      <result> noResult => intVal(primeHexCount(S) +Int 1) </result>
    </hexKey>
endmodule
