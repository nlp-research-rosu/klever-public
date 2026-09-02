requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Ground body-sensitivity probe. The digit offset is changed from 48 to 49,
  // while the expected result for change_base(8, 3) remains "22".
  claim [mutated-body]:
    <k>
      Call(Name("change_base"), (8, 3, .Exprs))
      =>
      str(iCons(50, iCons(50, .IntSeq)))
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
                       Int(49),
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
