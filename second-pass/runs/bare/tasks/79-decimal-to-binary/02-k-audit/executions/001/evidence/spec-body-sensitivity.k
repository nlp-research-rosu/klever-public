requires "verification.k"

module AUDIT-SPEC-BODY-SENSITIVITY
  imports VERIFICATION

  // This is deliberately not the submitted body. Fixed semantics must expose it.
  claim
    <k>
      Module(
        FuncDef(
          "decimal_to_binary",
          Params("decimal"),
          Return(Str("changed"))
        )
      )
    => .K
    </k>
    <arg> 15 </arg>
    <result> .K => strVal("db1111db") </result>
endmodule
