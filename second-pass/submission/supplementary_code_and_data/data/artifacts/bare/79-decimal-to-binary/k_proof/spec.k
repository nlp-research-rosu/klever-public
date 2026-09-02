requires "verification.k"

module SPEC
  imports VERIFICATION

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
    <arg> I:Int </arg>
    <result> .K => strVal(decimalToBinarySpec(I)) </result>
    requires I >=Int 0

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
    <arg> I:Int </arg>
    <result> .K => strVal(decimalToBinarySpec(I)) </result>
    requires I <Int 0

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
    <result> .K => strVal("db1111db") </result>

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
    <arg> 32 </arg>
    <result> .K => strVal("db100000db") </result>

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
    <arg> -5 </arg>
    <result> .K => strVal("dbb101db") </result>
endmodule
