requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately changed implementation: append n + 3*i, but demand the
  // original n + 2*i summary for the realizable input n = 3.
  claim [changed-multiplier]:
    <k>
      #loadAll(Module(FuncDef(
        "make_a_pile",
        Params("n"),
        Assign(Name("pile"), ListExpr(.Exprs))
        Assign(Name("i"), Int(0))
        While(
          Compare(Name("i"), CmpOp("<", Name("n"))),
          Expr(
            Call(
              Attribute(Name("pile"), "append"),
              BinOp("+", Name("n"), BinOp("*", Int(3), Name("i")))))
          AugAssign(Name("i"), "+", Int(1)))
        Return(Name("pile")))))
      ~> Call(Name("make_a_pile"), Int(3))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "make_a_pile" |->
          closureVal(
            ("n", .ParamNames),
            Assign(Name("pile"), ListExpr(.Exprs))
            Assign(Name("i"), Int(0))
            While(
              Compare(Name("i"), CmpOp("<", Name("n"))),
              Expr(
                Call(
                  Attribute(Name("pile"), "append"),
                  BinOp("+", Name("n"), BinOp("*", Int(3), Name("i")))))
              AugAssign(Name("i"), "+", Int(1)))
            Return(Name("pile")),
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(finishPile(.ValSeq, 3, 0))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
