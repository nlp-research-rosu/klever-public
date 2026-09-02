requires "bridge-audit.k"

module BRIDGE-CONNECTION-CASES-SPEC
  imports BRIDGE-AUDIT

  claim [vowel-case]:
    <k>
      strContains(iCons(C:Int, .IntSeq), auditVowelCodes)
      =>
      true
      ...
    </k>
    requires auditIsVowelCode(C)

  claim [nonvowel-case]:
    <k>
      strContains(iCons(C:Int, .IntSeq), auditVowelCodes)
      =>
      false
      ...
    </k>
    requires notBool auditIsVowelCode(C)
endmodule
