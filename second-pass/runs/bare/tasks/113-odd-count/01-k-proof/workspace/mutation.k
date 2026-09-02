requires "verification.k"

// Negative validation: the empty input must not produce a spurious item.
module ODD-COUNT-MUTATION
  imports ODD-COUNT-VERIFICATION

  claim [wrong-empty-result]:
    <k> solutionProgram => .K </k>
    <input> pyList(noValues) </input>
    <output>
      noValue
      => pyList(value(pyString(literal("incorrect")), noValues))
    </output>
endmodule
