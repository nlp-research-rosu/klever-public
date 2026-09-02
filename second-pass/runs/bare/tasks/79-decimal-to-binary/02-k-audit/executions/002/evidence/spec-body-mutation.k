requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Changes the program term that the claim actually executes: the final
  // wrapper literal is "xx", while the original result obligation is retained.
  claim [changed-final-literal]:
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
              Str("xx")
            )
          )
        )
      )
    => .K
    </k>
    <arg> I:Int </arg>
    <result> .K => strVal(decimalToBinarySpec(I)) </result>
    requires I >=Int 0
endmodule
