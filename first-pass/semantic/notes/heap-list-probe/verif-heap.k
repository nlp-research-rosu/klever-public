// verif-heap.k — probe: lists as HEAP REFERENCES (true Python reference semantics).
// The accumulator list lives in a <heap> Map cell behind an lref; append = heap update.
// Measures the PROOF-side cost of the heap: (1) invariant must expose the ref's heap entry
// over a symbolic frame; (2) with two live refs the claim needs explicit distinctness.
module VERIF-HEAP
  imports INT
  imports BOOL
  imports MAP
  imports K-EQUAL

  configuration <k> $PGM:K </k> <heap> .Map </heap> <nextref> 0 </nextref>

  syntax Val ::= Int | lref(Int)
  syntax ValSeq ::= ".ValSeq" | vCons(Val, ValSeq)

  syntax ValSeq ::= vSnoc(ValSeq, Val) [function, total]
  rule vSnoc(.ValSeq, V:Val)        => vCons(V, .ValSeq)
  rule vSnoc(vCons(W:Val, R:ValSeq), V:Val) => vCons(W, vSnoc(R, V))

  // allocate a fresh empty list, then append every element of the (by-value) input to it
  syntax KItem ::= #run(ValSeq) | #loop(ValSeq, Int)
  // allocation emits CONS-form directly (an update-form H[N <- _] never re-normalizes
  // symbolically, even with freshness in the path condition — probed)
  rule <k> #run(VS:ValSeq) => #loop(VS, N) ... </k>
       <heap> H:Map => (N |-> .ValSeq) H </heap>
       <nextref> N:Int => N +Int 1 </nextref>
       requires notBool N in_keys(H)

  rule <k> #loop(.ValSeq, _:Int) => .K ... </k>
  rule <k> #loop(vCons(V:Val, R:ValSeq), P:Int) => #loop(R, P) ... </k>
       <heap> ... P |-> (L:ValSeq => vSnoc(L, V)) ... </heap>

  // the summary: what the accumulator holds after appending all of VS
  syntax ValSeq ::= appAll(ValSeq, ValSeq) [function, total]
  rule appAll(A:ValSeq, .ValSeq)                => A [simplification]
  rule appAll(A:ValSeq, vCons(V:Val, R:ValSeq)) => appAll(vSnoc(A, V), R) [simplification]

  // update-form vs cons-form map equation decomposition (the stdlib's term-level
  // M[K <- V] => K |-> V M never fires inside an unsolved equation): with K fresh
  // for both rests, the maps agree iff the K-values agree and the rests agree
  rule { M:Map [ K:KItem <- V:KItem ] #Equals (K |-> W:KItem REST:Map) }
    => { V #Equals W } #And { M #Equals REST }
    requires notBool K in_keys(M) andBool notBool K in_keys(REST)
    [simplification]
  rule { (K |-> W:KItem REST:Map) #Equals M:Map [ K:KItem <- V:KItem ] }
    => { V #Equals W } #And { M #Equals REST }
    requires notBool K in_keys(M) andBool notBool K in_keys(REST)
    [simplification]
endmodule
