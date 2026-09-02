requires "verification-base.k"

module IDENTITY-MUTATION
  imports VERIFICATION-BASE

  // Deliberately false: changing += 1 to += 2 must not produce the exact
  // closure abbreviation used by the proof.
  claim [mutated-body-is-not-the-solution]:
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
              AugAssign(Name("candidate"), "+", Int(2)))
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
