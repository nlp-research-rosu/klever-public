requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // Material program-term mutation: result starts false instead of true.
  // At n = 2 the loop is skipped, while primeResult(2) is true.
  claim [mutated-body-at-two]:
    <k>
      Call(Name("is_prime"), (Int(2), .Exprs))
      => ?R:Bool ~> .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_prime" |->
          closureVal(
            ("n", .ParamNames),
            If(
              Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Bool(false)),
              .Stmts)
            Assign(Name("divisor"), Int(2))
            Assign(Name("result"), Bool(false))
            While(
              Compare(Name("divisor"), CmpOp("<", Name("n"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("divisor")),
                  CmpOp("==", Int(0))),
                Assign(Name("result"), Bool(false)),
                .Stmts)
              Assign(
                Name("divisor"),
                BinOp("+", Name("divisor"), Int(1)))
              .Stmts)
            Return(Name("result"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?R ==Bool primeResult(2)
endmodule
