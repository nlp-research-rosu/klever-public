requires "verification.k"

module DOMAIN-EXCLUSION-SPEC
  imports VERIFICATION

  claim
    <k> ints(vCons(str(S:IntSeq), REST:ValSeq)) => false </k>
    [label(strings-excluded)]

  claim
    <k> ints(vCons(F:Float, REST:ValSeq)) => false </k>
    [label(floats-excluded)]
endmodule
