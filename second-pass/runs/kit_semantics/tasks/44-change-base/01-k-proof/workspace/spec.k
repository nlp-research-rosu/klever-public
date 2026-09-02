requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [loop-invariant]:
    <k>
      #while(
        Compare(Name("x"), CmpOp(">", Int(0))),
        Assign(
          Name("result"),
          BinOp(
            "+",
            Call(
              Name("chr"),
              (BinOp("+", Int(48), BinOp("%", Name("x"), Name("base"))),
               .Exprs)),
            Name("result")))
        Assign(Name("x"), BinOp("//", Name("x"), Name("base")))
        .Stmts)
      ~> (Return(BinOp("+", Name("sign"), Name("result"))) .Stmts)
      ~> #endcall
      =>
      (Return(BinOp("+", Name("sign"), Name("result"))) .Stmts)
      ~> #endcall
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "change_base" |->
          closureVal(
            ("x", "base", .ParamNames),
            If(
              Compare(Name("x"), CmpOp("==", Int(0))),
              Return(Str("0")) .Stmts,
              .Stmts)
            Assign(Name("sign"), Str(""))
            If(
              Compare(Name("x"), CmpOp("<", Int(0))),
              Assign(Name("sign"), Str("-"))
              Assign(Name("x"), UnaryOp("-", Name("x")))
              .Stmts,
              .Stmts)
            Assign(Name("result"), Str(""))
            While(
              Compare(Name("x"), CmpOp(">", Int(0))),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Call(
                    Name("chr"),
                    (BinOp(
                       "+",
                       Int(48),
                       BinOp("%", Name("x"), Name("base"))),
                     .Exprs)),
                  Name("result")))
              Assign(Name("x"), BinOp("//", Name("x"), Name("base")))
              .Stmts)
            Return(BinOp("+", Name("sign"), Name("result")))
            .Stmts,
            0),
        parent(-1))
      1 |-> scope(
        "x"      |-> (X:Int => 0)
        "base"   |-> B:Int
        "sign"   |-> str(_SIGN:IntSeq)
        "result" |-> (str(ACC:IntSeq) => str(baseAcc(X, B, ACC))),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires X >=Int 0
     andBool B >=Int 2
     andBool B <Int 10

  claim [change-base]:
    <k>
      Call(Name("change_base"), (X:Int, B:Int, .Exprs))
      =>
      str(changeBaseCodes(X, B))
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "change_base" |->
          closureVal(
            ("x", "base", .ParamNames),
            If(
              Compare(Name("x"), CmpOp("==", Int(0))),
              Return(Str("0")) .Stmts,
              .Stmts)
            Assign(Name("sign"), Str(""))
            If(
              Compare(Name("x"), CmpOp("<", Int(0))),
              Assign(Name("sign"), Str("-"))
              Assign(Name("x"), UnaryOp("-", Name("x")))
              .Stmts,
              .Stmts)
            Assign(Name("result"), Str(""))
            While(
              Compare(Name("x"), CmpOp(">", Int(0))),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Call(
                    Name("chr"),
                    (BinOp(
                       "+",
                       Int(48),
                       BinOp("%", Name("x"), Name("base"))),
                     .Exprs)),
                  Name("result")))
              Assign(Name("x"), BinOp("//", Name("x"), Name("base")))
              .Stmts)
            Return(BinOp("+", Name("sign"), Name("result")))
            .Stmts,
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires B >=Int 2
     andBool B <Int 10
endmodule
