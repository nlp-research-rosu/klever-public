requires "verification.k"

module SPEC-VACUITY-GROUND
  imports VERIFICATION

  // The source precondition is satisfied by A = seq(), O = 0, N = 0.
  // Real execution returns -1; this deliberate mutation requires 0.
  claim [empty-array-false-result]:
    <k> invoke("can_arrange", arrayVal(seq(.Ints), 0, 0))
      => value(intVal(0)) </k>
    <env> .Map </env>
    <defs> "can_arrange" |-> canArrangeFunction </defs>
    <stack> .List </stack>

endmodule
