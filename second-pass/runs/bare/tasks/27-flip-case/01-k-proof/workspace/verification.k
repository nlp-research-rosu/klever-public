requires "semantic.k"

module VERIFICATION
  imports MPY

  // The contract-level operation.  Keeping this wrapper separate from the AST
  // semantics makes the postcondition state the intended string operation.
  syntax String ::= flipSpec(String) [function]
  rule flipSpec(S) => pySwapCase(S)
endmodule
