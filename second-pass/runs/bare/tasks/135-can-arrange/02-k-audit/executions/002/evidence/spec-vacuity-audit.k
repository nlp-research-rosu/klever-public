requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false ground mutation of the documented example:
  // the real and formally claimed answer is 3, not 4.
  claim
    <k> invoke("can_arrange", arrayVal(seq(1,2,4,3,5), 0, 5))
      => value(intVal(4)) </k>
    <env> .Map </env>
    <defs> "can_arrange" |-> canArrangeFunction </defs>
    <stack> .List </stack>

endmodule
