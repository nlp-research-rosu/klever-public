requires "/tmp/audit-work/audit96/verification.k"

module AUDIT-FALSE-RESULT-SPEC
  imports COUNT-UP-TO-WITH-OUTER

  // Fresh result mutation: the real body is unchanged, but it is falsely
  // required to return heap reference 1 although its sole result is at 0.
  claim
    <k>
      Assign(Name("result"), ListExpr(.Exprs))
      Assign(Name("candidate"), Int(2))
      Assign(Name("is_prime"), Bool(true))
      Assign(Name("divisor"), Int(2))
      While(
        Compare(Name("candidate"), CmpOp("<", Name("n"))),
        While(
          Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
          If(
            Compare(
              BinOp("%", Name("candidate"), Name("divisor")),
              CmpOp("==", Int(0))),
            Assign(Name("is_prime"), Bool(false)),
            .Stmts)
          AugAssign(Name("divisor"), "+", Int(1)))
        If(
          Name("is_prime"),
          Expr(Call(
            Attribute(Name("result"), "append"),
            Name("candidate"))),
          .Stmts)
        AugAssign(Name("candidate"), "+", Int(1))
        Assign(Name("is_prime"), Bool(true))
        Assign(Name("divisor"), Int(2)))
      Return(Name("result"))
      ~> #endcall
    => ref(1)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope("n" |-> N:Int, parent(0)))
    =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map => 0 |-> list(primesAcc(.ValSeq, 2, N)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires N >=Int 2
endmodule
