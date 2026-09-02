requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately changes the source body: an odd digit no longer sets found.
  // The unchanged expected result for input 1 must therefore be rejected.
  claim [digits-mutated-body]:
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
                Assign(Name("found"), Int(0)),
                .Stmts)
              Assign(
                Name("n"),
                BinOp("//", Name("n"), Int(10)))
              .Stmts)
            Return(
              BinOp("*", Name("product"), Name("found")))
            .Stmts)
          .Stmts))
      ~> Call(Name("digits"), Int(1))
      => 1
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
