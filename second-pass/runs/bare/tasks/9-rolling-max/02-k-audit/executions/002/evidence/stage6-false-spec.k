requires "verification.k"

module REVIEW-FALSE-SPEC
  imports VERIFICATION

  // Satisfiable input: both Python implementations and fixed K execution
  // return [2, 2]. This fresh mutation falsely demands [2, 1].
  claim <py>
          <k> VerifyRunList(
                 SOLUTION,
                 ListItem(2) ListItem(1))
            => ListVal(ListItem(2) ListItem(1)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
