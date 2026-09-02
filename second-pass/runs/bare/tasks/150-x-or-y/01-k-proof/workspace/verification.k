requires "semantic.k"

module MPY-VERIFICATION
  imports MPY

  // primeFrom(N, D) means that N has no divisor in the inclusive range
  // from D through floor(sqrt(N)).  Its recursive shape mirrors the loop.
  syntax Bool ::= primeFrom(Int, Int) [function]
  rule primeFrom(N, D) => true
    requires N <Int D *Int D
  rule primeFrom(N, D) => false
    requires D *Int D <=Int N andBool N %Int D ==Int 0
  rule primeFrom(N, D) => primeFrom(N, D +Int 1)
    requires D *Int D <=Int N andBool N %Int D =/=Int 0

  syntax Bool ::= isPrime(Int) [function]
  rule isPrime(N) => false
    requires N <Int 2
  rule isPrime(N) => primeFrom(N, 2)
    requires 2 <=Int N

  syntax Val ::= chooseVal(Bool, Int, Int) [function]
  rule chooseVal(true, X, _Y) => intVal(X)
  rule chooseVal(false, _X, Y) => intVal(Y)
endmodule
