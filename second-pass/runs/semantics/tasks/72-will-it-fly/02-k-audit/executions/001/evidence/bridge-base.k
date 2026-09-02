requires "reference-semantics/semantics.k"

// Proof-side mathematical functions, intentionally excluding both candidate
// operational shortcut rules. This definition is used only to test whether
// the fixed supplied semantics connects to the proposed summaries.
module BRIDGE-BASE
  imports MPY

  syntax Bool ::= auditAllInts(ValSeq) [function, total]
  rule auditAllInts(.ValSeq) => true
  rule auditAllInts(vCons(_:Int, REST:ValSeq)) => auditAllInts(REST)
  rule auditAllInts(vCons(V:Val, _:ValSeq)) => false
    requires notBool isInt(V)

  syntax Int ::= auditSumIntVS(ValSeq) [function, total]
  rule auditSumIntVS(.ValSeq) => 0
  rule auditSumIntVS(vCons(I:Int, REST:ValSeq))
    => I +Int auditSumIntVS(REST)

  syntax ValSeq ::= auditSnocVS(ValSeq, Val) [function, total]
  rule auditSnocVS(.ValSeq, V:Val) => vCons(V, .ValSeq)
  rule auditSnocVS(vCons(H:Val, T:ValSeq), V:Val)
    => vCons(H, auditSnocVS(T, V))

  syntax ValSeq ::= auditReverseVS(ValSeq) [function, total]
  rule auditReverseVS(.ValSeq) => .ValSeq
  rule auditReverseVS(vCons(H:Val, T:ValSeq))
    => auditSnocVS(auditReverseVS(T), H)
endmodule
