requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  // Recursive domain predicate for arbitrary finite semantic integer lists.
  syntax Bool ::= allInts(ValSeq) [function, total]

  // A guarded total twin of the partial Val-to-Int subsort projection.  It has
  // no evaluator and can only collapse to a value already known to be an Int.
  syntax Bool ::= definedProjectInt(Val) [function, total]
  syntax Int ::= projectIntTotal(Val)
    [function, total, symbol(projectIntTotal), no-evaluators]

  // addSummary(VS, ODD) is the mathematical sum still to be accumulated
  // while traversing VS, where ODD is the parity of the next index.
  syntax Int ::= addSummary(ValSeq, Bool) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX

  rule allInts(.ValSeq) => true
  rule allInts(vCons(V:Val, VS:ValSeq))
    => isInt(V) andBool allInts(VS)

  rule definedProjectInt(V:Val) => isInt(V)

  // Standard guarded-total-projection characterization (the ceils.k idiom).
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
    => projectIntTotal(V) [simplification]

  // Guarded dispatch twins of the exact MPY-INT equations.  These compensate
  // only for the backend's lack of path-condition-based static sort refinement.
  rule applyBin("%", V:Val, I:Int)
    => pyMod(projectIntTotal(V), I)
    requires isInt(V)
    [simplification]
  rule applyBin("+", I:Int, V:Val)
    => I +Int projectIntTotal(V)
    requires isInt(V)
    [simplification]

  // Definitional postcondition summary.  It does not rewrite program syntax or
  // operational K items: the supplied MPY rules execute the complete body.
  rule addSummary(.ValSeq, _:Bool) => 0
  rule addSummary(vCons(_:Val, VS:ValSeq), false)
    => addSummary(VS, true)
  rule addSummary(vCons(V:Val, VS:ValSeq), true)
    => (#if pyMod(projectIntTotal(V), 2) ==Int 0
        #then projectIntTotal(V)
        #else 0
        #fi)
       +Int addSummary(VS, false)
endmodule
