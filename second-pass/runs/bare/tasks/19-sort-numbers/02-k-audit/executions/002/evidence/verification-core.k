requires "solution-program.k"

module VERIFICATION-CORE
  imports SOLUTION-PROGRAM

  syntax String ::= coreSortSpec(String) [function]
  rule coreSortSpec(S) => trimTrailingSpace(
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
endmodule

