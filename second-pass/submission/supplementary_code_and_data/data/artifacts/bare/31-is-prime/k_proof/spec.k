requires "verification.k"

module SPEC
  imports VERIFICATION

  // Tail-recursive invariant: for any search position D >= 2, executing the
  // helper computes exactly the finite divisor search in verification.k.
  claim
    <k> #invoke("no_divisor", (Int(N), Int(D))) => .K </k>
    <functions>
      "no_divisor" |-> noDivisorFunction() _REST
    </functions>
    <env> _RHO => ?_FINALENV </env>
    <result> _R => Bool(noDivisor(N, D)) </result>
    requires N >=Int 2 andBool D >=Int 2
    [label(helper-correct)]

  // Universal target theorem for the required entry point.
  claim
    <k> solutionProgram() ~> #invoke("is_prime", Int(N)) => .K </k>
    <functions>
      .Map
      => "no_divisor" |-> noDivisorFunction()
         "is_prime" |-> isPrimeFunction()
    </functions>
    <env> .Map => ?_FINALENV </env>
    <result> Bool(false) => Bool(prime(N)) </result>
    [label(is-prime-correct)]
endmodule
