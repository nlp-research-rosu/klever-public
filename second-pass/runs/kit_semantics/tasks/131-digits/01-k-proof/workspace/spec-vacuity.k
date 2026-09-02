requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the real result for input 1 is 1, not 2.
  claim [digits-entry-off-by-one]:
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
      ~> Call(Name("digits"), Int(1))
      => 2
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
