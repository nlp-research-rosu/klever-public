requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false mutation: append "!" to the required result for every input.
  // The original precondition is unchanged; input "aB" is a satisfying
  // witness whose real result is "B", not "B!".
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
      <result>
        noResult => result(removeVowelsSpec(INPUT) +String "!")
      </result>
    </mpy>
endmodule
