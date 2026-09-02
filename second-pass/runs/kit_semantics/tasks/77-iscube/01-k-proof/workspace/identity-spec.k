requires "verification-base.k"

module IDENTITY
  imports VERIFICATION-BASE

  // Loading the translated source creates exactly the closure used by SPEC.
  claim [solution-loads-exact-closure]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "iscube",
            Params("a"),
            If(
              Compare(Name("a"), CmpOp("<", Int(0))),
              Assign(Name("a"), UnaryOp("-", Name("a"))),
              .Stmts)
            Assign(Name("candidate"), Int(0))
            While(
              Compare(
                BinOp(
                  "*",
                  BinOp("*", Name("candidate"), Name("candidate")),
                  Name("candidate")),
                CmpOp("<", Name("a"))),
              AugAssign(Name("candidate"), "+", Int(1)))
            Return(
              Compare(
                BinOp(
                  "*",
                  BinOp("*", Name("candidate"), Name("candidate")),
                  Name("candidate")),
                CmpOp("==", Name("a")))))))
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
         0 |-> scope(.Map, parent(-1))
      =>
        -1 |-> builtinsScope
         0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
