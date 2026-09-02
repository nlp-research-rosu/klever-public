requires "bridge-audit.k"

module BRIDGE-CONNECTION-EXHAUSTIVE-SPEC
  imports BRIDGE-AUDIT

  claim <k> strContains(iCons(65,  .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(69,  .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(73,  .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(79,  .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(85,  .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(97,  .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(101, .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(105, .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(111, .IntSeq), auditVowelCodes) => true ... </k>
  claim <k> strContains(iCons(117, .IntSeq), auditVowelCodes) => true ... </k>

  claim
    <k>
      strContains(iCons(C:Int, .IntSeq), auditVowelCodes)
      =>
      false
      ...
    </k>
    requires C =/=Int 65  andBool C =/=Int 69  andBool C =/=Int 73
     andBool C =/=Int 79  andBool C =/=Int 85  andBool C =/=Int 97
     andBool C =/=Int 101 andBool C =/=Int 105 andBool C =/=Int 111
     andBool C =/=Int 117
endmodule
