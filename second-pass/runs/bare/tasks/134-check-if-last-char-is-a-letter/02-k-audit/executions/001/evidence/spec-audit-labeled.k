requires "verification.k"

module SPEC-AUDIT
  imports VERIFICATION

  claim [entry]:
        <k> Module(
              FuncDef("check_if_last_char_is_a_letter", Params("txt"),
                Return(
                  BoolOp(
                    "or",
                    BoolOp(
                      "and",
                      Compare(Call(Name("len"), Name("txt")),
                              CmpOp("==", Int(1))),
                      Call(Attribute(Name("txt"), "isalpha"), .Exprs)),
                    BoolOp(
                      "and",
                      Compare(Call(Name("len"), Name("txt")),
                              CmpOp(">", Int(1))),
                      Call(
                        Attribute(
                          Subscript(Name("txt"), UnaryOp("-", Int(1))),
                          "isalpha"),
                        .Exprs),
                      Compare(
                        Subscript(Name("txt"), UnaryOp("-", Int(2))),
                        CmpOp("==", Str(" "))))))))
            ~> runEntry("check_if_last_char_is_a_letter", S)
            => pyBool(standaloneLastLetter(S))
          ... </k>

  claim [empty]:
        <k> standaloneLastLetter("") => false ... </k>

  claim [apple-pie]:
        <k> standaloneLastLetter("apple pie") => false ... </k>

  claim [apple-pi-e]:
        <k> standaloneLastLetter("apple pi e") => true ... </k>

  claim [trailing-space]:
        <k> standaloneLastLetter("apple pi e ") => false ... </k>

  claim [single-letter]:
        <k> standaloneLastLetter("A") => true ... </k>
endmodule
