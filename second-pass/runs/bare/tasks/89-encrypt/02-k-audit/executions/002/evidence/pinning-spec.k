requires "semantic.k"

module PINNING-SPEC
  imports MPY

  claim Module(FuncDef("encrypt", Params("s"), solutionBody))
    => Module(
         FuncDef("encrypt", Params("s"),
           If(Compare(Name("s"), CmpOp("==", Str(""))),
              Return(Str("")),
              .Stmts)
           Return(
             BinOp("+",
               Call(Name("chr"),
                 BinOp("+",
                   BinOp("%",
                     BinOp("+",
                       BinOp("-",
                         Call(Name("ord"), Subscript(Name("s"), Int(0))),
                         Int(97)),
                       Int(4)),
                     Int(26)),
                   Int(97))),
               Call(Name("encrypt"),
                 Subscript(Name("s"),
                   Slice(Int(1), NoBound, NoBound)))))))
endmodule
