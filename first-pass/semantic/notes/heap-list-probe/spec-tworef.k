requires "verif-heap.k"

module SPEC-TWOREF-SPEC
  imports VERIF-HEAP

  // the aliasing-bookkeeping question: a SECOND live ref Q in the heap; the invariant only
  // proves if the prover can keep P and Q apart (explicit distinctness premise)
  claim <k> #loop(VS:ValSeq, P:Int) => .K ... </k>
        <heap> P |-> L:ValSeq Q |-> M:ValSeq HR:Map => P |-> appAll(L, VS) Q |-> M HR </heap>
        requires P =/=Int Q
        [all-path]
endmodule
