requires "verification.k"

module AUDIT-BRIDGE-CONTEXT
  imports VERIFICATION-BASE

  // The fixed supplied rule must preserve an immediate observable continuation.
  claim [fixed-yield-with-continuation]:
    <k>
      #iterYield(1, list(.ValSeq))
      ~> #loopStep(Name("n"), .Stmts)
      ~> Assign(Name("marker"), Int(7))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      ... 0 |-> scope(
            .Map
            => ("n" |-> 1
                "marker" |-> 7),
            parent(-1))
      ...
    </scopes>

  // This opposite interpretation is false: yielding 1 cannot bind n to 2.
  claim [wrong-yield-value]:
    <k>
      #iterYield(1, list(.ValSeq))
      ~> #loopStep(Name("n"), .Stmts)
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      ... 0 |-> scope(.Map => ("n" |-> 2), parent(-1)) ...
    </scopes>
endmodule
