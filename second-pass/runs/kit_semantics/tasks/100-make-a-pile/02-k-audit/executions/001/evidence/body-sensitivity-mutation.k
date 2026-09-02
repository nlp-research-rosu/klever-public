requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed program term is changed from n + 2*i to n + 4*i. At n = 2
  // this produces [2, 6], while the postcondition deliberately retains the
  // original implementation's [2, 4].
  claim [changed-executed-body]:
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
              BinOp("+", Name("n"), BinOp("*", Int(4), Name("i")))))
          AugAssign(Name("i"), "+", Int(1)))
        Return(Name("pile")))))
      ~> Call(Name("make_a_pile"), Int(2))
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
                  BinOp("+", Name("n"), BinOp("*", Int(4), Name("i")))))
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
      0 |-> list(vCons(2, vCons(4, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
