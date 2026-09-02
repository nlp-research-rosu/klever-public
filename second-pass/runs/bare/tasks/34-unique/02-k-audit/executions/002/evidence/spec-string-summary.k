requires "verification.k"

module SPEC-STRING-SUMMARY
  imports VERIFICATION

  // The original post shape may be reached even though uniqueSpec cannot
  // reduce to a value for these valid Python string elements.
  claim <k> apply(
          Module(FuncDef("unique", Params("l"),
            Return(Call(Name("sorted"), Call(Name("set"), Name("l")))))),
          VList(ListItem("b") ListItem("a") ListItem("b")))
    => VList(uniqueSpec(ListItem("b") ListItem("a") ListItem("b"))) </k>
endmodule
