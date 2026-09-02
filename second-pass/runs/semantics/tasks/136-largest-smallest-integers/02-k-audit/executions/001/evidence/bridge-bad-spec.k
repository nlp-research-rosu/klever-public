requires "bridge-base.k"

module BRIDGE-BAD-SPEC
  imports BRIDGE-BASE

  // Deliberately wrong yielded value, with an observable trailing continuation.
  // The fixed list semantics must retain -7, not fabricate -6.
  claim [wrong-yield-with-suffix]:
    <k> #iterNext(list(vCons(-7, .ValSeq))) ~> Int(999)
      => #iterYield(-6, list(.ValSeq)) ~> Int(999) ... </k>
endmodule
