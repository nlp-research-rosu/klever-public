requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // A typed logical view of the admissible input: every element is a string.
  syntax WordSeq ::= ".WordSeq" | wCons(IntSeq, WordSeq)
  syntax ValSeq ::= wordVals(WordSeq)
  rule wordVals(.WordSeq) => .ValSeq
  rule wordVals(wCons(WORD:IntSeq, REST:WordSeq))
    => vCons(str(WORD), wordVals(REST))

  // Constructor-preserving iterator lemmas keep the string element sort visible
  // to symbolic execution.  They are immediate compositions of wordVals with
  // MPY-LIST's two #iterNext equations.
  rule <k> #iterNext(list(wordVals(.WordSeq))) => #iterDone ... </k>
    [priority(40)]
  rule <k> #iterNext(list(wordVals(wCons(WORD:IntSeq, REST:WordSeq))))
        => #iterYield(str(WORD), list(wordVals(REST))) ... </k>
    [priority(40)]

  // Exact translated body of solution.py, named only to keep the claims small.
  syntax Stmts ::= "findMaxLoopBody" [function]
  rule findMaxLoopBody
    => Assign(
         Name("unique"),
         Call(Name("len"), Call(Name("set"), Name("word"))))
       If(Compare(Name("unique"), CmpOp(">", Name("max_unique"))),
         Assign(Name("max_unique"), Name("unique")),
         If(Compare(Name("unique"), CmpOp("==", Name("max_unique"))),
           If(Compare(Name("word"), CmpOp("<", Name("best"))),
             Assign(Name("best"), Name("word")),
             .Stmts),
           .Stmts))

  syntax Stmts ::= "findMaxFunctionBody" [function]
  rule findMaxFunctionBody
    => Assign(Name("best"), Str(""))
       Assign(Name("max_unique"), Int(0))
       Assign(Name("word"), Str(""))
       Assign(Name("unique"), Int(0))
       For(Name("word"), Name("words"), findMaxLoopBody)
       Return(Name("best"))

  // A mathematical accumulator for the contract.  The IntSeq is the selected
  // word and the Int is its number of distinct characters.
  syntax BestState ::= bestState(IntSeq, Int)
                     | findMaxWords(WordSeq, IntSeq, Int) [function, total]

  rule findMaxWords(.WordSeq, BEST:IntSeq, SCORE:Int)
    => bestState(BEST, SCORE)

  rule findMaxWords(
         wCons(WORD:IntSeq, REST:WordSeq),
         _BEST:IntSeq,
         SCORE:Int)
    => findMaxWords(REST, WORD, isLen(dedupCodes(WORD)))
    requires isLen(dedupCodes(WORD)) >Int SCORE

  rule findMaxWords(
         wCons(WORD:IntSeq, REST:WordSeq),
         BEST:IntSeq,
         SCORE:Int)
    => findMaxWords(REST, WORD, SCORE)
    requires isLen(dedupCodes(WORD)) ==Int SCORE
     andBool strLt(WORD, BEST)

  rule findMaxWords(
         wCons(WORD:IntSeq, REST:WordSeq),
         BEST:IntSeq,
         SCORE:Int)
    => findMaxWords(REST, BEST, SCORE)
    requires isLen(dedupCodes(WORD)) <Int SCORE

  rule findMaxWords(
         wCons(WORD:IntSeq, REST:WordSeq),
         BEST:IntSeq,
         SCORE:Int)
    => findMaxWords(REST, BEST, SCORE)
    requires isLen(dedupCodes(WORD)) ==Int SCORE
     andBool notBool strLt(WORD, BEST)

  syntax IntSeq ::= bestWord(BestState) [function, total]
  rule bestWord(bestState(WORD:IntSeq, _:Int)) => WORD

  syntax Int ::= bestScore(BestState) [function, total]
  rule bestScore(bestState(_:IntSeq, SCORE:Int)) => SCORE

  // Projection lemmas let the simplifier expose one specification step under
  // the path condition selected by the Python branch.
  rule bestWord(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), _BEST:IntSeq, SCORE:Int))
    => bestWord(findMaxWords(REST, WORD, isLen(dedupCodes(WORD))))
    requires isLen(dedupCodes(WORD)) >Int SCORE
    [simplification]
  rule bestScore(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), _BEST:IntSeq, SCORE:Int))
    => bestScore(findMaxWords(REST, WORD, isLen(dedupCodes(WORD))))
    requires isLen(dedupCodes(WORD)) >Int SCORE
    [simplification]

  rule bestWord(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), BEST:IntSeq, SCORE:Int))
    => bestWord(findMaxWords(REST, WORD, SCORE))
    requires isLen(dedupCodes(WORD)) ==Int SCORE
     andBool strLt(WORD, BEST)
    [simplification]
  rule bestScore(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), BEST:IntSeq, SCORE:Int))
    => bestScore(findMaxWords(REST, WORD, SCORE))
    requires isLen(dedupCodes(WORD)) ==Int SCORE
     andBool strLt(WORD, BEST)
    [simplification]

  rule bestWord(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), BEST:IntSeq, SCORE:Int))
    => bestWord(findMaxWords(REST, BEST, SCORE))
    requires isLen(dedupCodes(WORD)) <Int SCORE
    [simplification]
  rule bestScore(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), BEST:IntSeq, SCORE:Int))
    => bestScore(findMaxWords(REST, BEST, SCORE))
    requires isLen(dedupCodes(WORD)) <Int SCORE
    [simplification]

  rule bestWord(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), BEST:IntSeq, SCORE:Int))
    => bestWord(findMaxWords(REST, BEST, SCORE))
    requires isLen(dedupCodes(WORD)) ==Int SCORE
     andBool notBool strLt(WORD, BEST)
    [simplification]
  rule bestScore(findMaxWords(wCons(WORD:IntSeq, REST:WordSeq), BEST:IntSeq, SCORE:Int))
    => bestScore(findMaxWords(REST, BEST, SCORE))
    requires isLen(dedupCodes(WORD)) ==Int SCORE
     andBool notBool strLt(WORD, BEST)
    [simplification]
endmodule
