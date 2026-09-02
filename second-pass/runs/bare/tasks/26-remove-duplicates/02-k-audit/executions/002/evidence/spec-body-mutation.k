requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The executed program body now keeps values with count == 2, while the
  // expected result remains the original count == 1 result for input [7].
  claim
    <k>
      Module(
        ImportFrom("typing", "List")
        FuncDef("remove_duplicates",
          Params("numbers"),
          CellVars("numbers"),
          FreeVars(.Strings),
          Return(
            ListComp(Name("number"),
              CompFor(
                Name("number"),
                Name("numbers"),
                Compare(
                  Call(Attribute(Name("numbers"), "count"), Name("number")),
                  CmpOp("==", Int(2))))))))
      => .K
    </k>
    <input> listValue(7) </input>
    <function> noFunction =>
      closure("numbers",
        Return(
          ListComp(Name("number"),
            CompFor(
              Name("number"),
              Name("numbers"),
              Compare(
                Call(Attribute(Name("numbers"), "count"), Name("number")),
                CmpOp("==", Int(2)))))))
    </function>
    <env> emptyEnv => bind("numbers", listValue(7), emptyEnv) </env>
    <output> listValue(.Ints) => listValue(7) </output>
endmodule
