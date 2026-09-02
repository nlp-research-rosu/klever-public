requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Auditor-authored false result: digits(235) is 15, not 16.
  claim [audit-false-result-235]:
    <k>
      #loadAll(
        Module(
          FuncDef("digits", Params("n"),
            Assign(Name("product"), Int(1))
            Assign(Name("found"), Int(0))
            While(Compare(Name("n"), CmpOp(">", Int(0))),
              If(
                Compare(
                  BinOp("%", Name("n"), Int(2)),
                  CmpOp("==", Int(1))),
                Assign(
                  Name("product"),
                  BinOp(
                    "*",
                    Name("product"),
                    BinOp("%", Name("n"), Int(10))))
                Assign(Name("found"), Int(1)),
                .Stmts)
              Assign(
                Name("n"),
                BinOp("//", Name("n"), Int(10)))
              .Stmts)
            Return(
              BinOp("*", Name("product"), Name("found")))
            .Stmts)
          .Stmts))
      ~> Call(Name("digits"), Int(235))
      => 16
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => ?GLOBALS:Map, parent(-1))
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
