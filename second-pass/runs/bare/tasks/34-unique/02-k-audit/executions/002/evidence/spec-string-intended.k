requires "verification.k"

module SPEC-STRING-INTENDED
  imports VERIFICATION

  // Python's required result for ["b","a","b"] is ["a","b"].
  claim <k> apply(
          Module(FuncDef("unique", Params("l"),
            Return(Call(Name("sorted"), Call(Name("set"), Name("l")))))),
          VList(ListItem("b") ListItem("a") ListItem("b")))
    => VList(ListItem("a") ListItem("b")) </k>
endmodule
