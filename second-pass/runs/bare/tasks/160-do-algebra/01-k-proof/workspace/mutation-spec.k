requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  // Deliberately false: the prompt example returns 9, not 10.  prove.sh
  // requires this probe to exit nonzero, demonstrating a discriminating spec.
  claim
    <k> solutionProgram ~> invoke => answer(10) ... </k>
    <operators>
      ops(Op("+", Op("*", Op("-", .Ops))))
    </operators>
    <operands>
      ints(Num(2, Num(3, Num(4, Num(5, .Ints)))))
    </operands>
    <expression>
      noText
      => builder(
           Op("+", Op("*", Op("-", .Ops))),
           Num(2, Num(3, Num(4, Num(5, .Ints)))),
           .Ops,
           .Ints)
    </expression>
endmodule
