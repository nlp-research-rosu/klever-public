requires "/audit-output/evidence/bridge_free_verification.k"

module BRIDGE-CONNECTION-REFINED-SPEC
  imports BRIDGE-FREE-VERIFICATION

  claim [mod-connection-refined]:
    <k>
      BinOp("%", V:Val, I:Int) ~> KONT:K
      =>
      pyMod(intProjectionBF(V), I) ~> KONT
    </k>
    requires V ==K J:Int

  claim [add-connection-refined]:
    <k>
      BinOp("+", I:Int, V:Val) ~> KONT:K
      =>
      I +Int intProjectionBF(V) ~> KONT
    </k>
    requires V ==K J:Int

  claim [mul-connection-refined]:
    <k>
      BinOp("*", V:Val, I:Int) ~> KONT:K
      =>
      intProjectionBF(V) *Int I ~> KONT
    </k>
    requires V ==K J:Int
endmodule
