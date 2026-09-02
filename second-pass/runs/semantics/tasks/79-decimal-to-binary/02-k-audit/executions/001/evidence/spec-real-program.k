requires "verification.k"

module SPEC-REAL-PROGRAM
  imports VERIFICATION

  claim <k>
          #loadAll(
            Module(
              FuncDef(
                "decimal_to_binary",
                Params("decimal"),
                Return(
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      Str("db"),
                      Subscript(
                        Call(Name("bin"), Name("decimal")),
                        Slice(Int(2), NoBound, NoBound))),
                    Str("db")))
                .Stmts)
              .Stmts))
          ~> Call(Name("decimal_to_binary"), N)
        =>
          str(
            iCons(
              100,
              iCons(
                98,
                seqConcat(
                  binCodes(N),
                  iCons(100, iCons(98, .IntSeq))))))
        </k>
        <env> 0 </env>
        <scopes>
           0 |-> scope(
                  "decimal_to_binary" |->
                    closureVal(
                      "decimal",
                      Return(
                        BinOp(
                          "+",
                          BinOp(
                            "+",
                            Str("db"),
                            Subscript(
                              Call(Name("bin"), Name("decimal")),
                              Slice(Int(2), NoBound, NoBound))),
                          Str("db")))
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
    requires N >=Int 0
    [label(actual-module-symbolic)]
endmodule
