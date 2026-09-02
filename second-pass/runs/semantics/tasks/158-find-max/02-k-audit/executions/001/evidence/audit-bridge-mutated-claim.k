requires "audit-bridge-mutated.k"

module AUDIT-BRIDGE-MUTATED-CLAIM
  imports AUDIT-BRIDGE-MUTATED

  claim [mutated-word-map-must-not-connect]:
    <k> #iterNext(list(auditMutWordVals(
          amwCons(iCons(97, .IntSeq), .AuditMutWordSeq))))
         ~> Int(7)
      => #iterYield(
           str(iCons(97, .IntSeq)),
           list(auditMutWordVals(.AuditMutWordSeq)))
         ~> Int(7)
    </k>
endmodule
