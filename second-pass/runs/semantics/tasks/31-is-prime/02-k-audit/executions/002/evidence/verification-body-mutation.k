requires "reference-semantics/semantics.k"

module VERIFICATION-BASE
  imports MPY

  // The call semantics removes a fresh frame with a symbolic map update.
  // MAP does not simplify these identities under path constraints on its own,
  // so expose the elementary finite-map facts to the symbolic backend.
  rule M:Map [ L:Int <- undef ] => M
    requires notBool (L in_keys(M))
  rule ((M:Map L:Int |-> _V:Scope) [ L <- undef ]) => M
    requires notBool (L in_keys(M))

  // Closed syntax terms taken verbatim from solution.mpy.  These equations
  // only abbreviate syntax; they do not summarize execution.
  syntax Expr ::= "#primeCond" [macro]
  rule #primeCond
    => Compare(
         BinOp("*", Name("divisor"), Name("divisor")),
         CmpOp("<=", Name("n")))

  syntax Stmts ::= "#primeLoopBody" [macro]
  rule #primeLoopBody
    => If(Compare(
         BinOp("%", Name("n"), Name("divisor")),
         CmpOp("==", Int(0))),
         Return(Bool(false)),
         .Stmts)
       AugAssign(Name("divisor"), "+", Int(1))

  syntax Stmts ::= "#entryBody" [macro]
  rule #entryBody
    => If(Compare(Name("n"), CmpOp("<", Int(2))),
         Return(Bool(false)),
         .Stmts)
       Assign(Name("divisor"), Int(2))
       While(#primeCond, #primeLoopBody)
       Return(Bool(false))

  // Executable mathematical specification.  For n >= 2, trialPrime(n,d)
  // says that no divisor at or above d and at or below sqrt(n) divides n.
  // Every composite n >= 2 has a factor no greater than sqrt(n), so the entry
  // predicate below is exactly mathematical primality.
  syntax Bool ::= trialPrime(Int, Int) [function]
  rule trialPrime(N:Int, D:Int) => true
    requires D *Int D >Int N
  rule trialPrime(N:Int, D:Int) => false
    requires D *Int D <=Int N andBool N %Int D ==Int 0
  rule trialPrime(N:Int, D:Int) => trialPrime(N, D +Int 1)
    requires D *Int D <=Int N andBool N %Int D =/=Int 0

  syntax Bool ::= isPrimeSpec(Int) [function]
  rule isPrimeSpec(N:Int) => false requires N <Int 2
  rule isPrimeSpec(N:Int) => trialPrime(N, 2) requires N >=Int 2
endmodule

// Public proof module.  The specification composes a finite entry-prefix
// theorem with the general loop theorem, so no unproved execution-summary
// rule is added here.
module VERIFICATION
  imports VERIFICATION-BASE
endmodule
