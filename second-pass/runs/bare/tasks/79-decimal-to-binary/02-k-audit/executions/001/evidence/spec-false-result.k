requires "verification.k"

module AUDIT-SPEC-FALSE-RESULT
  imports VERIFICATION

  // Fresh false mutation: the submitted program returns db1111db for 15.
  claim
    <k>
      Module(
        FuncDef(
          "decimal_to_binary",
          Params("decimal"),
          Return(
            BinOp(
              "+",
              BinOp(
                "+",
                Str("db"),
                Subscript(
                  Call(Name("bin"), Name("decimal")),
                  Slice(Int(2), NoBound, NoBound)
                )
              ),
              Str("db")
            )
          )
        )
      )
    => .K
    </k>
    <arg> 15 </arg>
    <result> .K => strVal("db1110db") </result>
endmodule
