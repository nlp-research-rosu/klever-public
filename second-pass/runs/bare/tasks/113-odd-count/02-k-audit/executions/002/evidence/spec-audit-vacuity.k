requires "verification.k"

// Reviewer-authored A5 mutation.  The real program produces message(4) for
// "1234567"; this deliberately strengthens the result to the false message(5).
module AUDIT-VACUITY
  imports ODD-COUNT-VERIFICATION

  claim [wrong-prompt-one-count]:
    <k> solutionProgram => .K </k>
    <input> pyList(value(
        pyString(inputDigits(
          digit(oddDigit,
          digit(evenDigit,
          digit(oddDigit,
          digit(evenDigit,
          digit(oddDigit,
          digit(evenDigit,
          digit(oddDigit, noDigits))))))))),
        noValues)) </input>
    <output>
      noValue
      => pyList(value(pyString(message(5)), noValues))
    </output>
endmodule
