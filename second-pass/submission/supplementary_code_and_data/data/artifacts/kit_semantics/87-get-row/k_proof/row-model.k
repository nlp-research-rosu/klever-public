requires "reference-semantics/semantics.k"

module ROW-MODEL-SYNTAX
  imports MPY-CORE

  syntax ValSeq ::= rowContents(Val) [function, total]
  syntax Bool ::= listRows(ValSeq) [function, total]
endmodule

module ROW-MODEL
  imports MPY
  imports ROW-MODEL-SYNTAX

  rule rowContents(list(VS:ValSeq)) => VS
  rule rowContents(_:Val) => .ValSeq [owise]

  rule listRows(.ValSeq) => true
  rule listRows(vCons(V:Val, VS:ValSeq))
    => (V ==K list(rowContents(V))) andBool listRows(VS)
endmodule
