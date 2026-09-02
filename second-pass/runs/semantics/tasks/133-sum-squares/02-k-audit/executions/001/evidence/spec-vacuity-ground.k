requires "verification.k"

module SUM-SQUARES-SPEC-VACUITY-GROUND
  imports SUM-SQUARES-VERIFICATION

  // Fresh reviewer-authored false mutation at a satisfying ground entry state:
  // the empty-list execution returns 0, while this postcondition demands 1.
  claim [empty-list-off-by-one]:
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
      1
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
