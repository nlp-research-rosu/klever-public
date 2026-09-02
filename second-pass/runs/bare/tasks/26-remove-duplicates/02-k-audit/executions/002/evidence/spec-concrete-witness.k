requires "verification.k"

module SPEC-CONCRETE-WITNESS
  imports VERIFICATION

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
                  CmpOp("==", Int(1))))))))
      => .K
    </k>
    <input> listValue(1, 2, 3, 2, 4) </input>
    <function> noFunction =>
      closure("numbers",
        Return(
          ListComp(Name("number"),
            CompFor(
              Name("number"),
              Name("numbers"),
              Compare(
                Call(Attribute(Name("numbers"), "count"), Name("number")),
                CmpOp("==", Int(1)))))))
    </function>
    <env> emptyEnv =>
      bind("numbers", listValue(1, 2, 3, 2, 4), emptyEnv)
    </env>
    <output> listValue(.Ints) => listValue(1, 3, 4) </output>
endmodule
