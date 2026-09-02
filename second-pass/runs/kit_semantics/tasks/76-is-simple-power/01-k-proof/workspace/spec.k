requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
        Compare(
          BinOp("%", Name("x"), Name("n")),
          CmpOp("==", Int(0))),
        Assign(
          Name("x"),
          BinOp("//", Name("x"), Name("n"))) .Stmts)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "x" |-> (X:Int => ?XF:Int)
        "n" |-> N:Int,
        parent(0))
      ...
    </scopes>
    requires X =/=Int 0
     andBool (N <=Int -2 orBool N >=Int 2)
    ensures (?XF ==Int 1) ==Bool simplePower(X, N)

  claim [is-simple-power]:
    <k>
      Call(
        Name("is_simple_power"),
        (X:Int, N:Int, .Exprs))
      => simplePower(X, N)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "is_simple_power" |->
          closureVal(
            ("x", "n", .ParamNames),
            (If(
              Compare(Name("x"), CmpOp("==", Int(1))),
              Return(Bool(true)) .Stmts,
              .Stmts)
            If(
              Compare(Name("n"), CmpOp("==", Int(0))),
              Return(
                Compare(Name("x"), CmpOp("==", Int(0)))) .Stmts,
              .Stmts)
            If(
              Compare(Name("n"), CmpOp("==", Int(1))),
              Return(Bool(false)) .Stmts,
              .Stmts)
            If(
              Compare(
                Name("n"),
                CmpOp("==", UnaryOp("-", Int(1)))),
              Return(
                Compare(
                  Name("x"),
                  CmpOp("==", UnaryOp("-", Int(1))))) .Stmts,
              .Stmts)
            If(
              Compare(Name("x"), CmpOp("==", Int(0))),
              Return(Bool(false)) .Stmts,
              .Stmts)
            While(
              Compare(
                BinOp("%", Name("x"), Name("n")),
                CmpOp("==", Int(0))),
              Assign(
                Name("x"),
                BinOp("//", Name("x"), Name("n"))) .Stmts)
            Return(
              Compare(Name("x"), CmpOp("==", Int(1)))) .Stmts),
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
endmodule
