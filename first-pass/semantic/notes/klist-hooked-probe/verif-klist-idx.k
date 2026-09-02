// verif-klist-idx.k — the RIGHT question (user correction): can a builtin List OF VALS carry
// the full casts.k trick — a totalized index access getTotal(L, I) (the RV #getIntsTotal
// pattern) + the projectIntTotal element cast — so INDEX-based proofs work with no container
// narrowing (the index case-splits against size(L), an opaque Int)?
// Design note: the SEMANTICS reads unconditionally through total fns (production style —
// domain guards live in the proof layer only); an isInt guard on a semantics rule stalls
// rule selection (first probe run).
module VERIF-KLIST-IDX
  imports INT
  imports BOOL
  imports LIST
  imports K-EQUAL

  configuration <k> $PGM:K </k> <acc> 0 </acc>

  syntax Val ::= Int | "other"

  // ==== the total Int cast (casts.k core, verbatim architecture) ============
  syntax Bool ::= definedProjectInt(KItem) [function, total]
  rule definedProjectInt(K:KItem) => isInt(K)

  syntax Int ::= projectIntTotal(KItem) [function, total, no-evaluators]

  rule #Ceil({@Arg0:KItem}:>Int) => ({ definedProjectInt(@Arg0) #Equals true } #And #Ceil(@Arg0))
    [simplification]
  rule projectIntTotal(Arg0:KItem) => {Arg0}:>Int
    requires definedProjectInt(Arg0)
    [concrete, simplification(10), preserves-definedness]
  rule {Arg0:KItem}:>Int => projectIntTotal(Arg0)
    requires definedProjectInt(Arg0)
    [symbolic(Arg0), simplification, preserves-definedness]
  rule projectIntTotal(I:Int) => I [simplification]

  // ==== the total List access (the SAME trick, one level up) ================
  syntax Bool ::= definedGet(List, Int) [function, total]
  rule definedGet(L:List, I:Int) => (0 -Int size(L)) <=Int I andBool I <Int size(L)

  syntax KItem ::= getTotal(List, Int) [function, total, no-evaluators]

  rule #Ceil(@L:List [ @I:Int ]) => ({ definedGet(@L, @I) #Equals true } #And #Ceil(@L) #And #Ceil(@I))
    [simplification]
  rule getTotal(L:List, I:Int) => L [ I ]
    requires definedGet(L, I)
    [concrete, simplification(10), preserves-definedness]
  rule L:List [ I:Int ] => getTotal(L, I)
    requires definedGet(L, I)
    [symbolic(L), simplification, preserves-definedness]

  // size is non-negative (stdlib does not say so)
  rule size(_L:List) >=Int 0 => true [simplification]
  rule size(_L:List) <Int 0  => false [simplification]

  // ==== the index-loop semantics: reads through TOTAL fns, no proof-layer guards ====
  syntax KItem ::= #isum(List, Int)
  rule <k> #isum(L:List, I:Int) => .K ... </k>
       requires I >=Int size(L)
  rule <k> #isum(L:List, I:Int) => #isum(L, I +Int 1) ... </k>
       <acc> A:Int => A +Int projectIntTotal(getTotal(L, I)) </acc>
       requires 0 <=Int I andBool I <Int size(L)

  // ==== proof layer ==========================================================
  // leg idx2: junk-tolerant summary (no domain premise — isolates the container mechanics)
  syntax Int ::= sumFrom(List, Int) [function, total]
  rule sumFrom(L:List, I:Int) => 0
       requires I >=Int size(L) [simplification]
  rule sumFrom(L:List, I:Int) => projectIntTotal(getTotal(L, I)) +Int sumFrom(L, I +Int 1)
       requires 0 <=Int I andBool I <Int size(L) [simplification]

  // leg idx3: declare-then-guard summary + index-recursive domain predicate (production style)
  syntax Bool ::= allIntFrom(List, Int) [function, total]
  rule allIntFrom(L:List, I:Int) => true
       requires I >=Int size(L) [simplification]
  rule allIntFrom(L:List, I:Int) => isInt(getTotal(L, I)) andBool allIntFrom(L, I +Int 1)
       requires 0 <=Int I andBool I <Int size(L) [simplification]

  syntax Int ::= sumFromG(List, Int) [function, total]
  rule sumFromG(L:List, I:Int) => 0
       requires I >=Int size(L) [simplification]
  rule sumFromG(L:List, I:Int) => {getTotal(L, I)}:>Int +Int sumFromG(L, I +Int 1)
       requires 0 <=Int I andBool I <Int size(L) andBool isInt(getTotal(L, I)) [simplification]
endmodule
