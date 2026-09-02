requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // Mathematical postcondition used by the reachability claim.
  syntax Bool ::= isPalindrome(String) [function]
  rule isPalindrome(S) => S ==String reverseString(S)
endmodule
