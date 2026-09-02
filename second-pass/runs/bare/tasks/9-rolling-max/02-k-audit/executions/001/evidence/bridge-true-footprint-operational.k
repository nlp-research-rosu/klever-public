requires "/tmp/audit-work/9-rolling-max/build/solution-ast.k"

module BRIDGE-TRUE-FOOTPRINT-OPERATIONAL
  imports SOLUTION-AST

  // Fixed execution at the actual submitted continuation retains all locals.
  claim <py>
          <k> For(Name("number"), Name("numbers"), ROLLING-LOOP)
                ~> Return(Name("result")) .Stmts ~> EndCall ~> Cleanup
            => Return(Name("result")) .Stmts ~> EndCall ~> Cleanup </k>
          <functions>
            "rolling_max" |->
              Function(Params("numbers", .Strings), ROLLING-BODY)
          </functions>
          <env>
            "first"   |-> BoolVal(true)
            "maximum" |-> IntVal(0)
            "numbers" |-> ListVal(ListItem(2) ListItem(1))
            "result"  |-> ListVal(.List)
            =>
            "first"   |-> BoolVal(false)
            "maximum" |-> IntVal(2)
            "number"  |-> IntVal(1)
            "numbers" |-> ListVal(ListItem(2) ListItem(1))
            "result"  |-> ListVal(ListItem(2) ListItem(2))
          </env>
          <stack> ListItem(Frame(.Map)) </stack>
        </py>
endmodule
