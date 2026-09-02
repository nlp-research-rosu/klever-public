requires "verification.k"

module GROUND-SPEC
  imports VERIFICATION

  claim
    <k> invoke("can_arrange", arrayVal(seq(1,2,4,3,5), 0, 5))
      => value(intVal(3)) </k>
    <env> .Map </env>
    <defs> "can_arrange" |-> canArrangeFunction </defs>
    <stack> .List </stack>

  claim
    <k> invoke("can_arrange", arrayVal(seq(.Ints), 0, 0))
      => value(intVal(-1)) </k>
    <env> .Map </env>
    <defs> "can_arrange" |-> canArrangeFunction </defs>
    <stack> .List </stack>

  claim
    <k> invoke("can_arrange", arrayVal(seq(5,4,3,2,1), 0, 5))
      => value(intVal(4)) </k>
    <env> .Map </env>
    <defs> "can_arrange" |-> canArrangeFunction </defs>
    <stack> .List </stack>

endmodule
