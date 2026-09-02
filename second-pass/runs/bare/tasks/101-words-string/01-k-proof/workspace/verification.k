module VERIFICATION
  imports STRING
  imports LIST
  imports INT
  imports BOOL

  // splitSpaces is a mathematical model of splitting on runs of spaces.
  // The prompt's input alphabet uses commas and spaces as its separators.
  syntax List ::= splitSpaces(String) [function]

  rule splitSpaces("") => .List
  rule splitSpaces(S) => splitSpaces(substrString(S, 1, lengthString(S)))
    requires lengthString(S) >Int 0
     andBool substrString(S, 0, 1) ==String " "
  rule splitSpaces(S) => ListItem(S)
    requires lengthString(S) >Int 0
     andBool findString(S, " ", 0) ==Int -1
  rule splitSpaces(S)
    => ListItem(substrString(S, 0, findString(S, " ", 0)))
       splitSpaces(substrString(S, findString(S, " ", 0) +Int 1,
                                  lengthString(S)))
    requires findString(S, " ", 0) >Int 0

  // Formal statement of the HumanEval contract: commas and spaces delimit
  // words, consecutive/edge separators contribute no empty strings.
  syntax List ::= wordsContract(String) [function, total]
  rule wordsContract(S) => splitSpaces(replaceAll(S, ",", " "))
endmodule
