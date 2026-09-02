requires "verification.k"

module GROUND-WITNESSES
  imports VERIFICATION

  // A concrete state satisfying the universal entry claim (which has no
  // requires-clause) and yielding the asserted prime(31) result.
  claim [entry-31]:
    <k> solutionProgram() ~> #invoke("is_prime", Int(31)) => .K </k>
    <functions>
      .Map
      => "no_divisor" |-> noDivisorFunction()
         "is_prime" |-> isPrimeFunction()
    </functions>
    <env> .Map => ?_FINALENV </env>
    <result> Bool(false) => Bool(true) </result>

  // A second entry witness takes the divisor-found branch.
  claim [entry-4]:
    <k> solutionProgram() ~> #invoke("is_prime", Int(4)) => .K </k>
    <functions>
      .Map
      => "no_divisor" |-> noDivisorFunction()
         "is_prime" |-> isPrimeFunction()
    </functions>
    <env> .Map => ?_FINALENV </env>
    <result> Bool(false) => Bool(false) </result>

  // N=31,D=2 satisfies N>=2 and D>=2 in the helper claim.
  claim [helper-31-2]:
    <k> #invoke("no_divisor", (Int(31), Int(2))) => .K </k>
    <functions>
      "no_divisor" |-> noDivisorFunction() _REST
    </functions>
    <env> .Map => ?_FINALENV </env>
    <result> Bool(false) => Bool(true) </result>
endmodule
