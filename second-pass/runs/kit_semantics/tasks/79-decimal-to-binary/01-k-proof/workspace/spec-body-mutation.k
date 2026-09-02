requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The closure is materially mutated from 48 + n % 2 to 49 + n % 2.
  // For decimal=2 it must not establish the real result "db10db".
  claim [mutated-body]:
    <k>
      Call(Name("decimal_to_binary"), (2, .Exprs))
      => str(
           iCons(100,
             iCons(98,
               iCons(49,
                 iCons(48,
                   iCons(100, iCons(98, .IntSeq)))))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "decimal_to_binary" |->
          closureVal(
            ("decimal", .ParamNames),
            Assign(Name("binary"), Str("db"))
            If(
              Compare(Name("decimal"), CmpOp("==", Int(0))),
              Assign(
                Name("binary"),
                BinOp("+", Str("0"), Name("binary"))),
              .Stmts)
            While(
              Compare(Name("decimal"), CmpOp("!=", Int(0))),
              Assign(
                Name("binary"),
                BinOp(
                  "+",
                  Call(
                    Name("chr"),
                    BinOp(
                      "+",
                      Int(49),
                      BinOp("%", Name("decimal"), Int(2)))),
                  Name("binary")))
              Assign(
                Name("decimal"),
                BinOp("//", Name("decimal"), Int(2))))
            Return(BinOp("+", Str("db"), Name("binary"))),
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
