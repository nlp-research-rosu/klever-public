requires "verification.k"

module CONTEXT-BRIDGED
  imports VERIFICATION

  syntax Program ::= "BridgeContext"

  // Identical start and continuation to CONTEXT-OPERATIONAL. The only
  // difference is importing the candidate's priority-40 loop bridge.
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
