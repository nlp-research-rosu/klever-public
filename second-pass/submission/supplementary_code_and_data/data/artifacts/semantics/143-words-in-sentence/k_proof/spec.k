requires "verification.k"

module SPEC
  imports VERIFICATION

  // Inductive loop invariant.  The function initializes word and n before the
  // loop, so each iteration only overwrites existing local-map entries.
  claim [loop-invariant]:
    <k>
      #loop(
        list(wordsVals(W:WordSeq)),
        Name("word"),
        solutionLoopBody)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ("result" |-> str(A:IntSeq))
        ("word"   |-> OLDWORD:Val)
        ("n"      |-> OLDN:Int)
        ("_plain" |-> 0)
        REST:Map,
        P:Parent)
      =>
      L |-> scope(
        ("result" |-> str(filterWords(A, W)))
        ("word"   |-> ?FINALWORD:Val)
        ("n"      |-> ?FINALN:Int)
        ("_plain" |-> 0)
        REST,
        P)
      ...
    </scopes>
    requires notBool (
      "$cells" in_keys(
        ("result" |-> str(A))
        ("word"   |-> OLDWORD)
        ("n"      |-> OLDN)
        ("_plain" |-> 0)
        REST))

  // End-to-end correctness for every contract-valid sentence: arbitrary
  // count of nonempty alphabetic words, single-space separated, total length
  // from 1 through 100.
  claim [words-in-sentence-correct]:
    <k>
      #loadAll(solutionProgram)
      ~> Call(
           Name("words_in_sentence"),
           str(sentenceCodes(W:WordSeq)))
      =>
      str(filterWords(.IntSeq, W))
    </k>
    <env> 0 </env>
    <scopes>
      (0  |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      (0  |-> scope(
               "words_in_sentence"
                 |-> closureVal(
                       ("sentence", .ParamNames),
                       solutionBody,
                       0),
               parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(wordsVals(W))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validWords(W)
     andBool sentenceLen(W) >=Int 1
     andBool sentenceLen(W) <=Int 100
endmodule
