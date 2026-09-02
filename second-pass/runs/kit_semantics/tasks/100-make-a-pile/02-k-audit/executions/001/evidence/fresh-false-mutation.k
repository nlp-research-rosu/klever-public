requires "verification.k"

module AUDIT-SPEC-FALSE
  imports VERIFICATION

  // Fresh audit mutation. The exact submitted body is invoked at the
  // satisfying source-contract input n = 1, but the postcondition demands
  // the demonstrably false list [2] instead of the actual list [1].
  claim [wrong-list-at-one]:
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
              BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))))
          AugAssign(Name("i"), "+", Int(1)))
        Return(Name("pile")))))
      ~> Call(Name("make_a_pile"), Int(1))
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
                  BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))))
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
      0 |-> list(vCons(2, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
