requires "/tmp/audit-work/9-rolling-max/build/solution-ast.k"

module AUDIT-OPERATIONAL-CLAIMS
  imports SOLUTION-AST

  claim [label(audit-operational-empty)]:
        <py>
          <k> OpRunList(SOLUTION, .List)
            => ListVal(.List) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>

  claim [label(audit-operational-prompt)]:
        <py>
          <k> OpRunList(SOLUTION,
               ListItem(1) ListItem(2) ListItem(3) ListItem(2)
               ListItem(3) ListItem(4) ListItem(2))
            => ListVal(ListItem(1) ListItem(2) ListItem(3)
                       ListItem(3) ListItem(3) ListItem(4) ListItem(4)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>

  claim [label(audit-operational-negative)]:
        <py>
          <k> OpRunList(SOLUTION,
               ListItem(-5) ListItem(-9) ListItem(-3) ListItem(-4))
            => ListVal(ListItem(-5) ListItem(-5) ListItem(-3) ListItem(-3)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
