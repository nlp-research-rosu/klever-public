// verification.k — sort_array on the UNIFIED semantics. Combines TWO capabilities: the isInt
// echo (the parity flag (array[0]+array[-1])%2==0 is arithmetic on two symbolic elements) and
// the trusted-sort LOOP-INDEX reconstruction (sorted ascending if the flag is false, descending
// if true — for an int list, sorted(x, reverse=True) == reversed(sorted(x))). solution.py
// rebuilds sorted(array, reverse=flag) by index. See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module SORT-ARRAY-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // rev flag: (array[0] + array[-1]) % 2 == 0 (array[-1] index = -1 + len).
  syntax Bool ::= sortArrRev(ValSeq) [function, total]
  rule sortArrRev(VS:ValSeq)
    => pyMod(projectIntTotal(valSeqAt(VS, 0)) +Int projectIntTotal(valSeqAt(VS, -1 +Int vsLen(VS))), 2) ==Int 0
    [simplification]

  // rev-branched loop-index reconstruction over the sorted list SS: descending (rev) reads
  // s[n-1-i]; ascending reads s[i].
  syntax ValSeq ::= sortArrFold(Bool, Int, Int, ValSeq, ValSeq) [function, total]
  rule sortArrFold(_REV:Bool, I:Int, N:Int, _SS:ValSeq, ACC:ValSeq) => ACC requires I >=Int N [simplification]
  rule sortArrFold(true, I:Int, N:Int, SS:ValSeq, ACC:ValSeq)
    => sortArrFold(true, I +Int 1, N, SS, valSeqConcat(ACC, vCons(valSeqAt(SS, normIdx(N -Int 1 -Int I, vsLen(SS))), .ValSeq)))
    requires I <Int N [simplification]
  rule sortArrFold(false, I:Int, N:Int, SS:ValSeq, ACC:ValSeq)
    => sortArrFold(false, I +Int 1, N, SS, valSeqConcat(ACC, vCons(valSeqAt(SS, normIdx(I, vsLen(SS))), .ValSeq)))
    requires I <Int N [simplification]

  // result: sorted(array, reverse=rev) rebuilt by index.
  syntax Val ::= sortArrRes(ValSeq) [function]
  rule sortArrRes(VS:ValSeq)
    => list(sortArrFold(sortArrRev(VS), 0, vsLen(VS), sortVS(VS), .ValSeq)) [simplification]
endmodule
