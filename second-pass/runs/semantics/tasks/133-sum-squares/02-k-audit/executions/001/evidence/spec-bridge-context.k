requires "verification.k"

module SUM-SQUARES-BRIDGE-CONTEXT-BASE
  imports SUM-SQUARES-VERIFICATION-BASE

  claim [observable-continuation-base]:
    <k>
      #loop(
        list(vCons(1, vCons(2, .ValSeq))),
        Name("number"),
        AugAssign(
          Name("result"),
          "+",
          BinOp(
            "**",
            Call(Attribute(Name("math"), "ceil"), Name("number")),
            Int(2)))
      )
      ~> Assign(Name("after"), Int(7))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          "lst" |-> list(vCons(1, vCons(2, .ValSeq)))
          "number" |-> (0 => 2)
          "result" |-> (0 => 5)
          "after" |-> (0 => 7),
          parent(0)))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
endmodule

module SUM-SQUARES-BRIDGE-CONTEXT-EXTENDED
  imports SUM-SQUARES-VERIFICATION

  claim [observable-continuation-extended]:
    <k>
      #loop(
        list(vCons(1, vCons(2, .ValSeq))),
        Name("number"),
        AugAssign(
          Name("result"),
          "+",
          BinOp(
            "**",
            Call(Attribute(Name("math"), "ceil"), Name("number")),
            Int(2)))
      )
      ~> Assign(Name("after"), Int(7))
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          "lst" |-> list(vCons(1, vCons(2, .ValSeq)))
          "number" |-> (0 => 2)
          "result" |-> (0 => 5)
          "after" |-> (0 => 7),
          parent(0)))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
endmodule
