requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated implementation: it keeps values occurring twice,
  // while the destination still states the original keep-singletons result.
  claim [count-two-does-not-refine-count-one]:
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
        "result"  |-> ref(H:Int)
        "number"  |-> (N:Val => ?N:Val),
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
