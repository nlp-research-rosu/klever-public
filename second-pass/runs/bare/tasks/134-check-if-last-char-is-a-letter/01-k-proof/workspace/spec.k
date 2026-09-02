requires "verification.k"

module SPEC
  imports VERIFICATION

  // The translated Python program agrees with the independently named
  // contract predicate for every input string.
  claim <k> Module(
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

  claim <k> standaloneLastLetter("") => false ... </k>
  claim <k> standaloneLastLetter("apple pie") => false ... </k>
  claim <k> standaloneLastLetter("apple pi e") => true ... </k>
  claim <k> standaloneLastLetter("apple pi e ") => false ... </k>
  claim <k> standaloneLastLetter("A") => true ... </k>
endmodule
