requires "bridge-audit.k"

module BRIDGE-CONNECTION-SPEC
  imports BRIDGE-AUDIT

  claim
    <k>
      strContains(iCons(C:Int, .IntSeq), auditVowelCodes)
      =>
      auditIsVowelCode(C)
      ...
    </k>
endmodule
