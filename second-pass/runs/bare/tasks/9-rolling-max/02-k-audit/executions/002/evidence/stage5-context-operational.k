requires "solution-ast.k"

module CONTEXT-OPERATIONAL
  imports SOLUTION-AST

  syntax Program ::= "BridgeContext"

  // Start at the exact loop-entry environment accepted by the candidate's
  // bridge, then observe a local that genuine loop execution preserves.
  rule <k> BridgeContext
        => For(Name("number"), Name("numbers"), ROLLING-LOOP)
           ~> Name("maximum") ... </k>
       <env> .Map
         =>
         "first" |-> BoolVal(true)
         "maximum" |-> IntVal(0)
         "numbers" |-> ListVal(ListItem(2) ListItem(1))
         "result" |-> ListVal(.List)
       </env>
endmodule
