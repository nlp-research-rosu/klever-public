requires "verification.k"

module PRECONDITION-WITNESS
  imports VERIFICATION

  claim
    <k>
      aligned(
        Op("+", Op("*", Op("-", .Ops))),
        Num(3, Num(4, Num(5, .Ints))))
      andBool validOps(Op("+", Op("*", Op("-", .Ops))))
      andBool nonNegative(Num(2, Num(3, Num(4, Num(5, .Ints)))))
      => true ...
    </k>
endmodule
