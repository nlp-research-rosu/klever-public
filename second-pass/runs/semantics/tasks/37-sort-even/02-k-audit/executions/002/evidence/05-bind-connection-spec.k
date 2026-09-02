requires "bind-fixed.k"

module BIND-CONNECTION-SPEC
  imports BIND-FIXED

  // Universal fixed-semantics behavior for the exact current frame. The
  // surrounding scope-map frame is tested separately by the ground context
  // witness because the Haskell backend cannot prove the generic AC-map frame.
  claim [singleton-bind]:
    <k> #bindP(("l"), (V:Val, .Vals)) => .K ... </k>
    <env> L:Int </env>
    <scopes> L |-> scope(.Map => ("l" |-> V), P:Parent) </scopes>
endmodule
