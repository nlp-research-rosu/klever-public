requires "verification.k"

module SPEC
  imports VERIFICATION

  // The translated program returns the mathematical length for every string.
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
