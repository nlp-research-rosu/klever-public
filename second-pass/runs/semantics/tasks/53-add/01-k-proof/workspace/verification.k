requires "reference-semantics/semantics.k"

module ADD-VERIFICATION
  imports MPY

  // The loaded function below is exactly the AST emitted in solution.mpy.
  syntax KItem ::= "#callAdd" "(" Int "," Int ")"

  rule <k> #callAdd(X:Int, Y:Int)
        => #loadAll(
             Module(
               FuncDef("add", Params("x", "y"),
                 Return(BinOp("+", Name("x"), Name("y"))))))
           ~> Call(Name("add"), Int(X), Int(Y))
           ...
       </k>
endmodule
