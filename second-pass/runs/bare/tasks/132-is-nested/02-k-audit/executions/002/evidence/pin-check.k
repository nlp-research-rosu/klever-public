requires "verification.k"

module PIN-CHECK
  imports VERIFICATION

  // The RHS below is the exact constructor tree in the freshly regenerated
  // solution.mpy. This claim checks that all three proof-local AST names
  // expand to that tree, without invoking the program semantics.
  claim
    <k> theSolution ~> start(BS:BString) =>
         Module(
           FuncDef("is_nested", Params("string"),
             Assign(Name("state"), Int(0))
             For(Name("bracket"), Name("string"),
               If(Compare(Name("bracket"), CmpOp("==", Str("["))),
                 If(Compare(Name("state"), CmpOp("<", Int(2))),
                   Assign(Name("state"), BinOp("+", Name("state"), Int(1))),
                   .Stmts),
                 If(Compare(Name("state"), CmpOp("==", Int(2))),
                   Assign(Name("state"), Int(3)),
                   If(Compare(Name("state"), CmpOp("==", Int(3))),
                     Return(Bool(true)),
                     .Stmts))))
             Return(Bool(false))))
         ~> start(BS)
    </k>
    <functions> .Map </functions>
    <env> .Map </env>
    <result> noResult </result>
endmodule
