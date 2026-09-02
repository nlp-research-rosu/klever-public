requires "verification.k"

module SUM-SQUARES-VACUITY-AUDIT-SPEC
  imports SUM-SQUARES-VERIFICATION

  // False result mutation over the exact original body prefix. The empty
  // satisfying input leaves result = 0; the mutated obligation demands 1.
  claim [off-by-one]:
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
      Return(1)
      ~> .Stmts
      ~> CONT
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          "lst" |-> list(.ValSeq)
          "result" |-> (99 => 1),
          parent(0)))
      GLOBAL:Map
    </scopes>
    requires notBool (1 in_keys(GLOBAL))
endmodule
