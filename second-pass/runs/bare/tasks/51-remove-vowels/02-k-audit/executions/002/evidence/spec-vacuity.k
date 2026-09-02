requires "../candidate/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result obligation.  The executed program is unchanged, but
  // the claim says it always returns empty.  Witness: INPUT ==String "b".
  claim
    <mpy>
      <k>
        Module(
          FuncDef("remove_vowels", Params("text"),
            Return(
              Call(
                Attribute(
                  Call(
                    Attribute(
                      Call(
                        Attribute(
                          Call(
                            Attribute(
                              Call(
                                Attribute(
                                  Call(
                                    Attribute(
                                      Call(
                                        Attribute(
                                          Call(
                                            Attribute(
                                              Call(
                                                Attribute(
                                                  Call(
                                                    Attribute(
                                                      Name("text"),
                                                    "replace"),
                                                  Str("a"), Str("")),
                                                "replace"),
                                              Str("e"), Str("")),
                                            "replace"),
                                          Str("i"), Str("")),
                                        "replace"),
                                      Str("o"), Str("")),
                                    "replace"),
                                  Str("u"), Str("")),
                                "replace"),
                              Str("A"), Str("")),
                            "replace"),
                          Str("E"), Str("")),
                        "replace"),
                      Str("I"), Str("")),
                    "replace"),
                  Str("O"), Str("")),
                "replace"),
              Str("U"), Str("")))))
        => done
      </k>
      <input> INPUT:String </input>
      <result> noResult => result("") </result>
    </mpy>
endmodule
