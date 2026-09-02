requires "semantic.k"

module VERIFICATION
  imports MPY

  // The mathematical postcondition from the HumanEval prompt.
  syntax PyVal ::= expectedSumProduct(Ints) [function, total]

  rule expectedSumProduct(IS)
       => PyTuple(PyInt(sumInts(IS)), PyInt(productInts(IS)))
endmodule
