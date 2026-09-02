requires "audit-pinning-definition.k"

module AUDIT-PINNING-CLAIMS
  imports AUDIT-PINNING-DEFINITION

  claim [loop-alias-is-submitted-body]:
    <k> loopAliasMatchesSubmitted => true </k>

  claim [function-alias-is-submitted-body]:
    <k> functionAliasMatchesSubmitted => true </k>
endmodule
