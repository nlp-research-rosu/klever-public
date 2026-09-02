requires "/tmp/audit-work/9-rolling-max/build/solution-ast.k"

module BRIDGE-CONTINUATION-OPERATIONAL
  imports SOLUTION-AST

  // Fixed operational semantics for the same state and continuation.
  claim <py>
          <k> For(Name("number"), Name("numbers"), ROLLING-LOOP)
                ~> Name("first")
            => BoolVal(false) </k>
          <functions> .Map </functions>
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
          <stack> .List </stack>
        </py>
endmodule
