requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  claim
    <k> solutionProgram
      => Module(
         FuncDef("can_arrange", Params("arr"),
           Assign(Name("result"), UnaryOp("-", Int(1)))
           Assign(Name("index"), Int(0))
           Assign(Name("previous"), Int(0))
           For(Name("current"), Name("arr"),
             If(Compare(Name("index"), CmpOp(">", Int(0))),
               If(Compare(Name("current"), CmpOp("<", Name("previous"))),
                 Assign(Name("result"), Name("index")),
                 .Stmts),
               .Stmts)
             Assign(Name("previous"), Name("current"))
             Assign(Name("index"), BinOp("+", Name("index"), Int(1))))
           Return(Name("result"))))
    </k>
    [label(program-constructor-pinning)]

  claim
    <k> arrangeBody
      => If(Compare(Name("index"), CmpOp(">", Int(0))),
         If(Compare(Name("current"), CmpOp("<", Name("previous"))),
            Assign(Name("result"), Name("index")),
            .Stmts),
         .Stmts)
       Assign(Name("previous"), Name("current"))
       Assign(Name("index"), BinOp("+", Name("index"), Int(1)))
    </k>
    [label(loop-body-constructor-pinning)]
endmodule
