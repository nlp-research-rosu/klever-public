requires "verification.k"

module ODD-COUNT-SPEC
  imports ODD-COUNT-VERIFICATION

  // The empty list is the outer-loop base case.
  claim [empty-list]:
    <k> solutionProgram => .K </k>
    <input> pyList(noValues) </input>
    <output> noValue => pyList(expected(noValues)) </output>

  // Exact examples from prompt.py (digits are represented by their parity).
  claim [prompt-example-one]:
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

  claim [prompt-example-two]:
    <k> solutionProgram => .K </k>
    <input> pyList(
        value(pyString(inputDigits(digit(oddDigit, noDigits))),
        value(pyString(inputDigits(
          digit(oddDigit,
          digit(oddDigit,
          digit(oddDigit,
          digit(oddDigit,
          digit(oddDigit,
          digit(oddDigit,
          digit(oddDigit,
          digit(oddDigit, noDigits)))))))))),
        noValues))) </input>
    <output> noValue => pyList(expected(
         value(pyString(inputDigits(digit(oddDigit, noDigits))),
         value(pyString(inputDigits(
           digit(oddDigit,
           digit(oddDigit,
           digit(oddDigit,
           digit(oddDigit,
           digit(oddDigit,
           digit(oddDigit,
           digit(oddDigit,
           digit(oddDigit, noDigits)))))))))),
         noValues)))) </output>

  // For every integer N, the source expression constructs exactly the
  // contract's sentence with N substituted at all four occurrences of "i".
  claim [format-all-counts]:
    <k> evaluate(
      BinOp(
        "+",
        BinOp(
          "+",
          BinOp(
            "+",
            BinOp(
              "+",
              BinOp(
                "+",
                BinOp(
                  "+",
                  BinOp(
                    "+",
                    BinOp(
                      "+",
                      Str("the number of odd elements "),
                      Call(Name("str"), Name("count"))),
                    Str("n the str")),
                  Call(Name("str"), Name("count"))),
                Str("ng ")),
              Call(Name("str"), Name("count"))),
            Str(" of the ")),
          Call(Name("str"), Name("count"))),
        Str("nput.")),
      store("count", pyInt(N), emptyEnv))
        => pyString(message(N)) </k>

  // These claims are the two universal character-step cases.  Together with
  // digitValues(noDigits) => noValues, they exhaust valid digit strings.
  claim [character-loop-base]:
    <k> executeFor(noValues, "c", innerBody, REST, ENV)
        => execute(REST, ENV) </k>

  claim [even-character-step]:
    <k> executeFor(
      digitValues(digit(evenDigit, DS)), "c", innerBody, REST,
      ENV)
        => executeFor(
         digitValues(DS), "c", innerBody, REST,
         store("c", pyString(oneDigit(evenDigit)), ENV)) </k>

  claim [odd-character-step]:
    <k> executeFor(
      digitValues(digit(oddDigit, DS)), "c", innerBody, REST,
      ENV)
        => executeFor(
         digitValues(DS), "c", innerBody, REST,
         store(
           "count",
           addValue(
             evaluate(Name("count"),
               store("c", pyString(oneDigit(oddDigit)), ENV)),
             pyInt(1)),
           store("c", pyString(oneDigit(oddDigit)), ENV))) </k>

  // The list-loop base and the two append equations complete the structural
  // cases used by the outer loop, for arbitrary values and continuations.
  claim [list-loop-base]:
    <k> executeFor(noValues, "s", outerBody, REST, ENV)
        => execute(REST, ENV) </k>

  claim [append-base]:
    <k> appendValues(noValues, VS) => VS </k>

  claim [append-step]:
    <k> appendValues(value(V, VS), WS)
        => value(V, appendValues(VS, WS)) </k>
endmodule
