requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: the result is constrained to one more than execution.
  // S="" is a concrete satisfying witness: execution returns 0, target demands 1.
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
          <result>
            noResult => Int(lengthString(S) +Int 1)
          </result>
        </py>
endmodule
