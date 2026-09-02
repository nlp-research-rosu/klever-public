requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // A mathematical reference predicate.  noDivisor(N,D) searches the finite
  // interval D .. floor(sqrt(N)); hence prime(N) says N >= 2 and has no
  // divisor in 2 .. floor(sqrt(N)), the standard characterization of primes.
  syntax Bool ::= noDivisor(Int, Int) [function]
                | prime(Int) [function]

  rule noDivisor(N, D) => true
    requires D *Int D >Int N
  rule noDivisor(N, D) => false
    requires D *Int D <=Int N andBool D dividesInt N
  rule noDivisor(N, D) => noDivisor(N, D +Int 1)
    requires D *Int D <=Int N andBool notBool (D dividesInt N)

  rule prime(N) => false
    requires N <Int 2
  rule prime(N) => noDivisor(N, 2)
    requires N >=Int 2

  // Canonical terms for the two definitions translated from solution.py.
  // Naming them keeps the claims readable; these are equations, not shortcuts
  // in the execution semantics.
  syntax Function ::= noDivisorFunction() [function]
                    | isPrimeFunction() [function]
  syntax Program ::= solutionProgram() [function]

  rule noDivisorFunction() =>
    function(
      Params("n", "d"),
      If(
        Compare(BinOp("*", Name("d"), Name("d")), CmpOp(">", Name("n"))),
        Return(Bool(true)),
        .Stmts)
      If(
        Compare(BinOp("%", Name("n"), Name("d")), CmpOp("==", Int(0))),
        Return(Bool(false)),
        .Stmts)
      Return(Call(Name("no_divisor"), Name("n"), BinOp("+", Name("d"), Int(1))))
    )

  rule isPrimeFunction() =>
    function(
      Params("n"),
      If(
        Compare(Name("n"), CmpOp("<", Int(2))),
        Return(Bool(false)),
        .Stmts)
      Return(Call(Name("no_divisor"), Name("n"), Int(2)))
    )

  rule solutionProgram() =>
    Module(
      FuncDef("no_divisor", Params("n", "d"),
        If(
          Compare(BinOp("*", Name("d"), Name("d")), CmpOp(">", Name("n"))),
          Return(Bool(true)),
          .Stmts)
        If(
          Compare(BinOp("%", Name("n"), Name("d")), CmpOp("==", Int(0))),
          Return(Bool(false)),
          .Stmts)
        Return(Call(Name("no_divisor"), Name("n"), BinOp("+", Name("d"), Int(1)))))
      FuncDef("is_prime", Params("n"),
        If(
          Compare(Name("n"), CmpOp("<", Int(2))),
          Return(Bool(false)),
          .Stmts)
        Return(Call(Name("no_divisor"), Name("n"), Int(2))))
    )
endmodule
