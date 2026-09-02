requires "verif-nest.k"

module ITER-NEST-SPEC
  imports ITER-NEST
  // symbolic ValSeq nested under the known `wrap` ctor — the iterNext(list(VS)) shape.
  claim <k> #drive(wrap(VS:ValSeq)) => .K </k> [all-path]
endmodule
