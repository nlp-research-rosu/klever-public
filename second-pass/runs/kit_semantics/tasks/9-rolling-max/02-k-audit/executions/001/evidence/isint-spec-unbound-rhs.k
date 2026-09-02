requires "isint-base.k"

module ISINT-SPEC
  imports ISINT-BASE

  claim [is-int-inversion]:
    <k>
      V:Val
      =>
      I:Int
    </k>
    requires isInt(V)
endmodule
