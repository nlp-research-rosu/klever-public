requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [factor-loop]:
    <k>
      #while(
        Compare(Name("divisor"), CmpOp("<=", Name("n"))),
        If(
          Compare(
            BinOp("%", Name("n"), Name("divisor")),
            CmpOp("==", Int(0))),
          Expr(
            Call(
              Attribute(Name("factors"), "append"),
              Name("divisor")))
          Assign(
            Name("n"),
            BinOp("//", Name("n"), Name("divisor"))),
          Assign(
            Name("divisor"),
            BinOp("+", Name("divisor"), Int(1))))
        .Stmts)
      ~> (Return(Name("factors")) .Stmts)
      ~> #endcall
      =>
      (Return(Name("factors")) .Stmts)
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
        "factorize" |->
          closureVal(
            "n",
            Assign(Name("factors"), ListExpr(.Exprs))
            Assign(Name("divisor"), Int(2))
            While(
              Compare(Name("divisor"), CmpOp("<=", Name("n"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("divisor")),
                  CmpOp("==", Int(0))),
                Expr(
                  Call(
                    Attribute(Name("factors"), "append"),
                    Name("divisor")))
                Assign(
                  Name("n"),
                  BinOp("//", Name("n"), Name("divisor"))),
                Assign(
                  Name("divisor"),
                  BinOp("+", Name("divisor"), Int(1))))
              .Stmts)
            Return(Name("factors"))
            .Stmts,
            0),
        parent(-1))
      1 |-> scope(
        "n" |-> (N:Int => ?NF:Int)
        "divisor" |-> (D:Int => ?DF:Int)
        "factors" |-> ref(0),
        parent(0))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> list(A:ValSeq => factorAcc(A, N, D))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1 andBool D >=Int 2

  claim [factorize]:
    <k>
      Call(Name("factorize"), (Int(N:Int), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(
         "factorize" |->
           closureVal(
             "n",
             Assign(Name("factors"), ListExpr(.Exprs))
             Assign(Name("divisor"), Int(2))
             While(
               Compare(Name("divisor"), CmpOp("<=", Name("n"))),
               If(
                 Compare(
                   BinOp("%", Name("n"), Name("divisor")),
                   CmpOp("==", Int(0))),
                 Expr(
                   Call(
                     Attribute(Name("factors"), "append"),
                     Name("divisor")))
                 Assign(
                   Name("n"),
                   BinOp("//", Name("n"), Name("divisor"))),
                 Assign(
                   Name("divisor"),
                   BinOp("+", Name("divisor"), Int(1))))
               .Stmts)
             Return(Name("factors"))
             .Stmts,
             0),
         parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(factorAcc(.ValSeq, N, 2))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 1
endmodule
