requires "verif-heap.k"

module SPEC-ENTRY-EMPTY-SPEC
  imports VERIF-HEAP

  // the invariant (needed as the circularity for the loop inside #run)
  claim <k> #loop(VS:ValSeq, P:Int) => .K ... </k>
        <heap> P |-> L:ValSeq HR:Map => P |-> appAll(L, VS) HR </heap>
        [all-path]

  // production-shaped entry: CONCRETE initial heap (programs start empty)
  claim <k> #run(VS:ValSeq) => .K ... </k>
        <heap> .Map => 0 |-> appAll(.ValSeq, VS) </heap>
        <nextref> 0 => 1 </nextref>
        [all-path]
endmodule
