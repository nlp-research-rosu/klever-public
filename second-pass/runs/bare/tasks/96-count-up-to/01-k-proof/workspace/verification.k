requires "semantic.k"

module VERIFICATION
  imports MPY

  // noFactor(C,D) states that C has no divisor in the closed interval
  // [D, floor(sqrt(C))].  These three equations are disjoint and total for
  // C >= 2 and D >= 2, precisely the domain used by the implementation.
  syntax Bool ::= "noFactor" "(" Int "," Int ")" [function, total]

  rule noFactor(C, D) => true
       requires D *Int D >Int C

  rule noFactor(C, D) => false
       requires D *Int D <=Int C
        andBool C %Int D ==Int 0
        andBool D =/=Int 0

  rule noFactor(C, D) => noFactor(C, D +Int 1)
       requires D *Int D <=Int C
        andBool C %Int D =/=Int 0
        andBool D =/=Int 0

  // Mathematical prime predicate and the ascending list of all primes in
  // [C,N).  primesBelow(N) is the task's required result.
  syntax Bool ::= "isPrime" "(" Int ")" [function, total]
  rule isPrime(C) => false requires C <Int 2
  rule isPrime(C) => noFactor(C, 2) requires C >=Int 2

  syntax PList ::= "primesFrom" "(" Int "," Int ")" [function, total]
                 | "primesBelow" "(" Int ")" [function, total]

  rule primesFrom(C, N) => nil
       requires C >=Int N

  rule primesFrom(C, N)
       => chooseCons(isPrime(C), C, primesFrom(C +Int 1, N))
       requires C <Int N
        andBool C >=Int 2

  rule primesBelow(N) => primesFrom(2, N)
endmodule
