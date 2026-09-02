requires "verification.k"

// Reviewer-authored operational sensitivity check.  This claim executes a
// materially different body (returning [] immediately) while retaining the
// real prompt-example input and the original result obligation.
module AUDIT-BODY-SENSITIVITY
  imports ODD-COUNT-VERIFICATION

  claim [changed-body-must-not-prove]:
    <k>
      Module(FuncDef("odd_count", Params("lst"),
        Assign(Name("result"), ListExpr())
        Return(Name("result"))))
      => .K
    </k>
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
    <output> noValue => pyList(expected(value(
         pyString(inputDigits(
           digit(oddDigit,
           digit(evenDigit,
           digit(oddDigit,
           digit(evenDigit,
           digit(oddDigit,
           digit(evenDigit,
           digit(oddDigit, noDigits))))))))),
         noValues))) </output>
endmodule
