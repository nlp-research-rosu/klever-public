requires "verification.k"

module SPEC-COUNT-OPPOSITE
  imports VERIFICATION

  // False opposite interpretation: count(7, [7]) is not treated as one.
  claim
    <k>
      walkComp((7, .Ints),
               "number",
               Name("number"),
               Compare(
                 Call(Attribute(Name("numbers"), "count"), Name("number")),
                 CmpOp("==", Int(1))),
               bind("numbers", listValue(7, .Ints), emptyEnv))
      => .K
    </k>
    <output> listValue(.Ints) => listValue(.Ints) </output>
    [label(singleton-wrongly-dropped)]

  // False opposite interpretation: count(7, [7, 7]) is treated as one.
  claim
    <k>
      walkComp((7, 7, .Ints),
               "number",
               Name("number"),
               Compare(
                 Call(Attribute(Name("numbers"), "count"), Name("number")),
                 CmpOp("==", Int(1))),
               bind("numbers", listValue(7, 7, .Ints), emptyEnv))
      => .K
    </k>
    <output>
      listValue(.Ints)
      => listValue(7, 7, .Ints)
    </output>
    [label(duplicate-wrongly-kept)]
endmodule
