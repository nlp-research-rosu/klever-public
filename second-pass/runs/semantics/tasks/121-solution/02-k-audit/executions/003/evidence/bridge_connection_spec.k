requires "/audit-output/evidence/bridge_free_verification.k"

module BRIDGE-CONNECTION-SPEC
  imports BRIDGE-FREE-VERIFICATION

  claim [mod-connection]:
    <k>
      BinOp("%", V:Val, I:Int) ~> KONT:K
      =>
      pyMod(intProjectionBF(V), I) ~> KONT
    </k>
    requires isInt(V)

  claim [add-connection]:
    <k>
      BinOp("+", I:Int, V:Val) ~> KONT:K
      =>
      I +Int intProjectionBF(V) ~> KONT
    </k>
    requires isInt(V)

  claim [mul-connection]:
    <k>
      BinOp("*", V:Val, I:Int) ~> KONT:K
      =>
      intProjectionBF(V) *Int I ~> KONT
    </k>
    requires isInt(V)
endmodule
