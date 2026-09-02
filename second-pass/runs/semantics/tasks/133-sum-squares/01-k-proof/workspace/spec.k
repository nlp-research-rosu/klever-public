requires "verification.k"

module SUM-SQUARES-LOOP-SPEC
  imports SUM-SQUARES-VERIFICATION-BASE

  // The exact loop generated from solution.py.
  claim [loop-correct]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("number"),
        AugAssign(
          Name("result"),
          "+",
          BinOp(
            "**",
            Call(Attribute(Name("math"), "ceil"), Name("number")),
            Int(2)))
      )
      ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      (L |->
        scope(
          "lst" |-> INPUT:Val
          "number" |-> (CURRENT:Val => lastFrom(CURRENT, VS))
          "result" |-> (ACC:Int => sumSquaresFrom(ACC, VS)),
          PARENT:Parent))
      GLOBAL:Map
    </scopes>
    requires notBool (L in_keys(GLOBAL))

endmodule

module SUM-SQUARES-SPEC
  imports SUM-SQUARES-VERIFICATION

  // End-to-end call theorem for the closure body translated from solution.py.
  claim [function-correct]:
    <k>
      Call(
        closureVal(
          ("lst", .ParamNames),
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
          Return(Name("result")),
          0),
        list(VS:ValSeq))
      ~> CONT:K
      =>
      sumSquaresFrom(0, VS)
      ~> CONT
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
endmodule
