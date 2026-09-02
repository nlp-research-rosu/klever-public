requires "semantic.k"

module VERIFICATION
  imports SEMANTIC
  imports K-EQUAL

  // Independent mathematical contract: starting from balance B, report
  // whether some running prefix makes the balance negative.
  syntax Bool ::= belowZeroFrom(Int, IntList) [function, total]

  rule belowZeroFrom(_, .IntList) => false
  rule belowZeroFrom(B, cons(I, IS))
    => #if B +Int I <Int 0
       #then true
       #else belowZeroFrom(B +Int I, IS)
       #fi
endmodule
