requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation.  The satisfying input encodes 1 + 2, whose
  // Python and K result is 3; the destination is deliberately changed to 4.
  claim
    <k> solutionProgram ~> invoke => answer(4) ... </k>
    <operators>
      ops(Op("+", .Ops))
    </operators>
    <operands>
      ints(Num(1, Num(2, .Ints)))
    </operands>
    <expression>
      noText
      => builder(
           Op("+", .Ops),
           Num(1, Num(2, .Ints)),
           .Ops,
           .Ints)
    </expression>
endmodule
