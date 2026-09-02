// The contract is stated independently of the AST evaluator.  It says:
// split into words, retain exactly those whose mathematical consonant count
// equals N, and retain their order.

requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  syntax PyValue ::= selectWordsSpec(String, Int) [function]

  rule selectWordsSpec(S, N)
       => pyList(filterWords(words(S), N))
endmodule
