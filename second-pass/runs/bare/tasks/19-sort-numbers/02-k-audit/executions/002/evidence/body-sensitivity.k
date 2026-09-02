requires "verification.k"

module BODY-SENSITIVITY
  imports VERIFICATION

  // Material body mutation: the zero block prints "WRONG " while still
  // counting occurrences of "zero". The program term below is executed.
  claim [mutated-body]:
    <k>
      Module(
        FuncDef(
          "sort_numbers",
          Params("numbers"),
          Return(
            Call(
              Attribute(
                BinOp("+",
                  BinOp("+",
                    BinOp("+",
                      BinOp("+",
                        BinOp("+",
                          BinOp("+",
                            BinOp("+",
                              BinOp("+",
                                BinOp("+",
                                  block("zero", "WRONG "),
                                  block("one", "one ")),
                                block("two", "two ")),
                              block("three", "three ")),
                            block("four", "four ")),
                          block("five", "five ")),
                        block("six", "six ")),
                      block("seven", "seven ")),
                    block("eight", "eight ")),
                  block("nine", "nine ")),
                "strip"),
              .Exprs))))
      ~> invoke("zero")
      => VStr("zero")
    </k>
endmodule
