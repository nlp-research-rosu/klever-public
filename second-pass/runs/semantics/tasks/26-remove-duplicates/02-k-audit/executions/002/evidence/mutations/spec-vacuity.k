requires "verification.k"

module REMOVE-DUPLICATES-SPEC-VACUITY
  imports REMOVE-DUPLICATES-VERIFICATION

  // Induction invariant for the loop.  The result list contains the existing
  // accumulator followed by precisely the singleton-occurrence elements in
  // REST, in their original order.
  claim [loop-invariant]:
    <k>
      #loop(list(REST), Name("number"), #removeDuplicatesBody)
      ~> CONT
      => CONT
    </k>
    <env> LOCAL </env>
    <scopes>
      SCOPES
      LOCAL |-> scope(
        ("number" |-> OLD)
        ("numbers" |-> list(ALL))
        ("result" |-> ref(RESULT)),
        PARENT)
      =>
      SCOPES
      LOCAL |-> scope(
        ("number" |-> ?LAST)
        ("numbers" |-> list(ALL))
        ("result" |-> ref(RESULT)),
        PARENT)
    </scopes>
    <heap>
      (RESULT |-> list(ACC))
      HEAP
      =>
      (RESULT |-> list(keepSinglesAcc(ACC, REST, ALL)))
      HEAP
    </heap>
    requires allInts(ALL)
     andBool allInts(REST)

  // The following exhaustive entry cases establish the theorem for every
  // value satisfying the prompt's List[int] precondition.
  claim [entry-empty]:
    <k>
      Call(#removeDuplicatesClosure, list(.ValSeq), .Exprs)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(999, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [entry-keep]:
    <k>
      Call(
        #removeDuplicatesClosure,
        list(vCons(V, REST)), .Exprs)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           keepSinglesAcc(
             vCons(V, .ValSeq),
             REST,
             vCons(V, REST)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(vCons(V, REST))
     andBool 1 ==Int cntOccVS(vCons(V, REST), V)

  claim [entry-drop]:
    <k>
      Call(
        #removeDuplicatesClosure,
        list(vCons(V, REST)), .Exprs)
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           keepSinglesAcc(
             .ValSeq,
             REST,
             vCons(V, REST)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(vCons(V, REST))
     andBool notBool (
       1 ==Int cntOccVS(vCons(V, REST), V))
endmodule
