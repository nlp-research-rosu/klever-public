requires "reference-semantics/semantics.k"

module CONNECTION-VERIFICATION
  imports MPY

  syntax Bool ::= connectionNondecreasing(ValSeq) [function, total]
  rule connectionNondecreasing(.ValSeq) => true
  rule connectionNondecreasing(vCons(_:Val, .ValSeq)) => true
  rule connectionNondecreasing(vCons(A:Val, vCons(B:Val, REST:ValSeq)))
    => applyCmp("<=", A, B)
       andBool connectionNondecreasing(vCons(B, REST))
endmodule
