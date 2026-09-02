requires "isint-base.k"

module ISINT-SPEC
  imports ISINT-BASE

  claim [is-int-inversion]:
    { true #Equals isInt(V:Val) }
    =>
    #Exists I:Int . { V #Equals I }
endmodule
