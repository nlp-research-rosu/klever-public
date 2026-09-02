requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [trial-loop]:
    <k>
      #while(
        Compare(Name("i"), CmpOp("<", Name("n"))),
        If(
          Compare(
            BinOp("%", Name("n"), Name("i")),
            CmpOp("==", Int(0))),
          Assign(Name("result"), Name("y")) .Stmts,
          .Stmts)
        Assign(Name("i"), BinOp("+", Name("i"), Int(1))) .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      SCOPES:Map
      1 |-> scope(
        "n" |-> N:Int
        "x" |-> X:Val
        "y" |-> Y:Val
        "i" |-> (I:Int => N)
        "result" |-> (R:Val => trialChoice(N, I, R, Y)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP </heap>
    <heapLoc> HEAPLOC </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> EXIT </exit-code>
    requires I >=Int 2 andBool I <=Int N

  claim [x-or-y]:
    <k>
      #loadAll(
        Module(
          FuncDef("x_or_y", Params("n", "x", "y"),
            If(
              Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")) .Stmts,
              .Stmts)
            Assign(Name("i"), Int(2))
            Assign(Name("result"), Name("x"))
            While(
              Compare(Name("i"), CmpOp("<", Name("n"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("i")),
                  CmpOp("==", Int(0))),
                Assign(Name("result"), Name("y")) .Stmts,
                .Stmts)
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))) .Stmts)
            Return(Name("result")) .Stmts)))
      ~> Call(Name("x_or_y"), N:Int, X:Val, Y:Val)
      => ?V:Val
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "x_or_y" |->
          closureVal(
            "n", "x", "y", .ParamNames,
            If(
              Compare(Name("n"), CmpOp("<", Int(2))),
              Return(Name("y")) .Stmts,
              .Stmts)
            Assign(Name("i"), Int(2))
            Assign(Name("result"), Name("x"))
            While(
              Compare(Name("i"), CmpOp("<", Name("n"))),
              If(
                Compare(
                  BinOp("%", Name("n"), Name("i")),
                  CmpOp("==", Int(0))),
                Assign(Name("result"), Name("y")) .Stmts,
                .Stmts)
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))) .Stmts)
            Return(Name("result")) .Stmts,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    ensures ?V ==K xOrYSpec(N, X, Y)
endmodule
