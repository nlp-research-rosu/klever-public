requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [split-words-empty]:
    <k>
      Call(Name("split_words"), str(.IntSeq), .Exprs)
      => 0
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "split_words" |-> closureVal(("txt", .ParamNames), splitWordsBody, 0),
               parent(-1)
             )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim [split-words-whitespace]:
    <k>
      Call(Name("split_words"), str(CS:IntSeq), .Exprs)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "split_words" |-> closureVal(("txt", .ParamNames), splitWordsBody, 0),
               parent(-1)
             )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(splitWS(CS, .IntSeq, .ValSeq))
         1 |-> list(vCons(str(CS), .ValSeq))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires notBool (CS ==K .IntSeq)
      andBool notBool (
        splitWS(CS, .IntSeq, .ValSeq)
          ==K vCons(str(CS), .ValSeq)
      )

  claim [split-words-comma]:
    <k>
      Call(Name("split_words"), str(CS:IntSeq), .Exprs)
      => ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "split_words" |-> closureVal(("txt", .ParamNames), splitWordsBody, 0),
               parent(-1)
             )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(splitWS(CS, .IntSeq, .ValSeq))
         1 |-> list(vCons(str(CS), .ValSeq))
         2 |-> list(splitSep(CS, 44, .IntSeq))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires notBool (CS ==K .IntSeq)
      andBool (
        splitWS(CS, .IntSeq, .ValSeq)
          ==K vCons(str(CS), .ValSeq)
      )
      andBool strContains(iCons(44, .IntSeq), CS)

  claim [split-words-count]:
    <k>
      Call(Name("split_words"), str(CS:IntSeq), .Exprs)
      => oddAlphabetCount(CS)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
               "split_words" |-> closureVal(("txt", .ParamNames), splitWordsBody, 0),
               parent(-1)
             )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(splitWS(CS, .IntSeq, .ValSeq))
         1 |-> list(vCons(str(CS), .ValSeq))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires notBool (CS ==K .IntSeq)
      andBool (
        splitWS(CS, .IntSeq, .ValSeq)
          ==K vCons(str(CS), .ValSeq)
      )
      andBool notBool strContains(iCons(44, .IntSeq), CS)
endmodule
