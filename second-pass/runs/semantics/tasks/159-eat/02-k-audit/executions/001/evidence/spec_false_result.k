requires "/tmp/audit-work/rebuild/verification.k"

module AUDIT-FALSE-RESULT
  imports EAT-VERIFICATION

  // Deliberately false: the actual first element is NUMBER +Int NEED.
  claim
    <k>
      Call(
        Name("eat"),
        Int(NUMBER:Int), Int(NEED:Int), Int(REMAINING:Int))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("eat" |-> eatClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(
             NUMBER +Int NEED +Int 1,
             vCons(REMAINING -Int NEED, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires 0 <=Int NUMBER andBool NUMBER <=Int 1000
     andBool 0 <=Int NEED andBool NEED <=Int 1000
     andBool 0 <=Int REMAINING andBool REMAINING <=Int 1000
     andBool NEED <=Int REMAINING
endmodule
