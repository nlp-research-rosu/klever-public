requires "verification-bridgefree.k"

module SPEC-BRIDGE-CONNECTIONS
  imports VERIFICATION-BRIDGEFREE

  claim [mod-connection]:
    <k>
      BinOp("%", V:Val, I:Int) ~> KONT:K
      =>
      pyMod(intProjection(V), I) ~> KONT
    </k>
    requires isInt(V)

  claim [add-connection]:
    <k>
      BinOp("+", I:Int, V:Val) ~> KONT:K
      =>
      I +Int intProjection(V) ~> KONT
    </k>
    requires isInt(V)

  claim [mul-connection]:
    <k>
      BinOp("*", V:Val, I:Int) ~> KONT:K
      =>
      intProjection(V) *Int I ~> KONT
    </k>
    requires isInt(V)

  // Typed-domain controls: these cover every ground match admitted by isInt,
  // but are narrower syntactically than the candidate's symbolic Val patterns.
  claim [mod-typed]:
    <k>
      BinOp("%", J:Int, 2) ~> KONT:K
      =>
      pyMod(J, 2) ~> KONT
    </k>

  claim [add-typed]:
    <k>
      BinOp("+", I:Int, J:Int) ~> KONT:K
      =>
      I +Int J ~> KONT
    </k>

  claim [mul-typed]:
    <k>
      BinOp("*", J:Int, I:Int) ~> KONT:K
      =>
      J *Int I ~> KONT
    </k>
endmodule
