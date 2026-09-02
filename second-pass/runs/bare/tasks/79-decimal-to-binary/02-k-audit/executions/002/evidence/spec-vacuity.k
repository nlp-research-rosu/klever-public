requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh result-obligation mutation. Witness I = 0 satisfies the precondition:
  // the executed program returns "db0db", not the demanded "db0dbx".
  claim [false-extra-suffix]:
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
    <result>
      .K => strVal(decimalToBinarySpec(I) +String "x")
    </result>
    requires I >=Int 0
endmodule
