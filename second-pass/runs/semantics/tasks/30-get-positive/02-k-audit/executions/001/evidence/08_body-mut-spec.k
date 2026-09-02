requires "verification-body-mut.k"

module BODY-MUT-SPEC
  imports VERIFICATION-BODY-MUT

  // Deliberately retain the original > 0 specification after changing the
  // submitted body to > 1.
  claim [filter-loop-body-mut]:
    <k>
      #loop(
        list(intValsMut(INPUT)),
        Name("x"),
        positiveLoopBodyMut)
      ~> CONT
      => CONT
    </k>
    <env> LOCAL </env>
    <scopes>
      ...
      LOCAL |-> (
        scope(
          ("l" |-> ARG)
          ("result" |-> ref(ACC_LOC))
          ("x" |-> _OLD_X),
          parent(0))
        =>
        scope(
          ("l" |-> ARG)
          ("result" |-> ref(ACC_LOC))
          ("x" |-> ?_FINAL_X),
          parent(0)))
      ...
    </scopes>
    <heap>
      ...
      ACC_LOC |-> list(
        PREFIX
        =>
        filterPositiveMut(PREFIX, INPUT))
      ...
    </heap>
endmodule

