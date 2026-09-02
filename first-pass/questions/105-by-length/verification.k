// verification.k — by_length on the UNIFIED semantics. sorted(arr), read DESCENDING (s[n-1-i]), keep
// values in 1..9, map each to its word. Reuses the trusted-sort rung (sortVS, indexed via valSeqAt).
// DE-ESCAPED: under the allInt domain the filter compares are REAL Int inequalities (shared cast
// echo) and the 1..9->word map is the DEFINED wordOf table; krun runs the real compares + helper.
// The descending traversal, the filter, and the word map are all VERIFIED (residue: shared sortVS).
// See ./PROOF.md.

requires "../../reference/src/lemmas.k"

module BYLEN-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  // DE-ESCAPED: the geOneV/leNineV reroutes are DELETED — under allInt(SS) (claims carry
  // allInt(VS); lemmas/sort.k carries it through sortVS) the SHARED lemmas/subscript.k cast echo
  // reduces the compares to real atomic Int inequalities, which #branch splits.

  // word(v): the interception stays (per-element call in the loop) but targets the DEFINED
  // wordOf selector — the 10-equation digit-name table (out-of-range -> ""). Folded on a symbolic
  // element (projectIntTotal irreducible), reduced on any concrete digit.
  syntax Val ::= wordV(Val) [function, total, symbol(wordV)]
  rule wordV(valSeqAt(SS:ValSeq, J:Int)) => wordOf(projectIntTotal(valSeqAt(SS, J)))
    requires allInt(SS) [simplification]
  syntax Val ::= wordOf(Int) [function, total]
  rule wordOf(1) => str(iCons(79, iCons(110, iCons(101, .IntSeq)))) [simplification]
  rule wordOf(2) => str(iCons(84, iCons(119, iCons(111, .IntSeq)))) [simplification]
  rule wordOf(3) => str(iCons(84, iCons(104, iCons(114, iCons(101, iCons(101, .IntSeq)))))) [simplification]
  rule wordOf(4) => str(iCons(70, iCons(111, iCons(117, iCons(114, .IntSeq))))) [simplification]
  rule wordOf(5) => str(iCons(70, iCons(105, iCons(118, iCons(101, .IntSeq))))) [simplification]
  rule wordOf(6) => str(iCons(83, iCons(105, iCons(120, .IntSeq)))) [simplification]
  rule wordOf(7) => str(iCons(83, iCons(101, iCons(118, iCons(101, iCons(110, .IntSeq)))))) [simplification]
  rule wordOf(8) => str(iCons(69, iCons(105, iCons(103, iCons(104, iCons(116, .IntSeq)))))) [simplification]
  rule wordOf(9) => str(iCons(78, iCons(105, iCons(110, iCons(101, .IntSeq))))) [simplification]
  rule wordOf(I:Int) => str(.IntSeq)
    requires notBool (1 <=Int I andBool I <=Int 9) [simplification]
  syntax KItem ::= "#wordK"
  rule <k> Call(Name("word"), (E:Expr, .Exprs)) => E ~> #wordK ... </k>
  rule <k> V:Val ~> #wordK => wordV(V) ... </k>

  // buildFold(I, N, SS, ACC) = ACC ++ [ word(s[n-1-i]) | i in [I,N), 1 <= s[n-1-i] <= 9 ].
  syntax ValSeq ::= buildFold(Int, Int, ValSeq, ValSeq) [function, total]
  rule buildFold(I:Int, N:Int, _SS:ValSeq, ACC:ValSeq) => ACC requires I >=Int N [simplification]
  rule buildFold(I:Int, N:Int, SS:ValSeq, ACC:ValSeq)
    => buildFold(I +Int 1, N, SS, valSeqConcat(ACC, vCons(wordV(valSeqAt(SS, N -Int 1 -Int I)), .ValSeq)))
    requires I <Int N andBool projectIntTotal(valSeqAt(SS, N -Int 1 -Int I)) >=Int 1 andBool projectIntTotal(valSeqAt(SS, N -Int 1 -Int I)) <=Int 9 [simplification]
  rule buildFold(I:Int, N:Int, SS:ValSeq, ACC:ValSeq)
    => buildFold(I +Int 1, N, SS, ACC)
    requires I <Int N andBool notBool (projectIntTotal(valSeqAt(SS, N -Int 1 -Int I)) >=Int 1 andBool projectIntTotal(valSeqAt(SS, N -Int 1 -Int I)) <=Int 9) [simplification]

endmodule
