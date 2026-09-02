requires "/audit-output/evidence/bind-connection.k"

module BIND-CONNECTION-SPEC
  imports BIND-CONNECTION

  // Universal fixed-semantics derivation of verification.k:44-47 over its
  // complete match domain.  No rule from verification.k is imported.
  claim [singleton-plain-bind]:
    <k>
      #bindP(("l"), (V:Val, .Vals))
      ~> K
    =>
      K
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(.Map => ("l" |-> V), P:Parent)
      ...
    </scopes>
endmodule
