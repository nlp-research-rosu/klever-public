requires "verification.k"

module SPEC
  imports VERIFICATION

  // The non-exponential primitive operators are proved for arbitrary
  // contract-valid operands; exponentiation is ground because the backend's
  // ^Int hook cannot simplify a symbolic base.
  claim <k>
          runDoAlgebra(
            vCons(plusV, .ValSeq),
            vCons(A:Int, vCons(B:Int, .ValSeq)))
          => A +Int B
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >=Int 0
    [label(plus)]

  claim <k>
          runDoAlgebra(
            vCons(minusV, .ValSeq),
            vCons(A:Int, vCons(B:Int, .ValSeq)))
          => A -Int B
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >=Int 0
    [label(minus)]

  claim <k>
          runDoAlgebra(
            vCons(timesV, .ValSeq),
            vCons(A:Int, vCons(B:Int, .ValSeq)))
          => A *Int B
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >=Int 0
    [label(times)]

  claim <k>
          runDoAlgebra(
            vCons(floorDivV, .ValSeq),
            vCons(A:Int, vCons(B:Int, .ValSeq)))
          => floorQuot(A, B)
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >Int 0
    [label(floor)]

  claim <k>
          runDoAlgebra(
            vCons(powerV, .ValSeq),
            vCons(2, vCons(5, .ValSeq)))
          => 32
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(power)]

  // Rightmost splitting makes subtraction left-associative.
  claim <k>
          runDoAlgebra(
            vCons(minusV, vCons(minusV, .ValSeq)),
            vCons(A:Int, vCons(B:Int, vCons(C:Int, .ValSeq))))
          => (A -Int B) -Int C
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >=Int 0 andBool C >=Int 0
    [label(minus-assoc)]

  // The same split direction makes floor division left-associative.
  claim <k>
          runDoAlgebra(
            vCons(floorDivV, vCons(floorDivV, .ValSeq)),
            vCons(20, vCons(3, vCons(2, .ValSeq))))
          => 3
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(floor-assoc)]

  // Leftmost splitting makes exponentiation right-associative.
  claim <k>
          runDoAlgebra(
            vCons(powerV, vCons(powerV, .ValSeq)),
            vCons(2, vCons(3, vCons(2, .ValSeq))))
          => 512
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    [label(power-assoc)]

  // The prompt's precedence pattern, generalized to arbitrary operands.
  claim <k>
          runDoAlgebra(
            vCons(plusV, vCons(timesV, vCons(minusV, .ValSeq))),
            vCons(A:Int, vCons(B:Int, vCons(C:Int, vCons(D:Int, .ValSeq)))))
          => (A +Int (B *Int C)) -Int D
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >=Int 0
      andBool C >=Int 0 andBool D >=Int 0
    [label(prompt-precedence)]

  // One mixed expression exercises all precedence levels together.
  claim <k>
          runDoAlgebra(
            vCons(plusV,
              vCons(timesV,
                vCons(powerV,
                  vCons(floorDivV, vCons(minusV, .ValSeq))))),
            vCons(A:Int,
              vCons(B:Int,
                vCons(2,
                  vCons(3, vCons(E:Int, vCons(F:Int, .ValSeq)))))))
          => (A +Int floorQuot(B *Int 8, E)) -Int F
        </k>
        <env> 0 </env>
        <scopes>
          (0 |-> scope(.Map, parent(-1)))
          (-1 |-> builtinsScope)
          => ?FINAL_SCOPES:Map
        </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
    requires A >=Int 0 andBool B >=Int 0
      andBool E >Int 0 andBool F >=Int 0
    [label(mixed-precedence)]
endmodule
