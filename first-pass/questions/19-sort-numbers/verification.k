// verification.k — sort_numbers on the UNIFIED semantics, TRAP-FREE (W3 P19).
// solution.py is canonical verbatim; the keyed sort is the SHARED opaque
// sortKeyVS with the lambda closure inside the atom (P145); the filtering
// comprehension folds via ftAcc; the join is the shared joinCodes.

requires "../../reference/src/lemmas.k"

module SORT-NUMBERS-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC
  imports K-EQUAL

  syntax Expr ::= Val

  // truthy of an abstract str element: the branchable isLen atom (same
  // spelling as ftAcc's guards, so the If case-split lines up with the fold)
  rule truthy(V:Val) => notBool (isLen(codesProj(V)) ==Int 0)
    requires isStr(V) [simplification]

  // the comp's `if x` filter over the split tokens, threaded-accumulator
  // style (the Q4 sadSeq shape): ftAcc(WS, ACC) = ACC ++ [nonempty strs of WS]
  syntax ValSeq ::= ftAcc(ValSeq, ValSeq) [function, total, no-evaluators]
  rule ftAcc(.ValSeq, ACC:ValSeq) => ACC [simplification]
  rule ftAcc(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => ftAcc(R, valSeqConcat(ACC, vCons(V, .ValSeq)))
    requires notBool (isLen(codesProj(V)) ==Int 0) [simplification]
  rule ftAcc(vCons(V:Val, R:ValSeq), ACC:ValSeq)
    => ftAcc(R, ACC)
    requires isLen(codesProj(V)) ==Int 0 [simplification]
endmodule
