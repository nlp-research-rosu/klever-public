requires "reference-semantics/semantics.k"

module CONNECTION-VERIFICATION
  imports MPY

  // A cast view only; unlike the candidate extension, this module does not add
  // any rule for applyCmp.
  syntax Int ::= auditIntValue(Val) [function, total]
  rule auditIntValue(I:Int) => I
endmodule
