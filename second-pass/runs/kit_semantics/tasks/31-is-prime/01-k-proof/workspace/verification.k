requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // primeScan(N, D) states that N has no divisor in the integer interval
  // [D, N).  The D < 2 case totalizes the helper outside the proof's
  // D >= 2 domain.
  syntax Bool ::= primeScan(Int, Int) [function, total]
                | primeResult(Int)    [function, total]

  rule primeScan(_N, D) => false
    requires D <Int 2

  rule primeScan(N, D) => true
    requires D >=Int 2 andBool D >=Int N

  rule primeScan(N, D) => false
    requires D >=Int 2 andBool D <Int N
      andBool pyMod(N, D) ==Int 0

  rule primeScan(N, D) => primeScan(N, D +Int 1)
    requires D >=Int 2 andBool D <Int N
      andBool pyMod(N, D) =/=Int 0

  rule primeResult(N) => false
    requires N <Int 2

  rule primeResult(N) => primeScan(N, 2)
    requires N >=Int 2
endmodule
