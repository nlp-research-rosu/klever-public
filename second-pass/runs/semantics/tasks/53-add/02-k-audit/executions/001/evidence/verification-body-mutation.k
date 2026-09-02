requires "reference-semantics/semantics.k"

module ADD-VERIFICATION-BODY-MUTATION
  imports MPY

  syntax KItem ::= "#callAddBodyMutation" "(" Int "," Int ")"

  // Operational-sensitivity mutation: the submitted "+" body is changed to "-".
  rule <k> #callAddBodyMutation(X:Int, Y:Int)
        => #loadAll(
             Module(
               FuncDef("add", Params("x", "y"),
                 Return(BinOp("-", Name("x"), Name("y"))))))
           ~> Call(Name("add"), Int(X), Int(Y))
           ...
       </k>
endmodule
