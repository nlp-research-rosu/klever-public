requires "bridge-connection.k"

module BRIDGE-DOMAIN-SPEC
  imports BRIDGE-CONNECTION

  // Reviewer-authored connection claims over the bridges' exact Val-typed,
  // isInt-guarded match domain, not merely syntactically Int-typed operands.
  claim [plus-exact-domain]:
    <k>
      applyBin("+", A:Val, B:Val)
      => intValConnection(A) +Int intValConnection(B)
    </k>
    requires isInt(A) andBool isInt(B)

  claim [times-exact-domain]:
    <k>
      applyBin("*", A:Val, B:Val)
      => intValConnection(A) *Int intValConnection(B)
    </k>
    requires isInt(A) andBool isInt(B)
endmodule
