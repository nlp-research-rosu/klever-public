requires "verification.k"

module SUM-SQUARES-BODY-MUTATION-SPEC
  imports SUM-SQUARES-VERIFICATION

  // Executed body mutation: initial accumulator 0 -> 1. The complete mutated
  // body prefix is executed on an empty list and must leave result = 1, not 0.
  claim [body-sensitive]:
    <k>
      Assign(Name("result"), Int(1))
      For(
        Name("number"),
        Name("lst"),
        AugAssign(
          Name("result"),
          "+",
          BinOp(
            "**",
            Call(Attribute(Name("math"), "ceil"), Name("number")),
            Int(2))))
      Return(Name("result"))
      ~> CONT:K
      =>
      Return(0)
      ~> .Stmts
      ~> CONT
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          "lst" |-> list(.ValSeq)
          "result" |-> (99 => 0),
          parent(0)))
      GLOBAL:Map
    </scopes>
    requires notBool (1 in_keys(GLOBAL))
endmodule
