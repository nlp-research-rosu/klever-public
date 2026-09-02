requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal inner-loop theorem: for every non-negative x and every initial
  // accumulator A, the loop adds exactly one for each base-10 digit equal to 7.
  claim
    <k>
      #while(Compare(Name("x"), CmpOp(">", Int(0))), INNER-BODY)
      ~> CONT:K
      =>
      CONT
    </k>
    <env> L:Int </env>
    <scopes>
      ( SC:Map
        L |-> scope(
          ("n" |-> N:Int)
          ("count" |-> A:Int)
          ("i" |-> I:Int)
          ("x" |-> X:Int),
          P:Parent)
      )
      =>
      ( SC
        L |-> scope(
          ("n" |-> N)
          ("count" |-> countSevensAcc(A, X))
          ("i" |-> I)
          ("x" |-> 0),
          P)
      )
    </scopes>
    <scopeLoc> NEXT:Int </scopeLoc>
    <heap> H:Map </heap>
    <heapLoc> HN:Int </heapLoc>
    <stack> ST:List </stack>
    <ret> R:RetState </ret>
    <exc> E:Exc </exc>
    <exit-code> EC:Int </exit-code>
    requires X >=Int 0

  // Full entry-point executions from a pristine module configuration.  These
  // include all prompt examples, the empty/negative boundary, and a wider
  // boundary after the prompt examples.
  claim
    <k> Call(FIZZ-BUZZ-CLOSURE, -5) => 0 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> Call(FIZZ-BUZZ-CLOSURE, 0) => 0 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> Call(FIZZ-BUZZ-CLOSURE, 50) => 0 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> Call(FIZZ-BUZZ-CLOSURE, 78) => 2 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> Call(FIZZ-BUZZ-CLOSURE, 79) => 3 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim
    <k> Call(FIZZ-BUZZ-CLOSURE, 100) => 3 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
