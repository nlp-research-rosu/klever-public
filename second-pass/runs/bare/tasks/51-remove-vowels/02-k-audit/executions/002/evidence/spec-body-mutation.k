requires "../candidate/verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The actually executed body is mutated: the last replace deletes "X"
  // instead of "U".  The result obligation remains the original contract.
  // Satisfying false witness: INPUT ==String "X".
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
              Str("X"), Str("")))))
        => done
      </k>
      <input> INPUT:String </input>
      <result> noResult => result(removeVowelsSpec(INPUT)) </result>
    </mpy>
endmodule
