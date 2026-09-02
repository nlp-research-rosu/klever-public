requires "verification.k"

module SPEC-BODY-SENSITIVITY-AUDIT
  imports VERIFICATION

  // Fresh body mutation: the final source-level comparison is x == 0 rather
  // than x == 1.  On (8,2), fixed execution reaches x=1 and returns false.
  claim [mutated-final-return]:
    <k>
      Call(Name("is_simple_power"), (8, 2, .Exprs))
      => true
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
              Compare(Name("x"), CmpOp("==", Int(0)))) .Stmts),
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
