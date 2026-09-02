requires "verification.k"

module HEX-KEY-SPEC
  imports VERIFICATION

  // Total functional correctness for every valid input (the prompt says every
  // input is an uppercase hexadecimal String or the empty String).  Proving a
  // stronger all-String statement is harmless and covers that precondition.
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
      <result> noResult => intVal(primeHexCount(S)) </result>
    </hexKey>
endmodule
