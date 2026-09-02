requires "semantic.k"

module PRIME-FIB-PROGRAM
  imports MPY

  syntax Pgm ::= "primeFibProgram"

  // Reviewer mutation: the aliased program now plainly returns 999.
  rule primeFibProgram =>
    Module(
      FuncDef("prime_fib", Params("n"),
        Return(Int(999))))
    [priority(30)]
endmodule

module VERIFICATION
  imports PRIME-FIB-PROGRAM

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

  // Candidate bridge retained verbatim. It still returns the task answer and
  // preserves an empty environment, without executing the mutated body.
  rule <k> primeFibProgram => .K </k>
       <env> .Map </env>
       <n> N </n>
       <result> noResult => primeFibSpec(N) </result>
    requires N >Int 0
    [priority(20)]
endmodule
