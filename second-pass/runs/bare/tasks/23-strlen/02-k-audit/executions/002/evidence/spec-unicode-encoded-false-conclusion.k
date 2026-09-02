requires "verification.k"

module SPEC-UNICODE-ENCODED-FALSE-CONCLUSION
  imports VERIFICATION

  // krun maps the normal input literal "😀" to this four-byte K String.
  // The universal target claim therefore has this ground instance, returning
  // 4 even though Python strlen("😀") returns 1.
  claim <py>
          <k>
            Module(
              FuncDef(
                "strlen",
                Params("string"),
                Return(Call(Name("len"), Name("string")))
              )
            )
            ~> invoke(
                 "strlen",
                 Str("\xf0\x9f\x98\x80")
               )
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
            .Map
            => "string" |-> Str("\xf0\x9f\x98\x80")
          </locals>
          <result> noResult => Int(4) </result>
        </py>
endmodule
