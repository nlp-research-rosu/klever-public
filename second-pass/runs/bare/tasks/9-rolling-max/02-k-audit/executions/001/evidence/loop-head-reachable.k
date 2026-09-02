requires "/tmp/audit-work/9-rolling-max/build/solution-ast.k"

module LOOP-HEAD-REACHABLE
  imports SOLUTION-AST

  // The concrete state used by the bridge counterexample is reached by the
  // submitted program on intended input [2,1], before any loop step executes.
  claim <py>
          <k> OpRunList(SOLUTION, ListItem(2) ListItem(1))
            =>
               For(Name("number"), Name("numbers"), ROLLING-LOOP)
                 ~> Return(Name("result")) .Stmts
                 ~> EndCall ~> Cleanup </k>
          <functions>
            .Map
            =>
            "rolling_max" |->
              Function(Params("numbers", .Strings), ROLLING-BODY)
          </functions>
          <env>
            .Map
            =>
            "first"   |-> BoolVal(true)
            "maximum" |-> IntVal(0)
            "numbers" |-> ListVal(ListItem(2) ListItem(1))
            "result"  |-> ListVal(.List)
          </env>
          <stack>
            .List => ListItem(Frame(.Map))
          </stack>
        </py>
endmodule
