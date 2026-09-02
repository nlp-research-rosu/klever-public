requires "verification-no-bridge.k"

module LOOP-ONLY-NO-BRIDGE
  imports VERIFICATION-NO-BRIDGE

  claim [loop-invariant-without-operational-bridge]:
    <k>
      #loop(list(intVals(INPUT:IntSeq)), Name("value"), addLoopBody)
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
        ("total" |-> addAccSpec(INPUT, ODD, ACC))
        ?FINALBINDINGS:Map,
        PARENT))
      RESTSCOPES
    </scopes>
    requires notBool (L in_keys(RESTSCOPES))
endmodule
