requires "/tmp/audit-work/154-cycpattern-check/candidate/reference-semantics/semantics.k"

module SLICE-CONNECTION
  imports MPY

  // Independent mathematical characterization used only in this connection proof.
  syntax IntSeq ::= dropOneConnection(IntSeq) [function, total]
  rule dropOneConnection(.IntSeq) => .IntSeq
  rule dropOneConnection(iCons(_:Int, R:IntSeq)) => R
endmodule
