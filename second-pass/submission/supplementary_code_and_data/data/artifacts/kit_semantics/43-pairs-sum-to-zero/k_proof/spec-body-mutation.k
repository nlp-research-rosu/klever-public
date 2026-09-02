requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Material mutation: the nonzero branch incorrectly requires two inverse
  // occurrences.  For [1, -1] the correct result is true, so this must fail.
  claim [mutated-body]:
    <k>
      #loop(
        list(vCons(1, vCons(-1, .ValSeq))),
        Name("x"),
        If(Compare(Name("x"), CmpOp("==", Int(0))),
          If(Compare(
            Call(Attribute(Name("l"), "count"), Int(0)),
            CmpOp(">", Int(1))),
            Assign(Name("found"), Bool(true)),
            .Stmts),
          If(Compare(
            Call(Attribute(Name("l"), "count"),
                 UnaryOp("-", Name("x"))),
            CmpOp(">", Int(1))),
            Assign(Name("found"), Bool(true)),
            .Stmts))
      ) => .K
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "found" |-> (false => true)
        "l"     |-> list(vCons(1, vCons(-1, .ValSeq)))
        "x"     |-> (0 => -1),
        parent(0))
      ...
    </scopes>
endmodule
