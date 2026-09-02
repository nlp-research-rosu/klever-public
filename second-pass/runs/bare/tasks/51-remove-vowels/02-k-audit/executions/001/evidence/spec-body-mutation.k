requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

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
              Str("O"), Str("")))))
        => done
      </k>
      <input> "U" </input>
      <result> noResult => result(removeVowelsSpec("U")) </result>
    </mpy>
endmodule
