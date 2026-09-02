requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [prime-loop]:
    <k>
      #while(
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
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(M:Map, parent(-1))
      1 |-> scope(
        "n"       |-> N
        "divisor" |-> (D => N)
        "result"  |-> (A => A andBool primeScan(N, D)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(FRAME:KItem) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires D >=Int 2 andBool D <=Int N

  claim [is-prime]:
    <k>
      Call(Name("is_prime"), (Int(N), .Exprs))
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
            Assign(Name("result"), Bool(true))
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
    ensures ?R ==Bool primeResult(N)
endmodule
