requires "verification.k"

module SPEC
  imports VERIFICATION

  claim <k> #runTriples(.ValSeq)
          => hasZeroTriple(.ValSeq) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(empty)]

  claim <k> #runTriples(vCons(A:Int, .ValSeq))
          => hasZeroTriple(vCons(A, .ValSeq)) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(length-one)]

  claim <k> #runTriples(vCons(A:Int, vCons(B:Int, .ValSeq)))
          => hasZeroTriple(vCons(A, vCons(B, .ValSeq))) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(length-two)]

  claim <k> #runTriples(
            vCons(A:Int, vCons(B:Int, vCons(C:Int, .ValSeq))))
          => hasZeroTriple(
            vCons(A, vCons(B, vCons(C, .ValSeq)))) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(length-three)]

  claim <k> #runTriples(
            vCons(A:Int, vCons(B:Int, vCons(C:Int,
              vCons(D:Int, .ValSeq)))))
          => hasZeroTriple(
            vCons(A, vCons(B, vCons(C,
              vCons(D, .ValSeq))))) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(length-four)]

  claim <k> #runTriples(
            vCons(A:Int, vCons(B:Int, vCons(C:Int,
              vCons(D:Int, vCons(E:Int, .ValSeq))))))
          => hasZeroTriple(
            vCons(A, vCons(B, vCons(C,
              vCons(D, vCons(E, .ValSeq)))))) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(length-five)]

  claim <k> #runTriples(
            vCons(A:Int, vCons(B:Int, vCons(C:Int,
              vCons(D:Int, vCons(E:Int,
                vCons(F:Int, .ValSeq)))))))
          => hasZeroTriple(
            vCons(A, vCons(B, vCons(C,
              vCons(D, vCons(E,
                vCons(F, .ValSeq))))))) ... </k>
        <env> 0 </env>
        <scopes>
          0 |-> scope(.Map, parent(-1))
          -1 |-> builtinsScope
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(length-six)]
endmodule
