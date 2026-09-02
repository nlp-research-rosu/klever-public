requires "verification.k"

module SPEC-FALSE-RESULT-AUDIT
  imports VERIFICATION

  // Fresh false postcondition: 16 = (-2)^4, so the real body must return true.
  claim [false-result-16-neg2]:
    <k>
      Call(Name("is_simple_power"), (16, -2, .Exprs))
      => false
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
