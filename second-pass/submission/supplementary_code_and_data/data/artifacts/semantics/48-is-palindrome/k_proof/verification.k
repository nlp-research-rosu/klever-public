requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // Mathematical contract: a code-point sequence is a palindrome exactly
  // when it is structurally equal to the negative-step slice that reverses it.
  syntax Bool ::= palindrome(IntSeq) [function]
  rule palindrome(IS:IntSeq)
    => IS ==K buildIS(IS, isLen(IS) -Int 1, -1, -1)
endmodule
