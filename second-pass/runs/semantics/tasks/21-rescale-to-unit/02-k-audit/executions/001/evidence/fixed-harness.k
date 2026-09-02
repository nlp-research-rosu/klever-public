requires "reference-semantics/semantics.k"

module FIXED-HARNESS
  imports MPY

  syntax KItem ::= "#observeFixed"
  rule <k> ref(H:Int) ~> #observeFixed => V ... </k>
       <heap> ... H |-> V:Val ... </heap>

  syntax KItem ::= #runFixed(ValSeq)
  rule <k> #runFixed(VS:ValSeq)
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
           ~> Call(Name("rescale_to_unit"), list(VS))
           ~> #observeFixed
           ...
       </k>
endmodule
