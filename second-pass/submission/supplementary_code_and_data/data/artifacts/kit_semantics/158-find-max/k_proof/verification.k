requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // A guarded total twin of the partial Val-to-Str subsort projection.
  syntax Bool ::= definedProjectStr(Val) [function, total]
  rule definedProjectStr(V:Val) => isStr(V)

  syntax Str ::= projectStrTotal(Val)
    [function, total, symbol(projectStrTotal), no-evaluators]

  rule #Ceil({@V:Val}:>Str)
    => ({ definedProjectStr(@V) #Equals true } #And #Ceil(@V))
    [simplification]

  rule projectStrTotal(V:Val) => {V}:>Str
    requires definedProjectStr(V)
    [concrete, simplification(10), preserves-definedness]
  rule {V:Val}:>Str => projectStrTotal(V)
    requires definedProjectStr(V)
    [symbolic(V), simplification, preserves-definedness]
  rule projectStrTotal(S:Str) => S [simplification]
  rule projectStrTotal(projectStrTotal(V)) => projectStrTotal(V) [simplification]

  syntax IntSeq ::= codesOf(Str) [function, total]
  rule codesOf(str(CS)) => CS

  // The complete dynamic input-domain predicate.
  syntax Bool ::= allStrings(ValSeq) [function, total]
  rule allStrings(.ValSeq) => true
  rule allStrings(vCons(V, REST))
    => definedProjectStr(V) andBool notBool isRefV(V) andBool allStrings(REST)

  // Guarded dispatch twins of the fixed set(str) and str < str equations.
  rule applyBuiltin("set", V:Val, .Vals)
    => setV(dedupCodes(codesOf(projectStrTotal(V))))
    requires definedProjectStr(V)
    [simplification]

  rule applyCmp("<", A:Val, B:Val)
    => strLt(codesOf(projectStrTotal(A)), codesOf(projectStrTotal(B)))
    requires definedProjectStr(A) andBool definedProjectStr(B)
    [simplification]

  // The score used by the HumanEval contract.
  syntax Int ::= uniqueCount(Val) [function, total]
  rule uniqueCount(V)
    => isLen(dedupCodes(codesOf(projectStrTotal(V))))

  // A candidate wins on score, then on lexicographically smaller spelling.
  syntax Bool ::= candidateWins(Val, Val, Int) [function, total]
  rule candidateWins(V, BEST, SCORE)
    => uniqueCount(V) >Int SCORE
       orBool (uniqueCount(V) ==Int SCORE
               andBool strLt(
                 codesOf(projectStrTotal(V)),
                 codesOf(projectStrTotal(BEST))))

  // Exact mathematical fold computed by the outer loop.
  syntax Val ::= bestWord(ValSeq, Val, Int) [function, total]
  rule bestWord(.ValSeq, BEST, _SCORE) => BEST
  rule bestWord(vCons(V, REST), BEST, SCORE)
    => #if candidateWins(V, BEST, SCORE)
       #then bestWord(REST, V, uniqueCount(V))
       #else bestWord(REST, BEST, SCORE)
       #fi

  syntax Int ::= bestScore(ValSeq, Val, Int) [function, total]
  rule bestScore(.ValSeq, _BEST, SCORE) => SCORE
  rule bestScore(vCons(V, REST), BEST, SCORE)
    => #if candidateWins(V, BEST, SCORE)
       #then bestScore(REST, V, uniqueCount(V))
       #else bestScore(REST, BEST, SCORE)
       #fi

  // Exact final values of the loop target and its per-element score temporary.
  syntax Val ::= lastWord(ValSeq, Val) [function, total]
  rule lastWord(.ValSeq, WORD)         => WORD
  rule lastWord(vCons(V, REST), _WORD) => lastWord(REST, V)

  syntax Int ::= lastScore(ValSeq, Int) [function, total]
  rule lastScore(.ValSeq, SCORE)         => SCORE
  rule lastScore(vCons(V, REST), _SCORE) => lastScore(REST, uniqueCount(V))
endmodule
