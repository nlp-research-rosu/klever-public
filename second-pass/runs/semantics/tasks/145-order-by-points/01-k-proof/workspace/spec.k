requires "verification.k"

module ORDER-BY-POINTS-SPEC
  imports ORDER-BY-POINTS-VERIFICATION

  claim
    <k> #runDigitSum(0) => 0 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #runDigitSum(1) => 1 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #runDigitSum(11) => 2 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #runDigitSum(-1) => -1 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #runDigitSum(-11) => 0 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #runDigitSum(-12) => 1 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #runDigitSum(-123) => 4 </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>

  claim
    <k> #runOrderByPoints(list(VS:ValSeq)) => ref(0) </k>
    <env> 0 </env>
    <scopes> initialScopes => loadedScopes </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortKeyVS(VS, digitSumClosure))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
