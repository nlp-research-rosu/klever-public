requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // False result obligation: every execution is required to return one more
  // than the semantics actually computes. S = "" is a concrete witness.
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
            noResult
            => Int(lengthString(S) +Int 1)
          </result>
        </py>
endmodule
