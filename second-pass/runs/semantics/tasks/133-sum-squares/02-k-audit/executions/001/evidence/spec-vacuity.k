requires "verification.k"

module SUM-SQUARES-SPEC-VACUITY
  imports SUM-SQUARES-VERIFICATION

  // Fresh reviewer-authored false mutation: the returned sum is one too large.
  // For the satisfying empty-list instance, the real result is 0 but this asks for 1.
  claim [function-off-by-one]:
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
      (sumSquaresFrom(0, VS) +Int 1)
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
