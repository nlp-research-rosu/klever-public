requires "verification-body-mutant.k"

module SPEC
  imports VERIFICATION

  claim [digit-sum-bound]:
    <k> .K => .K </k>
    requires digitDomain(D0, D1, D2, D3, D4)
    ensures 0 <=Int D0 +Int D1 +Int D2 +Int D3 +Int D4
        andBool D0 +Int D1 +Int D2 +Int D3 +Int D4 <=Int 36

  claim [solve-sum-00-07]:
    <k>
      #loadAll(solutionModule)
        ~> Call(
             Name("solve"),
             D0:Int +Int 10 *Int
               (D1:Int +Int 10 *Int
                 (D2:Int +Int 10 *Int
                   (D3:Int +Int 10 *Int D4:Int))))
      =>
      str(?CODES:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitDomain(D0, D1, D2, D3, D4)
        andBool D0 +Int D1 +Int D2 +Int D3 +Int D4 <Int 8
    ensures canonicalBin(?CODES)
        andBool decodeBin(?CODES)
          ==Int D0 +Int D1 +Int D2 +Int D3 +Int D4

  claim [solve-sum-08-15]:
    <k>
      #loadAll(solutionModule)
        ~> Call(
             Name("solve"),
             D0:Int +Int 10 *Int
               (D1:Int +Int 10 *Int
                 (D2:Int +Int 10 *Int
                   (D3:Int +Int 10 *Int D4:Int))))
      =>
      str(?CODES:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitDomain(D0, D1, D2, D3, D4)
        andBool 8 <=Int D0 +Int D1 +Int D2 +Int D3 +Int D4
        andBool D0 +Int D1 +Int D2 +Int D3 +Int D4 <Int 16
    ensures canonicalBin(?CODES)
        andBool decodeBin(?CODES)
          ==Int D0 +Int D1 +Int D2 +Int D3 +Int D4

  claim [solve-sum-16-23]:
    <k>
      #loadAll(solutionModule)
        ~> Call(
             Name("solve"),
             D0:Int +Int 10 *Int
               (D1:Int +Int 10 *Int
                 (D2:Int +Int 10 *Int
                   (D3:Int +Int 10 *Int D4:Int))))
      =>
      str(?CODES:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitDomain(D0, D1, D2, D3, D4)
        andBool 16 <=Int D0 +Int D1 +Int D2 +Int D3 +Int D4
        andBool D0 +Int D1 +Int D2 +Int D3 +Int D4 <Int 24
    ensures canonicalBin(?CODES)
        andBool decodeBin(?CODES)
          ==Int D0 +Int D1 +Int D2 +Int D3 +Int D4

  claim [solve-sum-24-31]:
    <k>
      #loadAll(solutionModule)
        ~> Call(
             Name("solve"),
             D0:Int +Int 10 *Int
               (D1:Int +Int 10 *Int
                 (D2:Int +Int 10 *Int
                   (D3:Int +Int 10 *Int D4:Int))))
      =>
      str(?CODES:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitDomain(D0, D1, D2, D3, D4)
        andBool 24 <=Int D0 +Int D1 +Int D2 +Int D3 +Int D4
        andBool D0 +Int D1 +Int D2 +Int D3 +Int D4 <Int 32
    ensures canonicalBin(?CODES)
        andBool decodeBin(?CODES)
          ==Int D0 +Int D1 +Int D2 +Int D3 +Int D4

  claim [solve-sum-32-36]:
    <k>
      #loadAll(solutionModule)
        ~> Call(
             Name("solve"),
             D0:Int +Int 10 *Int
               (D1:Int +Int 10 *Int
                 (D2:Int +Int 10 *Int
                   (D3:Int +Int 10 *Int D4:Int))))
      =>
      str(?CODES:IntSeq)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      ?SCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitDomain(D0, D1, D2, D3, D4)
        andBool 32 <=Int D0 +Int D1 +Int D2 +Int D3 +Int D4
    ensures canonicalBin(?CODES)
        andBool decodeBin(?CODES)
          ==Int D0 +Int D1 +Int D2 +Int D3 +Int D4
endmodule
