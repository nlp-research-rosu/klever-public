requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Fresh false result obligation. The precondition is satisfiable at N=2,
  // and the real submitted body returns true under the candidate semantics.
  claim
    <k> solutionProgram() ~> #invoke("is_prime", Int(2)) => .K </k>
    <functions>
      .Map
      => "no_divisor" |-> noDivisorFunction()
         "is_prime" |-> isPrimeFunction()
    </functions>
    <env> .Map => ?_FINALENV </env>
    <result> Bool(false) => Bool(false) </result>
    [label(audit-false-result)]
endmodule
