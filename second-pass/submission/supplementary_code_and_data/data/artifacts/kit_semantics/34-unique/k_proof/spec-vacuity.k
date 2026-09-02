requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: unique([2, 1, 2]) is [1, 2], not [2, 1].
  claim [false-result]:
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
        2 |-> list(vCons(2, vCons(1, .ValSeq)))
      )
    </heap>
    <heapLoc> 1 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
