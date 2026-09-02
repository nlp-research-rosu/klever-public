requires "reference-semantics/semantics.k"

module FIXED-HARNESS-LLVM
  imports MPY-KRUN

  syntax Stmt ::= "RunFixed"
  syntax KItem ::= "#observeFixedLLVM"

  rule <k> ref(H:Int) ~> #observeFixedLLVM => V ... </k>
       <heap> ... H |-> V:Val ... </heap>

  rule <k> RunFixed ~> .Stmts
        => #loadAll(Module(
             ImportFrom("typing", "List")
             FuncDef(
               "rescale_to_unit",
               Params("numbers"),
               CellVars("max_number", "min_number"),
               FreeVars(.ParamNames),
               Assign(
                 Name("min_number"),
                 Call(Name("min"), Name("numbers")))
               Assign(
                 Name("max_number"),
                 Call(Name("max"), Name("numbers")))
               Return(
                 ListComp(
                   BinOp(
                     "/",
                     BinOp("-", Name("number"), Name("min_number")),
                     BinOp("-", Name("max_number"), Name("min_number"))),
                   CompFor(
                     Name("number"),
                     Name("numbers"),
                     Bool(true)))))))
           ~> Call(
                Name("rescale_to_unit"),
                list(vCons(1.0, vCons(2.0, .ValSeq))))
           ~> #observeFixedLLVM
       </k>
endmodule
