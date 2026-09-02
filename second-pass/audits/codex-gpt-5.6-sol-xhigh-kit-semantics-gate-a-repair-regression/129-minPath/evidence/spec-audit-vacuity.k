requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  claim [prompt-examples]:
    <k>
      #loadAll(
        Module(
          FuncDef("minPath", Params("grid", "k"),
            Assign(Name("n"), Call(Name("len"), Name("grid")))
            Assign(Name("one_row"), Int(0))
            Assign(Name("one_col"), Int(0))
            Assign(Name("i"), Int(0))
            While(Compare(Name("i"), CmpOp("<", Name("n"))),
              Assign(Name("j"), Int(0))
              While(Compare(Name("j"), CmpOp("<", Name("n"))),
                If(Compare(
                  Subscript(Subscript(Name("grid"), Name("i")), Name("j")),
                  CmpOp("==", Int(1))),
                  Assign(Name("one_row"), Name("i"))
                  Assign(Name("one_col"), Name("j")),
                  .Stmts)
                Assign(Name("j"), BinOp("+", Name("j"), Int(1))))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
            Assign(Name("neighbors"), ListExpr(.Exprs))
            If(Compare(Name("one_row"), CmpOp(">", Int(0))),
              Expr(
                Call(
                  Attribute(Name("neighbors"), "append"),
                  Subscript(
                    Subscript(Name("grid"), BinOp("-", Name("one_row"), Int(1))),
                    Name("one_col")))),
              .Stmts)
            If(Compare(BinOp("+", Name("one_row"), Int(1)), CmpOp("<", Name("n"))),
              Expr(
                Call(
                  Attribute(Name("neighbors"), "append"),
                  Subscript(
                    Subscript(Name("grid"), BinOp("+", Name("one_row"), Int(1))),
                    Name("one_col")))),
              .Stmts)
            If(Compare(Name("one_col"), CmpOp(">", Int(0))),
              Expr(
                Call(
                  Attribute(Name("neighbors"), "append"),
                  Subscript(
                    Subscript(Name("grid"), Name("one_row")),
                    BinOp("-", Name("one_col"), Int(1))))),
              .Stmts)
            If(Compare(BinOp("+", Name("one_col"), Int(1)), CmpOp("<", Name("n"))),
              Expr(
                Call(
                  Attribute(Name("neighbors"), "append"),
                  Subscript(
                    Subscript(Name("grid"), Name("one_row")),
                    BinOp("+", Name("one_col"), Int(1))))),
              .Stmts)
            Assign(Name("next_value"), Call(Name("min"), Name("neighbors")))
            Assign(Name("answer"), ListExpr(.Exprs))
            Assign(Name("i"), Int(0))
            While(Compare(Name("i"), CmpOp("<", Name("k"))),
              If(Compare(BinOp("%", Name("i"), Int(2)), CmpOp("==", Int(0))),
                Expr(Call(Attribute(Name("answer"), "append"), Int(1))),
                Expr(
                  Call(Attribute(Name("answer"), "append"), Name("next_value"))))
              Assign(Name("i"), BinOp("+", Name("i"), Int(1))))
            Return(Name("answer")))
          Assert(
            Compare(
              Call(
                Name("minPath"),
                ListExpr(
                  ListExpr(Int(1), Int(2), Int(3)),
                  ListExpr(Int(4), Int(5), Int(6)),
                  ListExpr(Int(7), Int(8), Int(9))),
                Int(3)),
              CmpOp("==", ListExpr(Int(1), Int(2), Int(1)))))
          Assert(
            Compare(
              Call(
                Name("minPath"),
                ListExpr(
                  ListExpr(Int(5), Int(9), Int(3)),
                  ListExpr(Int(4), Int(1), Int(6)),
                  ListExpr(Int(7), Int(8), Int(2))),
                Int(1)),
              CmpOp("==", ListExpr(Int(1)))))
          Assert(
            Compare(
              Call(
                Name("minPath"),
                ListExpr(
                  ListExpr(Int(1), A:Int),
                  ListExpr(B:Int, C:Int)),
                Int(4)),
              CmpOp("==",
                ListExpr(Int(1), minInt(A, B), Int(1), minInt(A, B)))))
          Assert(
            Compare(
              Call(
                Name("minPath"),
                ListExpr(
                  ListExpr(A:Int, Int(1)),
                  ListExpr(B:Int, C:Int)),
                Int(4)),
              CmpOp("==",
                ListExpr(Int(1), minInt(A, C), Int(1), minInt(A, C)))))
          Assert(
            Compare(
              Call(
                Name("minPath"),
                ListExpr(
                  ListExpr(A:Int, B:Int),
                  ListExpr(Int(1), C:Int)),
                Int(4)),
              CmpOp("==",
                ListExpr(Int(1), minInt(A, C), Int(1), minInt(A, C)))))
          Assert(
            Compare(
              Call(
                Name("minPath"),
                ListExpr(
                  ListExpr(A:Int, B:Int),
                  ListExpr(C:Int, Int(1))),
                Int(4)),
              CmpOp("==",
                ListExpr(
                  Int(1), minInt(B, C), Int(1), minInt(B, C) +Int 1))))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      => ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => ?HEAP:Map </heap>
    <heapLoc> 0 => ?HEAPLOC:Int </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 2 <=Int A andBool A <=Int 4
     andBool 2 <=Int B andBool B <=Int 4
     andBool 2 <=Int C andBool C <=Int 4
     andBool A =/=Int B andBool A =/=Int C andBool B =/=Int C
endmodule
