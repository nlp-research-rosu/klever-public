requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Body sensitivity: the actual executed body is changed to return 0,
  // while the claimed result remains the string length.
  claim <py>
          <k>
            Module(
              FuncDef(
                "strlen",
                Params("string"),
                Return(Int(0))
              )
            )
            ~> invoke("strlen", Str(S))
            => .K
          </k>
          <functions>
            .Map
            => "strlen" |-> function(
                 "string",
                 Return(Int(0))
               )
          </functions>
          <locals> .Map => "string" |-> Str(S) </locals>
          <result> noResult => Int(lengthString(S)) </result>
        </py>
endmodule
