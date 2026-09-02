requires "verification.k"

module SPEC-FALSE-AUDIT
  imports VERIFICATION

  claim [scan-loop]:
    <k>
      #loop(str(CS:IntSeq), Name("char"), #scanBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "words_in_sentence"
               |-> closureVal("sentence", #wordsBody, 0),
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "sentence" |-> str(INPUT:IntSeq)
             "result"   |-> (str(O:IntSeq) => str(scanOutput(CS, W, O)))
             "word"     |-> (str(W:IntSeq) => str(scanWord(CS, W)))
             "char"     |-> (str(CH:IntSeq) => str(scanLast(CS, CH))),
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(KONT:K, 0, 1)) </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [words-in-sentence-deliberately-false]:
    <k>
      #loadAll(#solutionModule)
      ~> Call(Name("words_in_sentence"), str(CS:IntSeq))
      =>
      str(seqConcat(sentenceResult(CS), iCons(120, .IntSeq)))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
             "words_in_sentence"
               |-> closureVal("sentence", #wordsBody, 0),
             parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 1 <=Int isLen(CS)
     andBool isLen(CS) <=Int 100
endmodule
