requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY
  imports INT
  imports BOOL

  // Exact source-domain predicate: every element of the finite ValSeq is an
  // integer.  Its two equations are disjoint and cover all ValSeq values.
  syntax Bool ::= allInts(ValSeq) [function, total]
  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, VS:ValSeq))
    => isInt(V) andBool allInts(VS)

  // Guarded total twin of K's partial Val-to-Int subsort cast.  The #Ceil
  // characterization and orientation pair make it usable only where isInt
  // establishes definedness; no rule invents a value outside that domain.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  rule definedProjectInt(V:Val) => isInt(V)

  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Int)
    => ({ definedProjectInt(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectIntTotal(V:Val) => {V}:>Int
    requires definedProjectInt(V)
    [concrete, simplification(10), preserves-definedness]

  rule {V:Val}:>Int => projectIntTotal(V)
    requires definedProjectInt(V)
    [symbolic(V), simplification, preserves-definedness]

  rule projectIntTotal(I:Int) => I [simplification]
  rule projectIntTotal(projectIntTotal(V:Val))
    => projectIntTotal(V)
    [simplification]

  // Static-sort dispatch twins of the supplied MPY-INT equations.  The guards
  // are exactly the original Int/Int match domain expressed dynamically.
  rule applyBin("+", V:Val, W:Val)
    => projectIntTotal(V) +Int projectIntTotal(W)
    requires isInt(V) andBool isInt(W)
    [simplification]

  rule applyBin("*", V:Val, W:Val)
    => projectIntTotal(V) *Int projectIntTotal(W)
    requires isInt(V) andBool isInt(W)
    [simplification]

  // Mathematical left folds, including the empty identities.  The summaries
  // are consumed only under allInts; each projected head is therefore defined.
  syntax Int ::= sumFrom(ValSeq, Int) [function, total]
  rule sumFrom(.ValSeq, A:Int) => A
  rule sumFrom(vCons(V:Val, VS:ValSeq), A:Int)
    => sumFrom(VS, A +Int projectIntTotal(V))

  syntax Int ::= productFrom(ValSeq, Int) [function, total]
  rule productFrom(.ValSeq, A:Int) => A
  rule productFrom(vCons(V:Val, VS:ValSeq), A:Int)
    => productFrom(VS, A *Int projectIntTotal(V))
endmodule
