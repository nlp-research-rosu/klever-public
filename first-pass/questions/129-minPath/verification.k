// verification.k — minPath on the UNIFIED semantics. Faithful port of the 2x2-restricted old proof:
// grid = [[1, B], [C, D]] (B/C/D symbolic ints =/= 1 by the permutation domain), symbolic k. Phase 1
// (the nested grid scan) UNROLLS concretely (n=2) to val = min(B, C) (the two neighbors of the
// (0,0)=1 cell); phase 2 (`for i in range(k): ans += [1 if i%2==0 else val]`) is the symbolic part,
// summarized by altFrom over the range-loop. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module MIN-PATH-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // headAt(I, VAL) = 1 if I even, VAL if I odd (the phase-2 body's `1 if i%2==0 else val`). Split on
  // pyMod(I, 2) (Python's floored %, matching `i % 2`).
  syntax Int ::= headAt(Int, Int) [function, total]
  rule headAt(I:Int, _VAL:Int) => 1   requires pyMod(I, 2) ==Int 0 [simplification]
  rule headAt(I:Int,  VAL:Int) => VAL requires pyMod(I, 2) =/=Int 0 [simplification]

  // altFrom(ACC, I, K, VAL) = ACC with the alternating tail for indices I..K-1 appended (headAt(i)).
  // Recurses on the SAME valSeqConcat step the loop body (`ans = ans + [head_i]`) performs.
  syntax ValSeq ::= altFrom(ValSeq, Int, Int, Int) [function, total]
  rule altFrom(ACC:ValSeq, I:Int, K:Int, _VAL:Int) => ACC requires I >=Int K [simplification]
  rule altFrom(ACC:ValSeq, I:Int, K:Int, VAL:Int)
    => altFrom(valSeqConcat(ACC, vCons(headAt(I, VAL), .ValSeq)), I +Int 1, K, VAL)
    requires I <Int K [simplification]

endmodule
