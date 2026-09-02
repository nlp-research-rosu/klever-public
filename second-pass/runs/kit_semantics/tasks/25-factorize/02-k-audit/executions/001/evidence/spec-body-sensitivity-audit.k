requires "verification.k"

module SPEC-BODY-SENSITIVITY-AUDIT
  imports VERIFICATION

  // The program term executed by this claim is materially changed: the local
  // divisor is initialized to 3. At input 4 it returns [4], not [2,2].
  claim [audit-mutated-body]:
    <k>
      Call(Name("factorize"), (Int(4), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "factorize" |->
          closureVal(
            "n",
            Assign(Name("factors"), ListExpr(.Exprs))
            Assign(Name("divisor"), Int(3))
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
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(2, vCons(2, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
