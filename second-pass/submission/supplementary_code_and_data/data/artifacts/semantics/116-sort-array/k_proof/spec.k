requires "verification.k"

module SORT-ARRAY-SPEC
  imports SORT-ARRAY-VERIFICATION

  // Loading the exact translated module installs the closure used below.
  claim
    <k> #loadAll(sortArrayModule) => .K </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0  |-> scope("sort_array" |-> sortArrayClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // For every list in the task's stated domain, execution returns exactly the
  // reference semantics' stable sort by popcount and then decimal value.
  claim
    <k>
      Call(sortArrayClosure, list(VS))
      =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(VS))
      1 |-> list(sortArraySpec(VS))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNonNegativeInts(VS)

  // The key closure computes the number of "1" digits in bin(N).  The leading
  // "0b" contributes no matches, so this is the supplied semantics' popcount.
  claim
    <k>
      Call(popcountKeyClosure, Int(N))
      =>
      cntSub(
        iCons(48, iCons(98, binCodes(N))),
        iCons(49, .IntSeq))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0

  // Outside the promised domain, the extension assigns every negative the
  // same key.  The stable decimal pre-sort therefore matches the prompt's
  // otherwise out-of-domain negative example.
  claim
    <k> Call(popcountKeyClosure, Int(N)) => 0 </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N <Int 0
endmodule
