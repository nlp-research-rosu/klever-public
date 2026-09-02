requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [pile-loop]:
    <k>
      #while(
        Compare(Name("i"), CmpOp("<", Name("n"))),
        Expr(
          Call(
            Attribute(Name("pile"), "append"),
            BinOp("+", Name("n"), BinOp("*", Int(2), Name("i")))))
        AugAssign(Name("i"), "+", Int(1)))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "n"    |-> N:Int
        "pile" |-> ref(H:Int)
        "i"    |-> (I:Int => N)
        .Map,
        parent(0))
      ...
    </scopes>
    <heap>
      ...
      H |-> list(A:ValSeq => finishPile(A, N, I))
      ...
    </heap>
    requires N >=Int 0
     andBool I >=Int 0
     andBool I <=Int N

  claim [make-a-pile]:
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
      ~> Call(Name("make_a_pile"), N:Int)
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
      0 |-> list(finishPile(.ValSeq, N, 0))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >Int 0
endmodule
