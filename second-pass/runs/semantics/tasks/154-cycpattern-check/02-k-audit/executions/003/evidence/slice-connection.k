requires "reference-semantics/semantics.k"

module SLICE-AUDIT
  imports MPY

  syntax IntSeq ::= auditDropOne(IntSeq) [function, total]
  rule auditDropOne(.IntSeq) => .IntSeq
  rule auditDropOne(iCons(_:Int, R:IntSeq)) => R
endmodule

module SLICE-AUDIT-SPEC
  imports SLICE-AUDIT

  // Bridge-free connection theorem for verification.k's s[1:] acceleration.
  claim [slice-one-to-end]:
    <k>
      Subscript(
        str(S:IntSeq),
        Slice(Int(1), NoBound, NoBound))
      ~> CONT
    =>
      str(auditDropOne(S))
      ~> CONT
    </k>
endmodule

module SLICE-AUDIT-GROUND-SPEC
  imports SLICE-AUDIT

  claim [slice-empty]:
    <k>
      Subscript(str(.IntSeq), Slice(Int(1), NoBound, NoBound))
    =>
      str(.IntSeq)
    </k>

  claim [slice-singleton]:
    <k>
      Subscript(
        str(iCons(65, .IntSeq)),
        Slice(Int(1), NoBound, NoBound))
    =>
      str(.IntSeq)
    </k>

  claim [slice-two]:
    <k>
      Subscript(
        str(iCons(65, iCons(66, .IntSeq))),
        Slice(Int(1), NoBound, NoBound))
    =>
      str(iCons(66, .IntSeq))
    </k>
endmodule
