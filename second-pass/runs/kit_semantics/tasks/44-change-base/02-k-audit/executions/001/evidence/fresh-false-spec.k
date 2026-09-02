requires "verification.k"

module FRESH-FALSE-SPEC
  imports VERIFICATION

  // Reviewer-authored false result: 8 in base 3 is "22", not "23".
  claim [wrong-ground-result]:
    <k>
      Call(Name("change_base"), (8, 3, .Exprs))
      =>
      str(iCons(50, iCons(51, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "change_base" |->
          closureVal(
            ("x", "base", .ParamNames),
            If(
              Compare(Name("x"), CmpOp("==", Int(0))),
              Return(Str("0")) .Stmts,
              .Stmts)
            Assign(Name("sign"), Str(""))
            If(
              Compare(Name("x"), CmpOp("<", Int(0))),
              Assign(Name("sign"), Str("-"))
              Assign(Name("x"), UnaryOp("-", Name("x")))
              .Stmts,
              .Stmts)
            Assign(Name("result"), Str(""))
            While(
              Compare(Name("x"), CmpOp(">", Int(0))),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Call(
                    Name("chr"),
                    (BinOp(
                       "+",
                       Int(48),
                       BinOp("%", Name("x"), Name("base"))),
                     .Exprs)),
                  Name("result")))
              Assign(Name("x"), BinOp("//", Name("x"), Name("base")))
              .Stmts)
            Return(BinOp("+", Name("sign"), Name("result")))
            .Stmts,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
