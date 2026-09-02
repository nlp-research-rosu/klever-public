module VERIFICATION
  imports INT
  imports BOOL
  imports STRING

  // The mathematical reference checker carries the current unmatched-open
  // count.  It returns false on the first negative prefix and otherwise tests
  // for a zero count at end of input.
  syntax Bool ::= bracketSpec(String, Int) [function, total]
                | bracketEmpty(Bool, String, Int) [function, total]
                | bracketOpen(Bool, String, Int) [function, total]
                | bracketNegative(Bool, String, Int) [function, total]

  rule bracketSpec(S, D) => bracketEmpty(S ==String "", S, D)
  rule bracketEmpty(true, _, D) => D ==Int 0
  rule bracketEmpty(false, S, D)
    => bracketOpen(substrString(S, 0, 1) ==String "<", S, D)
  rule bracketOpen(true, S, D)
    => bracketSpec(substrString(S, 1, lengthString(S)), D +Int 1)
  rule bracketOpen(false, S, D)
    => bracketNegative(D -Int 1 <Int 0, S, D)
  rule bracketNegative(true, _, _) => false
  rule bracketNegative(false, S, D)
    => bracketSpec(substrString(S, 1, lengthString(S)), D -Int 1)

  // Constructor model of exactly the input language promised by the task.
  // It has no constructor for any character other than '<' and '>'.
  syntax BracketSeq ::= noBrackets() | openBracket(BracketSeq) | closeBracket(BracketSeq)
  syntax Bool ::= bracketSeqSpec(BracketSeq, Int) [function, total]

  rule bracketSeqSpec(noBrackets(), D) => D ==Int 0
  rule bracketSeqSpec(openBracket(BS), D) => bracketSeqSpec(BS, D +Int 1)
  rule bracketSeqSpec(closeBracket(_), D) => false
    requires D -Int 1 <Int 0
  rule bracketSeqSpec(closeBracket(BS), D) => bracketSeqSpec(BS, D -Int 1)
    requires D -Int 1 >=Int 0
endmodule
