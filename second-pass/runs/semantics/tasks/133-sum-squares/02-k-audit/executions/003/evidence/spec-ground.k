requires "verification.k"

module SUM-SQUARES-GROUND-SPEC
  imports SUM-SQUARES-VERIFICATION

  claim [ground-empty]:
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
        list(.ValSeq))
      ~> CONT:K
      =>
      0 ~> CONT
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>

  claim [ground-ints]:
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
        list(vCons(1, vCons(2, vCons(3, .ValSeq)))))
      ~> CONT:K
      =>
      14 ~> CONT
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <stack> .List </stack>
    <ret> noRet </ret>

  claim [ground-floats]:
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
        list(vCons(1.4, vCons(4.2, vCons(0, .ValSeq)))))
      ~> CONT:K
      =>
      29 ~> CONT
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
