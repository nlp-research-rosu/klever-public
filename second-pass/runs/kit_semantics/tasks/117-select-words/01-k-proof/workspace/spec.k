requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop circularity over the exact ordinary local frame and result-list heap
  // cell.  Return and frame pop remain outside this invariant.
  claim [select-words-loop]:
    <k>
      #loop(str(S:IntSeq), Name("ch"), charLoopBody)
      =>
      .K
      ...
    </k>
    <env> L </env>
    <scopes>
      ...
      L |-> (
        scope(
          "s"      |-> str(ORIGINAL:IntSeq)
          "n"      |-> N:Int
          "result" |-> ref(H:Int)
          "word"   |-> str(WORD:IntSeq)
          "count"  |-> COUNT:Int
          "ch"     |-> str(OLDCH:IntSeq),
          parent(0))
        =>
        scope(
          "s"      |-> str(ORIGINAL)
          "n"      |-> N
          "result" |-> ref(H)
          "word"   |-> str(wordAfter(S, WORD))
          "count"  |-> countAfter(S, COUNT)
          "ch"     |-> str(charAfter(S, OLDCH)),
          parent(0)))
      ...
    </scopes>
    <heap>
      H |-> (list(A:ValSeq) => list(scanAccum(S, N, WORD, COUNT, A)))
      ...
    </heap>
    requires N >=Int 0

  // Whole-program claim from the initial reference configuration.  The
  // function definition, parameter binding, body, loop, return, and heap
  // result all execute under the fixed semantics.
  claim [select-words]:
    <k>
      #loadAll(Module(
        FuncDef("select_words", Params("s", "n"), selectWordsBody)
        .Stmts))
      ~> Call(Name("select_words"), str(S:IntSeq), N:Int)
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "select_words" |->
          closureVal(("s", "n", .ParamNames), selectWordsBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(selectScan(S, N, .IntSeq, 0, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
endmodule
