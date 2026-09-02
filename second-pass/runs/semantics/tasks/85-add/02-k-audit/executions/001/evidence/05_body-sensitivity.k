requires "verification-body-mutant.k"

module BODY-SENSITIVITY
  imports VERIFICATION-BODY-MUTANT

  // Deliberately false after the body mutation: the operational body adds odd
  // values, while addAccSpecMut continues to summarize even values.
  claim [mutated-body-must-not-prove-original-summary]:
    <k>
      #loop(list(intValsMut(INPUT:IntSeq)), Name("value"), mutatedLoopBody)
      =>
      .K
    </k>
    <env> L:Int </env>
    <scopes>
      (L |-> scope(
        ("lst" |-> LST:Val)
        ("total" |-> ACC)
        ("odd_index" |-> ODD)
        ("value" |-> OLDVALUE:Int),
        PARENT:Parent))
      RESTSCOPES:Map
      =>
      (L |-> scope(
        ("total" |-> addAccSpecMut(INPUT, ODD, ACC))
        ?FINALBINDINGS:Map,
        PARENT))
      RESTSCOPES
    </scopes>
    requires notBool (L in_keys(RESTSCOPES))
endmodule
