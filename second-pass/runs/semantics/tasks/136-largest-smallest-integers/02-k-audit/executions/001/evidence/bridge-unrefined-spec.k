requires "bridge-base.k"

module BRIDGE-UNREFINED-SPEC
  imports BRIDGE-BASE

  // This extensionally equivalent Val-plus-isInt formulation exposes a
  // backend limitation: kprove does not reverse the generated sort predicate
  // into a symbolic subsort injection, leaving V = intValue(V) residual.
  claim [iter-int-unrefined]:
    <k> #iterNext(list(vCons(V:Val, REST:ValSeq)))
      => #iterYield(intValue(V), list(REST)) ... </k>
    requires isInt(V)
endmodule
