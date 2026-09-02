requires "semantic.k"

module VERIFICATION
  imports MPY

  // Declarative maximality check over a finite interval.  It says that every
  // candidate from LO through HI fails to divide N.
  syntax Bool ::= noDivisorFrom(Int, Int, Int) [function]
  rule noDivisorFrom(_, LO, HI) => true
    requires LO >Int HI
  rule noDivisorFrom(N, LO, HI)
    => (N modInt LO =/=Int 0) andBool noDivisorFrom(N, LO +Int 1, HI)
    requires LO <=Int HI

  syntax Bool ::= isLargestThrough(Int, Int, Int) [function]
  rule isLargestThrough(N, D, UPPER)
    => D >Int 0
       andBool D <=Int UPPER
       andBool N modInt D ==Int 0
       andBool noDivisorFrom(N, D +Int 1, UPPER)

  syntax Bool ::= isLargestProperDivisor(Int, Int) [function]
  rule isLargestProperDivisor(N, D)
    => D <Int N andBool isLargestThrough(N, D, N -Int 1)
endmodule
