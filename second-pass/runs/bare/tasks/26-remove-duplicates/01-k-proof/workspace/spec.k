requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive bridge between the transition-level comprehension iterator and
  // the separately stated stable-filter contract.
  claim
    <k>
      walkComp(INPUT,
               "number",
               Name("number"),
               Compare(
                 Call(Attribute(Name("numbers"), "count"), Name("number")),
                 CmpOp("==", Int(1))),
               bind("numbers", listValue(ORIGINAL), emptyEnv))
      ~> KREST
      => KREST
    </k>
    <output>
      listValue(SUFFIX)
      => listValue(removeRepeatedOnto(INPUT, ORIGINAL, SUFFIX))
    </output>
    [label(walk-correct)]

  // End-to-end theorem for the exact AST in solution.mpy and an arbitrary
  // integer list INPUT.  This begins in the generated initial configuration.
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
    <input> listValue(INPUT) </input>
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
    <env> emptyEnv => bind("numbers", listValue(INPUT), emptyEnv) </env>
    <output> listValue(.Ints) => listValue(removeRepeated(INPUT, INPUT)) </output>
    [label(program-correct)]
endmodule
