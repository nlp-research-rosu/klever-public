requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  // Operational-sensitivity mutant: the submitted len call is replaced by 0.
  syntax Module ::= "strlenModuleMutant" [macro]
  rule strlenModuleMutant
    => Module(
         FuncDef(
           "strlen",
           Params("string"),
           Return(Int(0))
         )
       )

  syntax KItem ::= "#invokeStrlenMutant" "(" Val ")"
  rule <k> #invokeStrlenMutant(V:Val)
        => #loadAll(strlenModuleMutant) ~> Call(Name("strlen"), V) ... </k>
endmodule
