requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // Reviewer mutation: every loop iteration appends, instead of conditionally
  // appending only absent values. The exact loop bridge must not match this
  // changed program term, and the original unique-result obligation must fail.
  claim [always-append-is-not-unique]:
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
              Expr(Call(
                Attribute(Name("result"), "append"),
                Name("x"))))
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

