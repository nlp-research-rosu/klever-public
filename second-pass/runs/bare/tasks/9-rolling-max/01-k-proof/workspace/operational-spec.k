requires "solution-ast.k"

module OPERATIONAL-SPEC
  imports SOLUTION-AST

  // These claims use only semantic.k's small-step rules: no symbolic summary
  // from verification.k is present in this compiled definition.
  claim <py>
          <k> OpRunList(SOLUTION, .List)
            => ListVal(.List) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>

  claim <py>
          <k> OpRunList(SOLUTION,
               ListItem(1) ListItem(2) ListItem(3) ListItem(2)
               ListItem(3) ListItem(4) ListItem(2))
            => ListVal(ListItem(1) ListItem(2) ListItem(3)
                       ListItem(3) ListItem(3) ListItem(4) ListItem(4)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>

  claim <py>
          <k> OpRunList(SOLUTION,
               ListItem(-5) ListItem(-9) ListItem(-3) ListItem(-4))
            => ListVal(ListItem(-5) ListItem(-5) ListItem(-3) ListItem(-3)) ~> .K </k>
          <functions> .Map </functions>
          <env> .Map </env>
          <stack> .List </stack>
        </py>
endmodule
