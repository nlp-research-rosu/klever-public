requires "shape-connection.k"

module STAGE5-SHAPE-CONTEXT-SPEC
  imports SHAPE-CONNECTION

  claim [for-shape-preserves-observable-suffix]:
    <k> For(Name("v"), list(vCons(7, .ValSeq)), .Stmts) ~> Int(9)
        => 9 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map => "v" |-> 7, parent(-1))
      -1 |-> builtinsScope
    </scopes>
endmodule
