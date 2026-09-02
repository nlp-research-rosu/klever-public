requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false result mutation. The entry precondition is universal,
  // so N=31 is satisfying. The correct concrete result is Bool(true); this
  // mutation requires the completed configuration to retain Bool(false).
  claim [false-entry-31]:
    <k> solutionProgram() ~> #invoke("is_prime", Int(31)) => .K </k>
    <functions>
      .Map
      => "no_divisor" |-> noDivisorFunction()
         "is_prime" |-> isPrimeFunction()
    </functions>
    <env> .Map => ?_FINALENV </env>
    <result> Bool(false) </result>
endmodule
