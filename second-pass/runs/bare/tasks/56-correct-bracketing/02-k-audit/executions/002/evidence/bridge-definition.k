requires "semantic.k"

module BRIDGE-DEFINITION
  imports MPY

  // Reviewer-authored, truthful renderer from the candidate's symbolic
  // BracketSeq representation to the real K String representation.
  syntax String ::= bracketSeqString(BracketSeq) [function, total]
  rule bracketSeqString(noBrackets()) => ""
  rule bracketSeqString(openBracket(BS))
    => "<" +String bracketSeqString(BS)
  rule bracketSeqString(closeBracket(BS))
    => ">" +String bracketSeqString(BS)
endmodule
