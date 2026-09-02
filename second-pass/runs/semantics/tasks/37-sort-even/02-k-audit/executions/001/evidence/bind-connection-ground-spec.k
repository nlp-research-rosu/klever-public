requires "/audit-output/evidence/bind-connection.k"

module BIND-CONNECTION-GROUND-SPEC
  imports BIND-CONNECTION

  // Satisfiable boundary witness for the bridge, using only fixed semantics.
  claim [singleton-plain-bind-ground]:
    <k>
      #bindP(("l"), (7, .Vals))
      ~> Int(9)
    =>
      9
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(.Map => ("l" |-> 7), parent(0)))
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
endmodule
