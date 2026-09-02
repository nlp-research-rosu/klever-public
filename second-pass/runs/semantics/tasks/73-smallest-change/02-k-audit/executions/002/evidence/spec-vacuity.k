requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false result mutation on a fully ground satisfying state.
  // targetValid(mainCall, .ValSeq, 0, 0) is true and targetAnswer is 0,
  // so the mutated RHS deliberately demands the false result 1.
  claim [false-off-by-one-result]:
    <k> #targetCall(mainCall, ref(0), 0, 0) => 1 </k>
    <heap> 0 |-> list(.ValSeq) </heap>
endmodule
