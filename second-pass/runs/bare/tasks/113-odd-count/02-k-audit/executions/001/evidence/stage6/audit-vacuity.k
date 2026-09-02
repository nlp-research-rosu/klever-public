requires "verification.k"

module AUDIT-VACUITY
  imports ODD-COUNT-VERIFICATION

  // Fresh false mutation: "1234567" has four odd digits, not five.
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
