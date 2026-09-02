requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [reverse-loop]:
    <k>
      #loop(str(R:IntSeq), Name("char"), reverseLoopBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "is_palindrome" |-> isPalindromeClosure
             "make_palindrome" |-> makePalindromeClosure,
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "string" |-> str(S:IntSeq)
             "reverse_string" |-> (str(A:IntSeq) => str(reverseAcc(R, A)))
             "char" |-> (str(CH:IntSeq) => str(?FINALCHAR:IntSeq)),
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HN:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EC:Int </exit-code>

  claim [search-loop]:
    <k>
      #loop(str(R:IntSeq), Name("char"), searchLoopBody)
      =>
      .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      0 |-> scope(
             "is_palindrome" |-> isPalindromeClosure
             "make_palindrome" |-> makePalindromeClosure,
             parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
             "string" |-> str(S:IntSeq)
             "reverse_string" |-> str(REV:IntSeq)
             "prefix" |-> (str(P:IntSeq) => str(?FINALP:IntSeq))
             "reverse_prefix" |-> (str(RP:IntSeq) => str(?FINALRP:IntSeq))
             "found" |-> (F:Bool => ?FINALF:Bool)
             "result" |-> (
               str(RESULT:IntSeq)
               =>
               str(searchResult(S, R, P, RP, REV, F, RESULT)))
             "char" |-> (str(CH:IntSeq) => str(?FINALCHAR:IntSeq)),
             parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> HEAP:Map </heap>
    <heapLoc> HN:Int </heapLoc>
    <stack> STACK:List </stack>
    <ret> noRet </ret>
    <exc> EXC:Exc </exc>
    <exit-code> EC:Int </exit-code>

  claim [make-palindrome-entry]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("make_palindrome"),
           (str(S:IntSeq), .Exprs))
      =>
      str(completePal(S))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "is_palindrome" |-> isPalindromeClosure
                  "make_palindrome" |-> makePalindromeClosure,
                  parent(-1)))
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
