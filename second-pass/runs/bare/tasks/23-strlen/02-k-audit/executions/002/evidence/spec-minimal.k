requires "verification-minimal.k"

module SPEC-MINIMAL
  imports VERIFICATION-MINIMAL

  claim <py>
          <k>
            Module(
              FuncDef(
                "strlen",
                Params("string"),
                Return(Call(Name("len"), Name("string")))
              )
            )
            ~> invoke("strlen", Str(S))
            => .K
          </k>
          <functions>
            .Map
            => "strlen" |-> function(
                 "string",
                 Return(Call(Name("len"), Name("string")))
               )
          </functions>
          <locals> .Map => "string" |-> Str(S) </locals>
          <result> noResult => Int(lengthString(S)) </result>
        </py>
endmodule
