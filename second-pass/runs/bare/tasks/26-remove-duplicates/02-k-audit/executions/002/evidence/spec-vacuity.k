requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

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

  // Deliberately false result mutation. For the satisfying input INPUT=.Ints,
  // actual output is empty while this postcondition demands a leading zero.
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
    <output>
      listValue(.Ints) => listValue(0, removeRepeated(INPUT, INPUT))
    </output>
    [label(program-false-result)]
endmodule
