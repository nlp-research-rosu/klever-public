requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [derivative-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("x"),
        If(
          Compare(Name("i"), CmpOp(">", Int(0))),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              (BinOp("*", Name("i"), Name("x")), .Exprs))),
          .Stmts)
        Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
        .Stmts)
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      SC:Map
      1 |-> scope(
        "xs"     |-> list(ORIG:ValSeq)
        "result" |-> ref(H:Int)
        "i"      |-> (I:Int => ?IF:Int)
        "x"      |-> (_X:Val => ?X:Val),
        parent(0))
    </scopes>
    <heap>
      H |-> list(ACC:ValSeq => derivAcc(ACC, VS, I))
      RESTHEAP:Map
    </heap>
    <heapLoc> HL:Int </heapLoc>
    <scopeLoc> 2 </scopeLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires I >=Int 0 andBool noRefsVS(VS)

  claim [derivative-entry]:
    <k>
      #loadAll(
        Module(
          FuncDef(
            "derivative",
            Params("xs"),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("i"), Int(0))
            Assign(Name("x"), NoneVal)
            For(
              Name("x"),
              Name("xs"),
              If(
                Compare(Name("i"), CmpOp(">", Int(0))),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    (BinOp("*", Name("i"), Name("x")), .Exprs))),
                .Stmts)
              Assign(Name("i"), BinOp("+", Name("i"), Int(1)))
              .Stmts)
            Return(Name("result"))
            .Stmts)))
      ~> Call(Name("derivative"), (list(INPUT:ValSeq), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(derivAcc(.ValSeq, INPUT, 0)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires noRefsVS(INPUT)
endmodule
