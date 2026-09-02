requires "semantic.k"

module VERIFICATION
  imports MPY

  // Executable form of the HumanEval postcondition.
  syntax Bool ::= "strlenPost" "(" Value "," Value ")" [function, total]
  rule strlenPost(Str(S), Int(N)) => N ==Int lengthString(S)
endmodule
