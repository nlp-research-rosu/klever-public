requires "reference-semantics/semantics.k"

module AUDIT-BRIDGE-FREE-VERIFICATION
  imports MPY

  syntax Bool ::= auditAllInts(ValSeq) [function, total]
  rule auditAllInts(.ValSeq) => true
  rule auditAllInts(vCons(_I:Int, VS:ValSeq)) => auditAllInts(VS)
  rule auditAllInts(vCons(_V:Val, _VS:ValSeq)) => false [owise]

  syntax Int ::= auditMagnitudeAcc(ValSeq, Int) [function]
  rule auditMagnitudeAcc(.ValSeq, A:Int) => A
  rule auditMagnitudeAcc(vCons(I:Int, VS:ValSeq), A:Int)
    => auditMagnitudeAcc(VS, A -Int I)
    requires I <Int 0
  rule auditMagnitudeAcc(vCons(I:Int, VS:ValSeq), A:Int)
    => auditMagnitudeAcc(VS, A +Int I)
    requires I >=Int 0

  syntax Int ::= auditSignAcc(ValSeq, Int) [function]
  rule auditSignAcc(.ValSeq, S:Int) => S
  rule auditSignAcc(vCons(I:Int, VS:ValSeq), S:Int)
    => auditSignAcc(VS, 0 -Int S)
    requires I <Int 0
  rule auditSignAcc(vCons(0, VS:ValSeq), _S:Int)
    => auditSignAcc(VS, 0)
  rule auditSignAcc(vCons(I:Int, VS:ValSeq), S:Int)
    => auditSignAcc(VS, S)
    requires I >Int 0

  syntax Int ::= auditLastInt(ValSeq) [function]
  rule auditLastInt(vCons(I:Int, .ValSeq)) => I
  rule auditLastInt(vCons(_I:Int, vCons(J:Int, VS:ValSeq)))
    => auditLastInt(vCons(J, VS))
endmodule
