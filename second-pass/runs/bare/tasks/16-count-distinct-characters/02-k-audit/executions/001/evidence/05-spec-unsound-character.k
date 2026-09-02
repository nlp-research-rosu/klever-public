requires "verification.k"

module SPEC-UNSOUND-CHARACTER
  imports VERIFICATION

  // The actual -cINPUT route injects raw UTF-8 bytes for "😀", observed as
  // "\xf0\x9f\x98\x80". Candidate semantics says 4; the corresponding Python
  // string has one code point and set("😀") has exactly one element.
  claim [non-bmp-character-witness]:
    <k>
      Module(
        FuncDef("count_distinct_characters", Params("string"),
          Return(
            Call(
              Name("len"),
              Call(Name("set"),
                Call(Attribute(Name("string"), "lower"), .Exprs))))))
      => .K
    </k>
    <env>
      .Map => "string" |-> StrVal("\xf0\x9f\x98\x80")
    </env>
    <input> "\xf0\x9f\x98\x80" </input>
    <result> noResult => IntVal(4) </result>
endmodule
