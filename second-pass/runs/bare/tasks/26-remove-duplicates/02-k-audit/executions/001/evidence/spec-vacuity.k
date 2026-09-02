requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Same independently proved iterator lemma, renamed for this isolated spec.
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
    [label(vacuity-walk-correct)]

  // Deliberately false: it requires an additional leading 0 in every result.
  // INPUT = .Ints is a satisfying witness; the real/K result is .Ints, not 0.
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
      listValue(.Ints)
      => listValue(0, removeRepeated(INPUT, INPUT))
    </output>
    [label(program-false-extra-zero)]
endmodule
