requires "verification.k"

module BRIDGE-FIXED-SEMANTICS-WITNESS
  imports VOWELS-BASE

  claim [fixed-loop-uses-current-env-zero]:
    <k>
      #loop(str(iCons(97, .IntSeq)), Name("char"), vowelLoopBody)
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 100
        "char" |-> str(iCons(122, .IntSeq))
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 7
        "char" |-> str(iCons(113, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 101
        "char" |-> str(iCons(97, .IntSeq))
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 7
        "char" |-> str(iCons(113, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-FALSE-CONCLUSION-WITNESS
  imports VOWELS-VERIFICATION

  claim [bridge-wrongly-updates-scope-one]:
    <k>
      #loop(str(iCons(97, .IntSeq)), Name("char"), vowelLoopBody)
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 100
        "char" |-> str(iCons(122, .IntSeq))
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 7
        "char" |-> str(iCons(113, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 100
        "char" |-> str(iCons(122, .IntSeq))
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 8
        "char" |-> str(iCons(97, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule

module BRIDGE-FALSE-POST-UNDER-BASE
  imports VOWELS-BASE

  claim [fixed-semantics-rejects-bridge-post]:
    <k>
      #loop(str(iCons(97, .IntSeq)), Name("char"), vowelLoopBody)
      =>
      .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 100
        "char" |-> str(iCons(122, .IntSeq))
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 7
        "char" |-> str(iCons(113, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 100
        "char" |-> str(iCons(122, .IntSeq))
        "last_y" |-> false,
        parent(-1)
      )
      1 |-> scope(
        "s" |-> str(iCons(97, .IntSeq))
        "count" |-> 8
        "char" |-> str(iCons(97, .IntSeq))
        "last_y" |-> false,
        parent(0)
      )
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
