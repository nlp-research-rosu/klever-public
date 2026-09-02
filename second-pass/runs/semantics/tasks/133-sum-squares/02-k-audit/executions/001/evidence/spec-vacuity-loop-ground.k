requires "verification.k"

module SUM-SQUARES-LOOP-SPEC-VACUITY-GROUND
  imports SUM-SQUARES-VERIFICATION-BASE

  // False ground mutation of the result-bearing loop obligation.
  // An empty loop leaves result at 0; the target state demands 1.
  claim [empty-loop-off-by-one]:
    <k>
      #loop(
        list(.ValSeq),
        Name("number"),
        AugAssign(
          Name("result"),
          "+",
          BinOp(
            "**",
            Call(Attribute(Name("math"), "ceil"), Name("number")),
            Int(2)))
      )
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |->
        scope(
          "lst" |-> list(.ValSeq)
          "number" |-> 0
          "result" |-> (0 => 1),
          parent(0)))
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
endmodule
