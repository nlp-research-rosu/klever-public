requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // This is exactly the constructor tree generated in solution.mpy.
  syntax Module ::= "strlenModule" [macro]
  rule strlenModule
    => Module(
         FuncDef(
           "strlen",
           Params("string"),
           Return(Call(Name("len"), Name("string")))
         )
       )

  // Load the translated module and invoke its public entry point.
  syntax KItem ::= "#invokeStrlen" "(" Val ")"
  rule <k> #invokeStrlen(V:Val)
        => #loadAll(strlenModule) ~> Call(Name("strlen"), V) ... </k>
endmodule
