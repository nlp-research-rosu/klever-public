requires "verification.k"

module MEMBER-SPEC
  imports VERIFICATION-BASE

  // Fixed-semantics execution theorem for list membership.  This is a
  // circularity over the input sequence, not a rule that replaces execution.
  claim [member-summary]:
    <k> #memberAcc(V:Val, list(VS:ValSeq))
      => memberVS(V, VS) ... </k>
endmodule

module LOOP-SPEC
  imports VERIFICATION-MEMBER

  // The exact source for-loop with an arbitrary continuation.  The arbitrary
  // VS and ACC make this an unbounded loop circularity.
  claim [unique-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("x"),
        If(
          Compare(Name("x"), CmpOp("not in", Name("result"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("x"))),
          .Stmts))
      => .K ...
    </k>
    <env> 1 </env>
    <scopes>
      ... 1 |-> scope(
        ("l" |-> ref(0))
        ("result" |-> ref(1))
        ("x" |-> (X:Val => lastFromVS(VS, X))),
        parent(0))
      ...
    </scopes>
    <heap>
      ... 1 |-> list(ACC:ValSeq => dedupFromVS(VS, ACC)) ...
    </heap>
endmodule

module SPEC
  imports VERIFICATION

  // Required target theorem: invoke the exact generated function closure on
  // an arbitrary finite ValSeq stored as a Python list object.
  claim [unique-full-domain]:
    <k> Call(Name("unique"), ref(0)) => ref(2) </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        .Map [
          "unique" <- closureVal(
            ("l", .ParamNames),
            Expr(Str("Return sorted unique elements in a list."))
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("x"), NoneVal)
            For(
              Name("x"),
              Name("l"),
              If(
                Compare(Name("x"), CmpOp("not in", Name("result"))),
                Expr(Call(
                  Attribute(Name("result"), "append"),
                  Name("x"))),
                .Stmts))
            Return(Call(Name("sorted"), Name("result")))
            .Stmts,
            0) ],
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      ( 0 |-> list(INPUT:ValSeq)
      =>
        0 |-> list(INPUT)
        1 |-> list(dedupFromVS(INPUT, .ValSeq))
        2 |-> list(sortVS(dedupFromVS(INPUT, .ValSeq)))
      )
    </heap>
    <heapLoc> 1 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
