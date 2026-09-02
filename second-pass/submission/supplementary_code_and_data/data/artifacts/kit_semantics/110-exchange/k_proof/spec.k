requires "verification.k"

module SPEC
  imports VERIFICATION

  // One universal loop theorem applies to both syntactic for-loops, whose
  // bodies and state footprints are identical.
  claim [count-loop]:
    <k>
      #loop(list(VS:ValSeq), Name("value"), countBody)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ("lst1" |-> INPUT1:Val)
        ("lst2" |-> INPUT2:Val)
        ("even_count" |-> (C:Int => C +Int evenCount(VS)))
        ("value" |-> (_V0:Val => ?V1:Val))
        .Map,
        parent(0))
      ...
    </scopes>
    <heap> .Map </heap>
    requires allNumbers(VS)

  // Full entry-point theorem over arbitrary non-empty finite numeric lists.
  // All fixed semantics state starts in the reference initial configuration;
  // the returned value, normal control state, and absence of side effects are
  // observed at termination.
  claim [exchange]:
    <k>
      #loadAll(exchangeProgram)
      ~> Call(
           Name("exchange"),
           list(VS1:ValSeq),
           list(VS2:ValSeq))
      => exchangeResult(VS1, VS2)
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNumbers(VS1) andBool allNumbers(VS2)
      andBool vsLen(VS1) >Int 0 andBool vsLen(VS2) >Int 0
endmodule
