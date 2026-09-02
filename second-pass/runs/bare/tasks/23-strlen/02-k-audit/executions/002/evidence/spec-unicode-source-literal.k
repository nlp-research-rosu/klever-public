requires "verification.k"

module SPEC-UNICODE-FALSE-CONCLUSION
  imports VERIFICATION

  // In Python strlen("😀") is 1. This ground claim demonstrates that the
  // candidate semantics instead makes the false real-program conclusion 4.
  claim <py>
          <k>
            Module(
              FuncDef(
                "strlen",
                Params("string"),
                Return(Call(Name("len"), Name("string")))
              )
            )
            ~> invoke("strlen", Str("\U0001F600"))
            => .K
          </k>
          <functions>
            .Map
            => "strlen" |-> function(
                 "string",
                 Return(Call(Name("len"), Name("string")))
               )
          </functions>
          <locals>
            .Map => "string" |-> Str("\U0001F600")
          </locals>
          <result> noResult => Int(4) </result>
        </py>
endmodule
