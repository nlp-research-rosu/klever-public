requires "verification.k"

module SPEC-BODY-SENSITIVITY-AUDIT
  imports VERIFICATION

  // Change the executed loop guard from count == 1 to count == 2 while
  // retaining the original count-one destination.
  claim [count-two-body-is-not-count-one]:
    <k>
      #loop(
        list(REST:ValSeq),
        Name("number"),
        If(
          Compare(
            Call(
              Attribute(Name("numbers"), "count"),
              (Name("number"), .Exprs)),
            CmpOp("==", Int(2))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              (Name("number"), .Exprs))),
          .Stmts))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "numbers" |-> list(ALL:ValSeq)
        "result" |-> ref(H:Int)
        "number" |-> (N:Val => ?N:Val),
        parent(0))
      ...
    </scopes>
    <heap>
      ...
      H |-> list(ACC:ValSeq => rdAcc(ACC, REST, ALL))
      ...
    </heap>
    requires allInts(REST) andBool allInts(ALL)
endmodule
