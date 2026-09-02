requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
        Compare(Name("i"), CmpOp("<=", Name("n"))),
        AugAssign(Name("fact"), "*", Name("i"))
        AugAssign(Name("total"), "+", Name("i"))
        If(
          Compare(
            BinOp("%", Name("i"), Int(2)),
            CmpOp("==", Int(0))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              Name("fact"))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              Name("total"))))
        AugAssign(Name("i"), "+", Int(1)))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        "n"      |-> N:Int
        "result" |-> ref(H:Int)
        "fact"   |-> (F:Int => factRun(I, N, F))
        "total"  |-> (T:Int => totalRun(I, N, T))
        "i"      |-> (I:Int => N +Int 1),
        _P:Parent)
      ...
    </scopes>
    <heap>
      ...
      H |-> list(VS:ValSeq => resultRun(VS, I, N, F, T))
      ...
    </heap>
    requires I >=Int 1 andBool N >=Int I -Int 1

  claim [f-correct]:
    <k>
      Call(Name("f"), Int(N:Int))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "f" |->
          closureVal(
            ("n", .ParamNames),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("fact"), Int(1))
            Assign(Name("total"), Int(0))
            Assign(Name("i"), Int(1))
            While(
              Compare(Name("i"), CmpOp("<=", Name("n"))),
              AugAssign(Name("fact"), "*", Name("i"))
              AugAssign(Name("total"), "+", Name("i"))
              If(
                Compare(
                  BinOp("%", Name("i"), Int(2)),
                  CmpOp("==", Int(0))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    Name("fact"))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    Name("total"))))
              AugAssign(Name("i"), "+", Int(1)))
            Return(Name("result"))
            .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(999, resultRun(.ValSeq, 1, N, 1, 0)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
endmodule
