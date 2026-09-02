requires "verification.k"

module SPEC-PREDICATE-PROBES
  imports VERIFICATION

  claim <k> .K => .K </k>
    ensures outputOK(vCons(1, .ValSeq), 1, 1, 1, 0)
    [label(predicate-valid)]

  claim <k> .K => .K </k>
    ensures outputOK(vCons(2, .ValSeq), 1, 1, 1, 0)
    [label(predicate-wrong-int)]

  claim <k> .K => .K </k>
    ensures outputOK(vCons(noneV, .ValSeq), 1, 1, 1, 0)
    [label(predicate-wrong-type)]
endmodule
