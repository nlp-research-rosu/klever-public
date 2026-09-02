requires "verification.k"

// Same split redex under fixed semantics: it allocates and returns a list ref.
module SPLIT-FIXED-WITNESS
  imports ANTI-SHUFFLE-BASE

  claim [fixed-split-allocates]:
    <k>
      #applyK(
        toCall(boundMethodV(
          str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
          "split")),
        (str(iCons(32, .IntSeq)), .Vals))
      =>
      ref(0)
    </k>
    <heap>
      .Map
      =>
      0 |-> list(
        vCons(str(iCons(97, .IntSeq)),
        vCons(str(iCons(98, .IntSeq)), .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
endmodule

// Candidate split bridge: the identical redex fabricates a custom iterator
// and silently omits the fixed allocation.
module SPLIT-EXTENDED-WITNESS
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  claim [extended-split-skips-allocation]:
    <k>
      #applyK(
        toCall(boundMethodV(
          str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
          "split")),
        (str(iCons(32, .IntSeq)), .Vals))
      =>
      wordsObj(
        wCons(iCons(97, .IntSeq),
        wCons(iCons(98, .IntSeq), .Words)))
    </k>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
endmodule

// Fixed evaluation of the real nested list/sorted/join expression allocates
// the list(word) and sorted(...) temporaries.
module WORD-FIXED-WITNESS
  imports ANTI-SHUFFLE-BASE

  claim [fixed-word-allocates]:
    <k>
      Call(
        Attribute(Str(""), "join"),
        Call(Name("sorted"), Call(Name("list"), Name("word"))))
      =>
      str(sortWord(iCons(98, iCons(97, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "word" |-> str(iCons(98, iCons(97, .IntSeq))),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      (0 |-> list(charsOf(iCons(98, iCons(97, .IntSeq)))))
      (1 |-> list(sortVS(charsOf(iCons(98, iCons(97, .IntSeq))))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

// Candidate word bridge returns the same value while falsely preserving the
// heap and allocation counter.
module WORD-EXTENDED-WITNESS
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  claim [extended-word-skips-allocation]:
    <k>
      Call(
        Attribute(Str(""), "join"),
        Call(Name("sorted"), Call(Name("list"), Name("word"))))
      =>
      str(sortWord(iCons(98, iCons(97, .IntSeq))))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
        "word" |-> str(iCons(98, iCons(97, .IntSeq))),
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
endmodule

// Without the final loop-summary rule, a one-word loop leaves the loop target
// bound to that word, so the admitted immediate continuation observes "ba".
module LOOP-FIXED-WITNESS
  imports ANTI-SHUFFLE-LOOP-VERIFICATION

  claim [fixed-loop-updates-word]:
    <k>
      #loop(
        wordsObj(wCons(iCons(98, iCons(97, .IntSeq)), .Words)),
        Name("word"),
        antiLoopBody)
      ~> Name("word")
      =>
      str(iCons(98, iCons(97, .IntSeq)))
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "result" |-> str(.IntSeq)
        "s"      |-> str(iCons(98, iCons(97, .IntSeq)))
        "word"   |-> str(.IntSeq),
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?SCFINAL:Map
    </scopes>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
endmodule

// The final candidate rule accepts that same continuation but skips the
// target binding, so the continuation observes the stale empty value.
module LOOP-EXTENDED-WITNESS
  imports ANTI-SHUFFLE-VERIFICATION

  claim [extended-loop-leaves-word-stale]:
    <k>
      #loop(
        wordsObj(wCons(iCons(98, iCons(97, .IntSeq)), .Words)),
        Name("word"),
        antiLoopBody)
      ~> Name("word")
      =>
      str(.IntSeq)
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        "result" |-> str(.IntSeq)
        "s"      |-> str(iCons(98, iCons(97, .IntSeq)))
        "word"   |-> str(.IntSeq),
        parent(0))
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?SCFINAL:Map
    </scopes>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
endmodule
