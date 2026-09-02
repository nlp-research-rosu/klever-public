requires "solution-program.k"

module VERIFICATION
  imports SOLUTION-PROGRAM

  // Independent executable statement of the required ordering: the result
  // has one block per numeral, arranged from zero through nine.  On valid
  // inputs no numeral word is a substring of another numeral word, so K's
  // non-overlapping occurrence count equals that token's multiplicity.
  syntax String ::= sortSpec(String) [function]
  rule sortSpec(S) => trimTrailingSpace(
       repeatString("zero ",  countAllOccurrences(S, "zero"))
    +String repeatString("one ",   countAllOccurrences(S, "one"))
    +String repeatString("two ",   countAllOccurrences(S, "two"))
    +String repeatString("three ", countAllOccurrences(S, "three"))
    +String repeatString("four ",  countAllOccurrences(S, "four"))
    +String repeatString("five ",  countAllOccurrences(S, "five"))
    +String repeatString("six ",   countAllOccurrences(S, "six"))
    +String repeatString("seven ", countAllOccurrences(S, "seven"))
    +String repeatString("eight ", countAllOccurrences(S, "eight"))
    +String repeatString("nine ",  countAllOccurrences(S, "nine"))
  )

  syntax Bool ::= isNumeral(String) [function, total]
  rule isNumeral("zero")  => true
  rule isNumeral("one")   => true
  rule isNumeral("two")   => true
  rule isNumeral("three") => true
  rule isNumeral("four")  => true
  rule isNumeral("five")  => true
  rule isNumeral("six")   => true
  rule isNumeral("seven") => true
  rule isNumeral("eight") => true
  rule isNumeral("nine")  => true
  rule isNumeral(_)        => false [owise]

  // Recognizes exactly the contract's canonical space-delimited inputs,
  // plus the empty input (which the reference tests conventionally admit).
  syntax Bool ::= validNumerals(String) [function]
  rule validNumerals("") => true
  rule validNumerals(S) => isNumeral(S)
    requires S =/=String ""
     andBool findString(S, " ", 0) ==Int -1
  rule validNumerals(S) =>
       isNumeral(substrString(S, 0, findString(S, " ", 0)))
    andBool validNumerals(substrString(
              S,
              findString(S, " ", 0) +Int 1,
              lengthString(S)))
    requires findString(S, " ", 0) >=Int 0
     andBool findString(S, " ", 0) <Int lengthString(S) -Int 1
  rule validNumerals(S) => false
    requires findString(S, " ", 0) ==Int lengthString(S) -Int 1
endmodule
