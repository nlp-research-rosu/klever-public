requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable witness decimal=0:
  // the real result is "db0db", not "db1db".
  claim [wrong-zero-result]:
    <k>
      Call(Name("decimal_to_binary"), (0, .Exprs))
      => str(
           iCons(100,
             iCons(98,
               iCons(49,
                 iCons(100, iCons(98, .IntSeq))))))
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
                      Int(48),
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
