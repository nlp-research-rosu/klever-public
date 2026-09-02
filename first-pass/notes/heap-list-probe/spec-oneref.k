requires "verif-heap.k"

module SPEC-ONEREF-SPEC
  imports VERIF-HEAP

  // invariant: one live ref P over a SYMBOLIC heap frame HR
  claim <k> #loop(VS:ValSeq, P:Int) => .K ... </k>
        <heap> P |-> L:ValSeq HR:Map => P |-> appAll(L, VS) HR </heap>
        [all-path]

  // entry: allocation + loop; fresh ref N lands in the symbolic initial heap H.
  // Postcondition heap stated in CONS-form (an update-form goal never simplifies —
  // only path-condition equations reach the decomposition lemma).
  claim <k> #run(VS:ValSeq) => .K ... </k>
        <heap> H:Map => N |-> appAll(.ValSeq, VS) H </heap>
        <nextref> N:Int => N +Int 1 </nextref>
        requires notBool N in_keys(H)
        [all-path]
endmodule
