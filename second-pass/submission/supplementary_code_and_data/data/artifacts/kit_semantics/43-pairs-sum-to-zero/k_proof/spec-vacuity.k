requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: on the realizable empty-list input, the loop leaves
  // found false. Claiming true must be rejected.
  claim [false-result]:
    <k>
      #loop(
        list(.ValSeq),
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
            CmpOp(">", Int(0))),
            Assign(Name("found"), Bool(true)),
            .Stmts))
      ) => .K
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "found" |-> (false => true)
        "l"     |-> list(.ValSeq)
        "x"     |-> 0,
        parent(0))
      ...
    </scopes>
endmodule
