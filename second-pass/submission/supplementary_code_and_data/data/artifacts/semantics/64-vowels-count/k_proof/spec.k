requires "verification.k"

module LOOP-SPEC
  imports VOWELS-BASE

  claim [loop-summary]:
    <k>
      #loop(str(S:IntSeq), Name("char"), vowelLoopBody)
      ~> CONTINUATION:K
      =>
      CONTINUATION
    </k>
    <env> 1 </env>
    <scopes>
      SC:Map
      1 |-> scope(
        "s"      |-> ORIGINALS:Str
        "count"  |-> COUNT:Int
        "char"   |-> str(PREVIOUS:IntSeq)
        "last_y" |-> PREVIOUSY:Bool,
        parent(0)
      )
      =>
      SC
      1 |-> scope(
        "s"      |-> ORIGINALS
        "count"  |-> COUNT +Int ordinaryVowels(S)
        "char"   |-> str(finalLowerChar(S, PREVIOUS))
        "last_y" |-> finalIsY(S, PREVIOUSY),
        parent(0)
      )
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HEAPLOC:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (1 in_keys(SC))
endmodule

module MAIN-SPEC
  imports VOWELS-VERIFICATION

  claim [vowels-count-correct]:
    <k>
      #loadAll(vowelsModule)
      ~> Call(Name("vowels_count"), str(S:IntSeq))
      =>
      specifiedVowels(S)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope(
        "vowels_count" |-> closureVal("s", vowelsBody, 0),
        parent(-1)
      )
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
