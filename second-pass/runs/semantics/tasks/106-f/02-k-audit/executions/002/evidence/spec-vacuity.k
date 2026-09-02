requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false-postcondition mutation: the real f(5) ends in 15, not 16.
  claim
    <k> Call(Name("f"), Int(5)) => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "f" |-> closureVal("n", .ParamNames,
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("factorial"), Int(1))
          Assign(Name("total"), Int(0))
          Assign(Name("i"), Int(1))
          While(Compare(Name("i"), CmpOp("<=", Name("n"))),
            AugAssign(Name("factorial"), "*", Name("i"))
            AugAssign(Name("total"), "+", Name("i"))
            If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Expr(Call(Attribute(Name("result"), "append"), Name("factorial"))),
              Expr(Call(Attribute(Name("result"), "append"), Name("total"))))
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("result")), 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
        vCons(1, vCons(2, vCons(6, vCons(24, vCons(16, .ValSeq))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires true
    [label(false-f-five)]
endmodule
