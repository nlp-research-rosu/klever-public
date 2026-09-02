// verification.k — find_closest_elements on the UNIFIED semantics. Nested min-scan over a pair
// of INDEXED symbolic elements: d = abs(numbers[i] - numbers[j]), tracking the closest (dist,
// lo, hi). The element arithmetic (abs of a difference) and the min/max builtins on two symbolic
// elements need the isInt echoes (see reference/notes/isint-bridge-probe). See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module CLOSEST-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // ---- isInt echoes under allInt (SOUND). applyBin/applyBuiltin/minVals/maxVals are function
  // symbols → legal [simplification] LHSs.
  // (a) subtraction of two elements — for numbers[i] - numbers[j].
  // (b) min/max with an element as the FIRST arg (routes into minVals/maxVals with an Int seed).
  rule applyBuiltin("min", valSeqAt(NUMS:ValSeq, I:Int), REST:Vals)
    => applyBuiltin("min", projectIntTotal(valSeqAt(NUMS, I)), REST) requires allInt(NUMS) [simplification]
  rule applyBuiltin("max", valSeqAt(NUMS:ValSeq, I:Int), REST:Vals)
    => applyBuiltin("max", projectIntTotal(valSeqAt(NUMS, I)), REST) requires allInt(NUMS) [simplification]
  // (c) min/max with an element in the REST (the second arg).
  rule minVals(M:Int, (valSeqAt(NUMS:ValSeq, J:Int), R:Vals))
    => minVals(M, (projectIntTotal(valSeqAt(NUMS, J)), R)) requires allInt(NUMS) [simplification]
  rule maxVals(M:Int, (valSeqAt(NUMS:ValSeq, J:Int), R:Vals))
    => maxVals(M, (projectIntTotal(valSeqAt(NUMS, J)), R)) requires allInt(NUMS) [simplification]

  // ---- the (dist, lo, hi) accumulator triple -----------------------------------------------
  syntax Acc ::= acc(Int, Int, Int)
  syntax Int ::= accD(Acc)  [function, total]
               | accLo(Acc) [function, total]
               | accHi(Acc) [function, total]
  rule accD(acc(D:Int, _:Int, _:Int))  => D
  rule accLo(acc(_:Int, LO:Int, _:Int)) => LO
  rule accHi(acc(_:Int, _:Int, HI:Int)) => HI

  // one comparison: strict-`<` min-update of the (dist, lo, hi) triple, on the PROJECTED int
  // elements A, B (matching the program's abs/min/max builtins after the echoes).
  syntax Acc ::= step(Acc, Int, Int) [function, total]
  rule step(acc(D:Int, _LO:Int, _HI:Int), A:Int, B:Int) => acc(absInt(A -Int B), minInt(A, B), maxInt(A, B))
       requires absInt(A -Int B) <Int D [simplification]
  rule step(acc(D:Int, LO:Int, HI:Int), A:Int, B:Int) => acc(D, LO, HI)
       requires absInt(A -Int B) >=Int D [simplification]

  // inner fold: j in [J, N), fixed outer index I, skip j == I; step on the projected elements.
  syntax Acc ::= innerFold(Int, Int, Int, ValSeq, Acc) [function, total]
  rule innerFold(J:Int, N:Int, _I:Int, _NUMS:ValSeq, A:Acc) => A
       requires J >=Int N [simplification]
  rule innerFold(J:Int, N:Int, I:Int, NUMS:ValSeq, A:Acc) => innerFold(J +Int 1, N, I, NUMS, A)
       requires J <Int N andBool J ==Int I [simplification]
  rule innerFold(J:Int, N:Int, I:Int, NUMS:ValSeq, A:Acc)
        => innerFold(J +Int 1, N, I, NUMS, step(A, projectIntTotal(valSeqAt(NUMS, I)), projectIntTotal(valSeqAt(NUMS, J))))
       requires J <Int N andBool J =/=Int I [simplification]

  // outer fold: i in [I, N), each running the full inner fold; threaded back in projected form
  // acc(accD F, accLo F, accHi F) (= F) so the outer circularity matches the split store cells.
  syntax Acc ::= outerFold(Int, Int, ValSeq, Acc) [function, total]
  rule outerFold(I:Int, N:Int, _NUMS:ValSeq, A:Acc) => A
       requires I >=Int N [simplification]
  rule outerFold(I:Int, N:Int, NUMS:ValSeq, A:Acc)
        => outerFold(I +Int 1, N, NUMS,
             acc(accD(innerFold(0, N, I, NUMS, A)), accLo(innerFold(0, N, I, NUMS, A)), accHi(innerFold(0, N, I, NUMS, A))))
       requires I <Int N [simplification]

  // seed = the (0,1) pair, sorted; result tuple = (lo, hi) of the full scan.
  syntax Acc ::= seedAcc(ValSeq) [function, total]
  rule seedAcc(NUMS:ValSeq)
        => acc(absInt(projectIntTotal(valSeqAt(NUMS, 0)) -Int projectIntTotal(valSeqAt(NUMS, 1))),
               minInt(projectIntTotal(valSeqAt(NUMS, 0)), projectIntTotal(valSeqAt(NUMS, 1))),
               maxInt(projectIntTotal(valSeqAt(NUMS, 0)), projectIntTotal(valSeqAt(NUMS, 1))))
       [simplification]
  syntax Val ::= closestRes(ValSeq, Int) [function]
  rule closestRes(NUMS:ValSeq, N:Int)
        => tuple(vCons(accLo(outerFold(0, N, NUMS, seedAcc(NUMS))), vCons(accHi(outerFold(0, N, NUMS, seedAcc(NUMS))), .ValSeq)))
       [simplification]
endmodule
