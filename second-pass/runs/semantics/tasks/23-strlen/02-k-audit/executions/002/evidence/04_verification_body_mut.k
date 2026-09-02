requires "/tmp/audit-work/23-strlen-independent/rebuild/reference-semantics/semantics.k"

module VERIFICATION-BODY-MUT
  imports MPY

  syntax Module ::= "strlenModuleMut" [macro]
  rule strlenModuleMut
    => Module(
         FuncDef(
           "strlen",
           Params("string"),
           Return(Int(0))
         )
       )

  syntax KItem ::= "#invokeStrlenMut" "(" Val ")"
  rule <k> #invokeStrlenMut(V:Val)
        => #loadAll(strlenModuleMut) ~> Call(Name("strlen"), V) ... </k>
endmodule
