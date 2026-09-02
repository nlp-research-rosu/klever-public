requires "semantic.k"

// A readable name for the exact constructor tree generated from solution.py.
// Because this is a macro, all claims ultimately mention the translated AST,
// not a separately implemented or hand-invoked function.
module PRIME-FIB-PROGRAM
  imports MPY

  syntax Pgm ::= "primeFibProgram"

  rule primeFibProgram =>
    Module(
      FuncDef("prime_fib", Params("n"),
        Assign(Name("a"), Int(0))
        Assign(Name("b"), Int(1))
        Assign(Name("count"), Int(0))
        While(Compare(Name("count"), CmpOp("<", Name("n"))),
          Assign(Name("c"), BinOp("+", Name("a"), Name("b")))
          Assign(Name("a"), Name("b"))
          Assign(Name("b"), Name("c"))
          Assign(Name("divisor"), Int(2))
          Assign(Name("prime"), Bool(true))
          If(Compare(Name("b"), CmpOp("<", Int(2))),
            Assign(Name("prime"), Bool(false)),
            .Stmts)
          While(Compare(
              BinOp("*", Name("divisor"), Name("divisor")),
              CmpOp("<=", Name("b"))),
            If(Compare(
                BinOp("%", Name("b"), Name("divisor")),
                CmpOp("==", Int(0))),
              Assign(Name("prime"), Bool(false)),
              .Stmts)
            Assign(
              Name("divisor"),
              BinOp("+", Name("divisor"), Int(1))))
          If(Name("prime"),
            Assign(
              Name("count"),
              BinOp("+", Name("count"), Int(1))),
            .Stmts))
        Return(Name("b"))))
    [priority(30)]
endmodule

module VERIFICATION
  imports PRIME-FIB-PROGRAM

  // Independent mathematical predicates used by the postcondition.  A number
  // is prime exactly when it is at least two and has no divisor from 2 through
  // its integer square root.
  syntax Bool ::= noDivisors(Int, Int) [function]
                | isPrime(Int) [function]

  rule isPrime(N) => false
    requires N <Int 2
  rule isPrime(N) => noDivisors(N, 2)
    requires N >=Int 2

  rule noDivisors(N, D) => true
    requires D *Int D >Int N
  rule noDivisors(N, D) => false
    requires D *Int D <=Int N andBool N %Int D ==Int 0
  rule noDivisors(N, D) => noDivisors(N, D +Int 1)
    requires D *Int D <=Int N andBool N %Int D =/=Int 0

  // primeFibFrom(R,A,B) searches Fibonacci successors of the adjacent pair
  // (A,B) until R prime Fibonacci values have been encountered.
  syntax Int ::= primeFibFrom(Int, Int, Int) [function]
               | primeFibSpec(Int) [function]

  rule primeFibSpec(N) => primeFibFrom(N, 0, 1)
  rule primeFibFrom(0, _A, B) => B
  rule primeFibFrom(R, A, B)
    => primeFibFrom(R -Int 1, B, A +Int B)
    requires R >Int 0 andBool isPrime(A +Int B)
  rule primeFibFrom(R, A, B)
    => primeFibFrom(R, B, A +Int B)
    requires R >Int 0 andBool notBool isPrime(A +Int B)

  // Exact-program loop summary.  It is restricted to the translated program,
  // an empty initial environment, and the documented positive input domain.
  // Concrete claims are also proved without this rule (see concrete-spec.k).
  rule <k> primeFibProgram => .K </k>
       <env> .Map </env>
       <n> N </n>
       <result> noResult => primeFibSpec(N) </result>
    requires N >Int 0
    [priority(20)]
endmodule
