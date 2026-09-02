requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body-sensitivity witness: the submitted `total += i` is changed to
  // `total += 2`. On n = 1 the mutant returns [2], so the real [1] target must
  // no longer close.
  claim
    <k> Call(Name("f"), Int(1)) => ref(0) </k>
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
            AugAssign(Name("total"), "+", Int(2))
            If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
              Expr(Call(Attribute(Name("result"), "append"), Name("factorial"))),
              Expr(Call(Attribute(Name("result"), "append"), Name("total"))))
            AugAssign(Name("i"), "+", Int(1)))
          Return(Name("result")), 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(vCons(1, .ValSeq)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires true
    [label(body-mutant-one)]
endmodule
