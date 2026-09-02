requires "verification.k"

module AUDIT-MEMBER-WITNESS
  imports VERIFICATION-BASE

  // Satisfying ground instance of MEMBER-SPEC's precondition.
  claim [member-ground]:
    <k>
      #memberAcc(2, list(vCons(1, vCons(2, .ValSeq))))
      => true
    </k>
endmodule

module AUDIT-LOOP-WITNESS
  imports VERIFICATION-MEMBER

  // Satisfying ground instance of LOOP-SPEC's precondition, proved without
  // the loop bridge.
  claim [loop-ground]:
    <k>
      #loop(
        list(vCons(2, vCons(1, vCons(2, .ValSeq)))),
        Name("x"),
        If(
          Compare(Name("x"), CmpOp("not in", Name("result"))),
          Expr(Call(Attribute(Name("result"), "append"), Name("x"))),
          .Stmts))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("l" |-> ref(0))
        ("result" |-> ref(1))
        ("x" |-> (noneV => 2)),
        parent(0))
    </scopes>
    <heap>
      1 |-> list(
        .ValSeq
        => vCons(2, vCons(1, .ValSeq)))
    </heap>
endmodule

module AUDIT-ENTRY-WITNESS
  imports VERIFICATION

  // Ground instance of SPEC for INPUT=[2,1,2], with the supplied concrete
  // sort semantics reducing the claimed result to [1,2].
  claim [entry-ground]:
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
      ( 0 |-> list(vCons(2, vCons(1, vCons(2, .ValSeq))))
      =>
        0 |-> list(vCons(2, vCons(1, vCons(2, .ValSeq))))
        1 |-> list(vCons(2, vCons(1, .ValSeq)))
        2 |-> list(vCons(1, vCons(2, .ValSeq)))
      )
    </heap>
    <heapLoc> 1 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

