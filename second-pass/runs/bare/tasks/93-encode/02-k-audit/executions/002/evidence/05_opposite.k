requires "verification.k"

module OPPOSITE
  imports VERIFICATION

  // A legal interpretation of the otherwise equation-free abstract functions.
  // It deliberately makes encodedChar disagree with fixed body execution.
  rule encodedChar(_C) => "!"
  rule advancedVowel(C) => C
  rule swapCaseChar(C) => C
endmodule
