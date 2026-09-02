requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation of the real entry claim: the exact submitted program
  // returns true for "A", so requiring pyBool(false) must get stuck.
  claim [false-single-letter]:
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
            ~> runEntry("check_if_last_char_is_a_letter", "A")
            => pyBool(false)
          ... </k>
endmodule
