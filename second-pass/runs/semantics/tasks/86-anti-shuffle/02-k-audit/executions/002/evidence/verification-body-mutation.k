requires "reference-semantics/semantics.k"

module ANTI-SHUFFLE-BASE
  imports MPY

  // The two macros below are the exact constructor form emitted in
  // solution.mpy.  Naming the blocks keeps the reachability claims readable.
  syntax Stmts ::= "antiLoopBody" [macro]
  rule antiLoopBody
    => AugAssign(
         Name("result"),
         "+",
         Call(
           Attribute(Str(""), "join"),
           Call(Name("sorted"), Call(Name("list"), Name("word")))))
       AugAssign(Name("result"), "+", Str("!"))
       .Stmts

  syntax Stmts ::= "antiBody" [macro]
  rule antiBody
    => Assign(Name("result"), Str(""))
       Assign(Name("word"), Str(""))
       For(
         Name("word"),
         Call(Attribute(Name("s"), "split"), Str(" ")),
         antiLoopBody)
       Return(
         Subscript(
           Name("result"),
           Slice(NoBound, UnaryOp("-", Int(1)), NoBound)))
       .Stmts

  // sortWord is the semantics-level meaning of
  //     "".join(sorted(list(word)))
  // sortVS is intentionally the supplied trusted symbolic sorting primitive.
  syntax IntSeq ::= sortWord(IntSeq) [function, total]
  rule sortWord(W:IntSeq)
    => joinCodes(.IntSeq, sortVS(charsOf(W)))

  // A typed sequence of word code sequences. This avoids asking the prover to
  // recover "every element is a string" from an abstract ValSeq.
  syntax Words ::= ".Words" | wCons(IntSeq, Words)

  syntax ValSeq ::= wordVals(Words) [function, total]
  rule wordVals(.Words) => .ValSeq
  rule wordVals(wCons(W:IntSeq, REST:Words))
    => vCons(str(W), wordVals(REST))

  // The same recurrence as the supplied splitSep, with the result represented
  // by Words. WORD-SPEC proves their equivalence.
  syntax Words ::= splitWords(IntSeq, Int, IntSeq) [function, total]
  rule splitWords(.IntSeq, _SEP:Int, CUR:IntSeq)
    => wCons(CUR, .Words)
  rule splitWords(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq)
    => wCons(CUR, splitWords(R, SEP, .IntSeq))
    requires C ==Int SEP
  rule splitWords(iCons(C:Int, R:IntSeq), SEP:Int, CUR:IntSeq)
    => splitWords(R, SEP, seqConcat(CUR, iCons(C, .IntSeq)))
    requires notBool (C ==Int SEP)

  // emitWordSeq describes the loop before its final result[:-1]: every sorted
  // word is followed by exactly one ASCII space.
  syntax IntSeq ::= emitWordSeq(Words) [function, total]
  rule emitWordSeq(.Words) => .IntSeq
  rule emitWordSeq(wCons(W:IntSeq, REST:Words))
    => seqConcat(sortWord(W), iCons(32, emitWordSeq(REST)))

  // Declarative contract. splitSep preserves empty fields, so leading,
  // trailing, and repeated spaces are all preserved. The slice removes only
  // the loop's one deliberately-added trailing space.
  syntax Val ::= antiShuffleSpec(IntSeq) [function, total]
  rule antiShuffleSpec(S:IntSeq)
    => doSlice(
         str(emitWordSeq(splitWords(S, 32, .IntSeq))),
         noB,
         someB(-1),
         noB)

  // Algebraic normalizations needed by the accumulator invariant. Both are
  // standard consequences of seqConcat's defining equations.
  rule seqConcat(A:IntSeq, .IntSeq) => A [simplification]
  rule seqConcat(seqConcat(A:IntSeq, B:IntSeq), C:IntSeq)
    => seqConcat(A, seqConcat(B, C))
    [simplification]
endmodule

module ANTI-SHUFFLE-LOOP-VERIFICATION
  imports ANTI-SHUFFLE-BASE

  // Iteration-only view of split's result. The program never observes the
  // temporary list except through For, so this avoids an opaque symbolic
  // ValSeq while retaining splitSep's exact recurrence.
  syntax Iterable ::= wordsObj(Words)
  rule <k> #iterNext(wordsObj(.Words)) => #iterDone ... </k>
  rule <k> #iterNext(wordsObj(wCons(W:IntSeq, REST:Words)))
        => #iterYield(str(W), wordsObj(REST)) ... </k>

  rule <k>
         #applyK(
           toCall(boundMethodV(str(S:IntSeq), "split")),
           (str(iCons(SEP:Int, .IntSeq)), .Vals))
         => wordsObj(splitWords(S, SEP, .IntSeq))
         ...
       </k>
       [priority(35)]

  // Observational summary of the two temporary list allocations used to sort
  // one word. WORD-SPEC proves this composition separately from MPY rules.
  rule <k>
         Call(
           Attribute(Str(""), "join"),
           Call(Name("sorted"), Call(Name("list"), Name("word"))))
         => str(sortWord(W))
         ...
       </k>
       <env> L:Int </env>
       <scopes> ... L |-> scope(M:Map, _:Parent) ... </scopes>
       requires "word" in_keys(M)
       andBool {M["word"]}:>Val ==K str(W:IntSeq)
       [priority(40)]
endmodule

module ANTI-SHUFFLE-VERIFICATION
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  // This is the proved anti-loop reachability invariant, installed as a
  // summary for the end-to-end claim. loop-spec.k proves it without this rule.
  rule <k>
         #loop(wordsObj(WS:Words), Name("word"), antiLoopBody)
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         ... 1 |-> scope(
           (("result" |-> str(A:IntSeq)) M:Map)
           =>
           (("result" |-> str(seqConcat(A, emitWordSeq(WS)))) M),
           P:Parent)
         ...
       </scopes>
       requires notBool ("result" in_keys(M))
       [priority(40)]
endmodule
