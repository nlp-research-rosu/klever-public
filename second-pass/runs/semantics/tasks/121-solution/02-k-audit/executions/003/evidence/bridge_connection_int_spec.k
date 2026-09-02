requires "/audit-output/evidence/bridge_free_verification.k"

module BRIDGE-CONNECTION-INT-SPEC
  imports BRIDGE-FREE-VERIFICATION

  claim [mod-connection-int-domain]:
    <k>
      BinOp("%", J:Int, I:Int) ~> KONT:K
      =>
      pyMod(J, I) ~> KONT
    </k>

  claim [add-connection-int-domain]:
    <k>
      BinOp("+", I:Int, J:Int) ~> KONT:K
      =>
      I +Int J ~> KONT
    </k>

  claim [mul-connection-int-domain]:
    <k>
      BinOp("*", J:Int, I:Int) ~> KONT:K
      =>
      J *Int I ~> KONT
    </k>
endmodule
