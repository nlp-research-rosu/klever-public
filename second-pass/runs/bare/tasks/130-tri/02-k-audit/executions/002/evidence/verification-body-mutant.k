requires "semantic.k"

module TRI-VERIFICATION-BODY-MUTANT
  imports TRI-SEMANTIC

  // Material mutation of the program term itself: the final factor is n + 7
  // instead of n + 5, so tri(1) returns [1, 4] instead of [1, 3].
  syntax Program ::= "mutatedSolutionProgram" [macro]
  rule mutatedSolutionProgram =>
    Module(
      FuncDef("tri", Params("n"),
        If(Compare(Name("n"), CmpOp("==", Int(0))),
          Return(ListExpr(Int(1))),
          .Stmts)
        If(Compare(BinOp("%", Name("n"), Int(2)),
                   CmpOp("==", Int(0))),
          Return(
            BinOp("+",
              Call(Name("tri"), BinOp("-", Name("n"), Int(1))),
              ListExpr(BinOp("+", Int(1),
                             BinOp("//", Name("n"), Int(2)))))),
          .Stmts)
        Return(
          BinOp("+",
            Call(Name("tri"), BinOp("-", Name("n"), Int(1))),
            ListExpr(
              BinOp("*",
                BinOp("//", BinOp("+", Name("n"), Int(1)), Int(2)),
                BinOp("//", BinOp("+", Name("n"), Int(7)), Int(2))))))))
endmodule

