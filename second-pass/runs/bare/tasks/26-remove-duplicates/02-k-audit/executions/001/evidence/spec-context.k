requires "verification.k"

module SPEC-CONTEXT
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
    [label(context-walk-correct)]

  // The immediate continuation prepends 99 after walkComp has emitted 1.
  // A bridge that discards or unwinds KREST would produce a different output.
  claim
    <k>
      walkComp((1, .Ints),
               "number",
               Name("number"),
               Compare(
                 Call(Attribute(Name("numbers"), "count"), Name("number")),
                 CmpOp("==", Int(1))),
               bind("numbers", listValue(1, .Ints), emptyEnv))
      ~> emitComputed(true, 99)
      => .K
    </k>
    <output>
      listValue(.Ints)
      => listValue(99, 1, .Ints)
    </output>
    [label(context-continuation)]
endmodule
