requires "verification.k"

module SPEC-CONTEXT-WITNESS
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

  // Satisfiable boundary/context witness: the immediate continuation performs
  // another observable output update after the summarized iterator.
  claim
    <k>
      walkComp((1, .Ints),
               "number",
               Name("number"),
               Compare(
                 Call(Attribute(Name("numbers"), "count"), Name("number")),
                 CmpOp("==", Int(1))),
               bind("numbers", listValue(1), emptyEnv))
      ~> emitComputed(true, 9)
      => .K
    </k>
    <output> listValue(8) => listValue(9, 1, 8) </output>
    [label(context-witness)]
endmodule
