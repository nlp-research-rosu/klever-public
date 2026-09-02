requires "verification.k"

module SPEC-BODY-MUTATION-AUDIT
  imports VERIFICATION

  // The actual executed program term is mutated: length == 1 becomes length == 2.
  // The original postcondition is deliberately retained.  S = "A" is a witness.
  claim <k> Module(
            FuncDef("check_if_last_char_is_a_letter", Params("txt"),
              Return(
                BoolOp(
                  "or",
                  BoolOp(
                    "and",
                    Compare(Call(Name("len"), Name("txt")),
                            CmpOp("==", Int(2))),
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
endmodule
