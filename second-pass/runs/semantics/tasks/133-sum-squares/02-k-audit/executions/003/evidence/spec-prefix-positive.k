requires "verification.k"

module SUM-SQUARES-PREFIX-POSITIVE-SPEC
  imports SUM-SQUARES-VERIFICATION

  // Reachable baseline for the non-vacuity mutation below.
  claim [empty-result-zero]:
    <k>
      Assign(Name("result"), Int(0))
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
